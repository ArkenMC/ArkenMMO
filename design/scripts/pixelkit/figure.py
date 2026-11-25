"""Steps every hero shares: lean, facing, stair-stepped items, rim light, clean-up and detail grids.

Heroes are always posed facing the viewer's right. A left-facing hero is the same geometry
mirrored *before* it is lit, so the light still comes from the top left (no image is flipped).
"""
import numpy as np

from .draw import Canvas, dilate, poly_mask, shift
from .hullrig import rot
from .palette import col

LEAN_PIVOT = np.array((0.0, 56.0, 0.0))
MIRROR = np.array((-1.0, 1.0, 1.0))


class Figure:
    """A posed rig plus the rules for painting it.

    `lean` is the roll of everything above the legs in degrees (negative leans to the viewer's right).
    `blocky` lists group name prefixes that get stair-stepped edges.
    `rim` maps a material to the (ramp, step) of the bounce light on right-facing edges; groups starting
    with a `no_rim` prefix are skipped. `details` are callables drawing hand-placed grids last.
    `facing` is 1 for the viewer's right and -1 for the viewer's left.
    """

    def __init__(self, rig, lean=0.0, blocky=(), rim=None, no_rim=(), details=(), facing=1):
        self.rig, self.rim, self.facing = rig, rim or {}, facing
        self.blocky, self.no_rim, self.details = tuple(blocky), tuple(no_rim), tuple(details)
        self._lean = rot("z", lean)
        for part in rig.parts:
            if not part.group.startswith("leg_"):
                part.points = self.lean(part.points)
        if facing < 0:
            for part in rig.parts:
                part.points = part.points * MIRROR
            rig.mirror_view()

    def lean(self, points):
        return (np.asarray(points, float) - LEAN_PIVOT) @ self._lean.T + LEAN_PIVOT

    def screen(self, point, origin, leaned=True):
        """Screen pixel of a point given in the right-facing, unleaned pose."""
        point = self.lean(point) if leaned else np.asarray(point, float)
        if self.facing < 0:
            point = point * MIRROR
        x, y = self.rig.project(point, origin)
        return int(round(x)), int(round(y))

    def paint(self, size, origin):
        """The finished figure: rendered planes, rim light, clean-up, then the hand-placed details."""
        if self.blocky:
            buffers = self.rig.render_blocky(size, origin, lambda g: g.startswith(self.blocky))
        else:
            buffers = self.rig.render(size, origin)
        canvas = buffers.paint()
        self._rim_light(buffers, canvas)
        canvas.despeckle()
        for detail in self.details:
            detail(self, canvas, origin)
        return canvas

    def _rim_light(self, buffers, canvas):
        """One pixel of bounce light on edges that face right; vertical runs only."""
        edge = buffers.mask & ~shift(buffers.mask, -1, 0)
        edge &= shift(edge, 0, 1) | shift(edge, 0, -1) | shift(edge, 1, 1) | shift(edge, -1, -1)
        for y, x in zip(*np.nonzero(edge)):
            part = buffers.parts[buffers.part_id[y, x]]
            if part.material in self.rim and not (self.no_rim and part.group.startswith(self.no_rim)):
                canvas.px[y, x] = col(*self.rim[part.material])


def grid_detail(rows, legend, anchor, offset=None, leaned=True, flip=True):
    """A detail that stamps a pixel grid at a figure-space anchor point (centred unless `offset`).

    On a left-facing hero the grid and its offset are mirrored with the pose; `flip=False` keeps the
    grid itself unmirrored, for symbols with a reading direction.
    """
    def draw(figure, canvas, origin):
        x, y = figure.screen(anchor, origin, leaned)
        width = len(rows[0])
        dx, dy = offset if offset is not None else (-(width // 2), -(len(rows) // 2))
        stamped = rows
        if figure.facing < 0:
            dx = -dx - width
            if flip:
                stamped = [row[::-1] for row in rows]
        canvas.grid(stamped, legend, (x + dx, y + dy))
    return draw


def facet_art(shapes, ring=None, face_ring=None, face_line=0):
    """Hand-shaped flat facets as a detail layer, for hair that boxes cannot draw.

    `shapes` are painted in order as (points, (ramp, step), edge); points are art px around the
    anchor, and `edge` is (ramp, step) for a 1 px rim inside the shape, or None. A shape with two
    points is a 1 px strand line. `ring` outlines the whole layer; above `face_line` it uses `face_ring`.
    """
    width, height, ax, ay = 64, 64, 32, 16

    def draw(canvas, at, flipped):
        layer = Canvas(width, height)
        for points, colour, edge in shapes:
            moved = [(ax + x, ay + y) for x, y in points]
            if len(moved) == 2:
                (x0, y0), (x1, y1) = moved
                steps = max(abs(x1 - x0), abs(y1 - y0), 1)
                for i in range(steps + 1):
                    layer.dot(round(x0 + (x1 - x0) * i / steps), round(y0 + (y1 - y0) * i / steps), col(*colour))
                continue
            mask = poly_mask(moved, layer.size)
            layer.mask(mask, col(*colour))
            if edge:
                inner = mask.copy()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    inner &= shift(mask, dx, dy)
                layer.mask(mask & ~inner, col(*edge))
        layer.despeckle(1)
        if ring:
            solid = layer.px[..., 3] > 0
            outline = dilate(solid) & ~solid
            layer.mask(outline, col(*ring))
            if face_ring:
                above = outline.copy()
                above[ay + face_line:] = False
                layer.mask(above, col(*face_ring))
        pixels = layer.px[:, ::-1] if flipped else layer.px
        for y, x in zip(*np.nonzero(pixels[..., 3])):
            canvas.dot(at[0] - ax + x, at[1] - ay + y, pixels[y, x])
    return draw


def facet_detail(anchor, art, leaned=True):
    """Stamps `facet_art` at a figure-space anchor; it mirrors with the pose."""
    def draw(figure, canvas, origin):
        art(canvas, figure.screen(anchor, origin, leaned), figure.facing < 0)
    return draw


def mirrored_x(points):
    return [(-x, y) for x, y in points]


def pixel_blocks(rows, cell):
    """Scale a hand-drawn grid so each character is a `cell` x `cell` square, as in a block-game sprite."""
    return ["".join(ch * cell for ch in row) for row in rows for _ in range(cell)]


def block_eye(white, iris, glint=None, mirrored=False, block=4):
    """A block-game eye: two squares side by side, the iris nearest the nose.

    Both squares are `block` art px, so they stay crisp at GUI scale 3. `glint` lights the top corner
    of the iris. The unmirrored eye is the viewer's left one.
    """
    rows = []
    for y in range(block):
        row = list(white * block + iris * block)
        if glint and y < block // 2:
            row[block:block + block // 2] = glint * (block // 2)
        rows.append("".join(row[::-1] if mirrored else row))
    return rows
