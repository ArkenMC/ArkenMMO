"""Tiny flat-shaded renderer for faceted figures.

A part is the convex hull of a point list, so chamfered plates, wedges and blades are all real
geometry. Figure space: x to the viewer's right, y up from the ground, z toward the viewer;
one unit is one art pixel. Projection is orthographic, straight to the target resolution.
"""
from dataclasses import dataclass

import numpy as np
from scipy.spatial import ConvexHull

from .draw import Canvas, dilate, shift
from .palette import col


def rot(axis, degrees):
    a = np.radians(degrees)
    c, s = np.cos(a), np.sin(a)
    return np.array({"x": [[1, 0, 0], [0, c, -s], [0, s, c]],
                     "y": [[c, 0, s], [0, 1, 0], [-s, 0, c]],
                     "z": [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[axis])


def euler(yaw=0, pitch=0, roll=0):
    return rot("y", yaw) @ rot("x", pitch) @ rot("z", roll)


def slab(bottom, top, height, chamfer=0.0, top_shift=(0, 0)):
    """Tapered block centred on the origin with chamfered edges; bottom/top are (width, depth)."""
    pts = []
    for (w, d), y, (sx, sz) in ((bottom, -height / 2, (0, 0)), (top, height / 2, top_shift)):
        inward = chamfer if y < 0 else -chamfer
        for fx in (-1, 1):
            for fz in (-1, 1):
                hx, hz = fx * w / 2, fz * d / 2
                # two points on the end ring pulled in sideways, two on the side pulled in vertically
                pts.append((hx - fx * chamfer + sx, y, hz + sz))
                pts.append((hx + sx, y, hz - fz * chamfer + sz))
                pts.append((hx + sx, y + inward, hz - fz * chamfer + sz))
                pts.append((hx - fx * chamfer + sx, y + inward, hz + sz))
    return np.array(pts, float)


def box(w, h, d, chamfer=0.0):
    return slab((w, d), (w, d), h, chamfer)


def prism(outline, z0, z1):
    """Extrude a convex xy outline from z0 to z1."""
    return np.array([(x, y, z) for z in (z0, z1) for x, y in outline], float)


@dataclass
class Part:
    points: np.ndarray
    material: str
    base: int
    group: str
    lo: int = 1
    hi: int = 99


class Rig:
    def __init__(self, yaw=28.0, pitch=10.0, light=(-0.46, 0.66, 0.60), scale=1.0):
        self.scale = scale
        self.view = rot("x", pitch) @ rot("y", yaw)
        light = np.array(light, float)
        self.light = light / np.linalg.norm(light)
        self.parts = []

    def add(self, points, material, base, group, at=(0, 0, 0), turn=None, lo=1, hi=99):
        """`turn` rotates the points about their own origin before they move to `at`."""
        pts = np.array(points, float)
        if turn is not None:
            pts = pts @ turn.T
        self.parts.append(Part(pts + np.array(at, float), material, base, group, lo, hi))

    def bone(self, p0, p1, size0, size1, material, base, group, chamfer=2.0, lo=1):
        """Tapered limb segment from joint p0 to joint p1; sizes are (width, depth)."""
        p0, p1 = np.array(p0, float), np.array(p1, float)
        length = np.linalg.norm(p1 - p0)
        up = (p1 - p0) / length
        side = np.cross(up, (0, 0, 1))
        side = side / np.linalg.norm(side) if np.linalg.norm(side) > 1e-6 else np.array((1.0, 0, 0))
        if side[0] < 0:
            side = -side
        basis = np.column_stack((side, up, np.cross(side, up)))
        pts = slab(size0, size1, length, chamfer) @ basis.T + (p0 + p1) / 2
        self.parts.append(Part(pts, material, base, group, lo))

    def project(self, point, origin):
        v = self.view @ np.array(point, float) * self.scale
        return (origin[0] + v[0], origin[1] - v[1])

    def _shade(self, dot):
        for limit, delta in ((0.80, 2), (0.52, 1), (0.10, 0), (-0.28, -1)):
            if dot > limit:
                return delta
        return -2

    def render(self, size, origin):
        """Rasterise into per-pixel buffers: depth, part index, face index and ramp step."""
        w, h = size
        depth = np.full((h, w), -1e9)
        part_id = np.full((h, w), -1)
        face_id = np.full((h, w), -1)
        level = np.zeros((h, w), int)
        faces = 0
        for index, part in enumerate(self.parts):
            pts = part.points @ self.view.T * self.scale
            screen = np.column_stack((origin[0] + pts[:, 0], origin[1] - pts[:, 1]))
            hull = ConvexHull(pts)
            planes = {}
            for simplex, eq in zip(hull.simplices, hull.equations):
                planes.setdefault(tuple(np.round(eq, 2)), []).append((simplex, eq))
            for tris in planes.values():
                normal = tris[0][1][:3]
                if normal[2] <= 0.03:
                    continue
                faces += 1
                step = int(np.clip(part.base + self._shade(float(normal @ self.light)), part.lo, part.hi))
                offset = tris[0][1][3]
                for simplex, _ in tris:
                    a, b, c = screen[simplex]
                    x0, y0 = np.floor(np.minimum.reduce((a, b, c))).astype(int)
                    x1, y1 = np.ceil(np.maximum.reduce((a, b, c))).astype(int) + 1
                    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, w), min(y1, h)
                    if x0 >= x1 or y0 >= y1:
                        continue
                    ys, xs = np.mgrid[y0:y1, x0:x1] + 0.5
                    area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                    if abs(area) < 1e-6:
                        continue
                    inside = np.ones(xs.shape, bool)
                    for p, q in ((a, b), (b, c), (c, a)):
                        edge = (q[0] - p[0]) * (ys - p[1]) - (q[1] - p[1]) * (xs - p[0])
                        inside &= edge * np.sign(area) >= -1e-7
                    # plane: n . (X, Y, Z) + offset = 0 with X = sx - ox, Y = oy - sy
                    z = -(normal[0] * (xs - origin[0]) + normal[1] * (origin[1] - ys) + offset) / normal[2]
                    win = inside & (z > depth[y0:y1, x0:x1] + 1e-6)
                    depth[y0:y1, x0:x1][win] = z[win]
                    part_id[y0:y1, x0:x1][win] = index
                    face_id[y0:y1, x0:x1][win] = faces
                    level[y0:y1, x0:x1][win] = step
        return Buffers(self.parts, depth, part_id, face_id, level)


class Buffers:
    def __init__(self, parts, depth, part_id, face_id, level):
        self.parts, self.depth, self.part_id, self.face_id, self.level = parts, depth, part_id, face_id, level
        self.mask = part_id >= 0
        names = sorted({p.group for p in parts})
        lookup = np.array([names.index(p.group) for p in parts] + [-1])
        self.group = lookup[part_id]

    def _occluded(self, dx, dy, threshold):
        """Pixels whose neighbour at offset (-dx, -dy) is a different, clearly nearer group."""
        moved_group = np.full_like(self.group, -1)
        moved_depth = np.full_like(self.depth, -1e9)
        h, w = self.group.shape
        dst = (slice(max(0, dy), h + min(0, dy)), slice(max(0, dx), w + min(0, dx)))
        src = (slice(max(0, -dy), h + min(0, -dy)), slice(max(0, -dx), w + min(0, -dx)))
        moved_group[dst] = self.group[src]
        moved_depth[dst] = self.depth[src]
        return self.mask & (moved_group >= 0) & (moved_group != self.group) & (moved_depth - self.depth > threshold)

    def clean(self, passes=2):
        """Merge single-pixel slivers into the surrounding face so no orphan texels remain."""
        h, w = self.mask.shape
        for _ in range(passes):
            for y, x in zip(*np.nonzero(self.mask)):
                if not (0 < y < h - 1 and 0 < x < w - 1):
                    continue
                around = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                same = sum(self.face_id[p] == self.face_id[y, x] for p in around)
                solid = [p for p in around if self.mask[p]]
                if same > 0 or not solid:
                    continue
                best = max(solid, key=lambda p: sum(self.face_id[q] == self.face_id[p] for q in solid))
                for buf in (self.part_id, self.face_id, self.level, self.group, self.depth):
                    buf[y, x] = buf[best]

    def paint(self, outline=2):
        """Resolve ramp steps to colours, with contact shadows, separation lines and outline."""
        self.clean()
        floor = np.array([p.lo for p in self.parts] + [0])[self.part_id]
        shadow = self._occluded(2, 3, 5.0) | self._occluded(1, 2, 5.0)
        level = np.where(shadow, np.maximum(self.level - 1, floor), self.level)
        line = np.zeros_like(self.mask)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            line |= self._occluded(dx, dy, 2.5)
        level = np.where(line, np.maximum(floor - 1, 0), level)
        canvas = Canvas(self.mask.shape[1], self.mask.shape[0])
        for y, x in zip(*np.nonzero(self.mask)):
            canvas.px[y, x] = col(self.parts[self.part_id[y, x]].material, int(level[y, x]))
        self._outline(canvas, outline)
        return canvas

    def _outline(self, canvas, width):
        grown = self.mask.copy()
        source = self.part_id.copy()
        h, w = source.shape
        for ring in range(width):
            wider = dilate(grown)
            filled = source.copy()
            for y, x in zip(*np.nonzero(wider & ~grown)):
                for ny, nx in ((y + 1, x), (y, x + 1), (y, x - 1), (y - 1, x)):
                    if 0 <= ny < h and 0 <= nx < w and grown[ny, nx]:
                        filled[y, x] = source[ny, nx]
                        break
                part = self.parts[filled[y, x]]
                # selective outline: the outer ring lifts one step where the edge faces the light
                lit = ring == width - 1 and any(
                    0 <= y + d < h and 0 <= x + d < w and self.mask[y + d, x + d] for d in (2, 3))
                canvas.px[y, x] = col(part.material, 1 if lit else 0)
            grown, source = wider, filled
