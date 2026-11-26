"""Hard-edged shape primitives for 24x24 sigil masks, sampled at pixel centres."""
import numpy as np

from .draw import dilate, poly_mask

SIZE = 24
_YS, _XS = np.mgrid[0:SIZE, 0:SIZE] + 0.5


def grid(text):
    """A hand-authored mask: one character per pixel, '#' is carved."""
    rows = [row.strip() for row in text.strip().split("\n")]
    if len(rows) != SIZE or any(len(row) != SIZE for row in rows):
        raise ValueError(f"icon grid must be {SIZE}x{SIZE}: {[len(r) for r in rows]}")
    return np.array([[ch == "#" for ch in row] for row in rows])


def poly(*points):
    return poly_mask(points, (SIZE, SIZE))


def union(*masks):
    out = np.zeros((SIZE, SIZE), bool)
    for mask in masks:
        out |= mask
    return out


def cut(mask, *holes):
    """`mask` with every hole removed."""
    return mask & ~union(*holes)


def apart(front, back):
    """`front` laid over `back` with a 1 px gap around it, so the two stay separate shapes."""
    return front | (back & ~dilate(front))


def box(x0, y0, x1, y1):
    return (_XS > x0) & (_XS < x1) & (_YS > y0) & (_YS < y1)


def disc(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    return ((_XS - cx) / rx) ** 2 + ((_YS - cy) / ry) ** 2 <= 1


def arc(cx, cy, outer, inner, start=0, end=360):
    """A ring section; angles in degrees, 0 points right and 90 points down."""
    radius = np.hypot(_XS - cx, _YS - cy)
    angle = np.degrees(np.arctan2(_YS - cy, _XS - cx)) % 360
    sweep = (angle - start) % 360 <= (end - start if end - start >= 360 else (end - start) % 360)
    return (radius <= outer) & (radius >= inner) & sweep


def stroke(width, *points):
    """A polyline `width` px thick with flat ends."""
    out = np.zeros((SIZE, SIZE), bool)
    for (ax, ay), (bx, by) in zip(points, points[1:]):
        dx, dy = bx - ax, by - ay
        length = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / length * width / 2, dx / length * width / 2
        out |= poly((ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny))
    for x, y in points[1:-1]:
        out |= disc(x, y, width / 2)
    return out


def head(tip, direction, length, width):
    """A triangular arrow or spear point whose tip is at `tip`, flying along `direction`."""
    dx, dy = direction
    norm = (dx * dx + dy * dy) ** 0.5
    dx, dy = dx / norm, dy / norm
    bx, by = tip[0] - dx * length, tip[1] - dy * length
    return poly(tip, (bx - dy * width / 2, by + dx * width / 2), (bx + dy * width / 2, by - dx * width / 2))


def arrow(tail, tip, shaft, length, width):
    dx, dy = tip[0] - tail[0], tip[1] - tail[1]
    norm = (dx * dx + dy * dy) ** 0.5
    neck = (tip[0] - dx / norm * length * 0.7, tip[1] - dy / norm * length * 0.7)
    return stroke(shaft, tail, neck) | head(tip, (dx, dy), length, width)


def diamond(cx, cy, rx, ry):
    return poly((cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy))


def mirrored(mask):
    """The mask joined with its left-right mirror image."""
    return mask | mask[:, ::-1]
