"""Hard-edged drawing helpers on numpy RGBA arrays. No anti-aliasing, no resampling."""
import numpy as np
from PIL import Image

from .palette import col


class Canvas:
    def __init__(self, width, height):
        self.px = np.zeros((height, width, 4), np.uint8)

    @property
    def size(self):
        return self.px.shape[1], self.px.shape[0]

    def image(self):
        return Image.fromarray(self.px, "RGBA")

    def rect(self, r, colour):
        x0, y0, x1, y1 = r
        self.px[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = colour

    def dot(self, x, y, colour):
        if 0 <= x < self.px.shape[1] and 0 <= y < self.px.shape[0]:
            self.px[y, x] = colour

    def mask(self, mask, colour):
        self.px[mask] = colour

    def poly(self, points, colour, clip=None):
        m = poly_mask(points, self.size)
        if clip is not None:
            m &= rect_mask(clip, self.size)
        self.px[m] = colour

    def paste(self, other, clip=None):
        """Binary-alpha composite of a same-sized canvas."""
        solid = other.px[..., 3] > 0
        if clip is not None:
            solid &= rect_mask(clip, self.size)
        self.px[solid] = other.px[solid]

    def despeckle(self, passes=2):
        """Give every lone texel (no neighbour of its colour, diagonals included) its neighbours' main colour."""
        height, width = self.px.shape[:2]
        for _ in range(passes):
            source = self.px.copy()
            for y, x in zip(*np.nonzero(source[..., 3])):
                around = [tuple(source[y + dy, x + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                          if (dx or dy) and 0 <= y + dy < height and 0 <= x + dx < width]
                solid = [c for c in around if c[3]]
                if solid and tuple(source[y, x]) not in around:
                    self.px[y, x] = max(sorted(set(solid)), key=solid.count)

    def grid(self, rows, legend, at):
        """Hand-authored pixel grid: one character per pixel, '.' is transparent."""
        width = len(rows[0])
        for dy, row in enumerate(rows):
            if len(row) != width:
                raise ValueError(f"ragged pixel grid row {dy}: {row!r}")
            for dx, ch in enumerate(row):
                if ch != ".":
                    self.dot(at[0] + dx, at[1] + dy, col(*legend[ch]))


def rect_mask(r, size):
    m = np.zeros((size[1], size[0]), bool)
    x0, y0, x1, y1 = r
    m[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = True
    return m


def poly_mask(points, size):
    """Even-odd fill sampled at pixel centres, so adjacent polygons never overlap."""
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w]
    xs, ys = xs + 0.5, ys + 0.5
    inside = np.zeros((h, w), bool)
    points = list(points)
    for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1]):
        if ay == by:
            continue
        crosses = (ay <= ys) != (by <= ys)
        inside ^= crosses & (xs < ax + (ys - ay) * (bx - ax) / (by - ay))
    return inside


def shift(mask, dx, dy):
    """Mask moved by (dx, dy), filled with False."""
    out = np.zeros_like(mask)
    h, w = mask.shape
    out[max(0, dy):h + min(0, dy), max(0, dx):w + min(0, dx)] = \
        mask[max(0, -dy):h + min(0, -dy), max(0, -dx):w + min(0, -dx)]
    return out


def dilate(mask):
    return mask | shift(mask, 1, 0) | shift(mask, -1, 0) | shift(mask, 0, 1) | shift(mask, 0, -1)


def frame(canvas, r, layers):
    """Concentric 1px rings from the outside in; each layer is (top/left colour, bottom/right colour)."""
    x0, y0, x1, y1 = r
    for i, (top, bottom) in enumerate(layers):
        canvas.rect((x0 + i, y0 + i, x1 - i, y0 + i + 1), top)
        canvas.rect((x0 + i, y0 + i, x0 + i + 1, y1 - i), top)
        canvas.rect((x0 + i + 1, y1 - i - 1, x1 - i, y1 - i), bottom)
        canvas.rect((x1 - i - 1, y0 + i + 1, x1 - i, y1 - i), bottom)


def dither_band(canvas, r, upper, lower):
    """Vertical transition from `upper` to `lower`: sparse, checker, then dense."""
    x0, y0, x1, y1 = r
    for y in range(y0, y1):
        t = (y - y0 + 0.5) / (y1 - y0)
        for x in range(x0, x1):
            sparse = (x % 4 == 0 and y % 2 == 0) or (x % 4 == 2 and y % 2 == 1)
            if t < 0.34:
                use_lower = sparse
            elif t < 0.67:
                use_lower = (x + y) % 2 == 0
            else:
                use_lower = not sparse
            canvas.dot(x, y, lower if use_lower else upper)
