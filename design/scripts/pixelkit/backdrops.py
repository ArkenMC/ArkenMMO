"""Panel backdrops. Darker and less saturated than any figure, built in layers for depth."""
import random

import numpy as np

from .draw import Canvas, dither_band, poly_mask, rect_mask
from .palette import PALETTE, col


def _sky(canvas, rect, ramp, bands):
    """`bands` is a list of (bottom y offset, ramp step); neighbours blend through a dithered strip."""
    x0, y0, x1, _ = rect
    top = y0
    for i, (bottom, step) in enumerate(bands):
        canvas.rect((x0, top, x1, y0 + bottom), col(ramp, step))
        if i:
            dither_band(canvas, (x0, top - 4, x1, top + 4), col(ramp, bands[i - 1][1]), col(ramp, step))
        top = y0 + bottom


def _lift(canvas, mask, ramp):
    """Raise sky pixels inside `mask` by one ramp step, which keeps dithering intact."""
    colours = PALETTE[ramp]
    source = canvas.px.copy()
    for low, high in zip(colours[:-1], colours[1:]):
        hit = mask & np.all(source[..., :3] == low, axis=-1)
        canvas.px[hit] = high + (255,)


def _rays(canvas, rect, centre, ramp, limit):
    x0, y0, x1, y1 = rect
    mask = np.zeros(canvas.px.shape[:2], bool)
    for start in range(-180, 180, 30):
        a, b = np.radians((start, start + 11))
        mask |= poly_mask([centre, (centre[0] + 260 * np.cos(a), centre[1] + 260 * np.sin(a)),
                           (centre[0] + 260 * np.cos(b), centre[1] + 260 * np.sin(b))], canvas.size)
    mask &= rect_mask((x0, y0, x1, limit), canvas.size)
    _lift(canvas, mask, ramp)


def _halo(canvas, rect, centre, radius):
    """A low sun behind the head, with one thin ring: it frames the face, the focal point."""
    ys, xs = np.mgrid[0:canvas.size[1], 0:canvas.size[0]] + 0.5
    distance = np.hypot(xs - centre[0], ys - centre[1])
    inside = rect_mask(rect, canvas.size)
    _lift(canvas, inside & (distance < radius), "ember_sky")
    _lift(canvas, inside & (distance > radius + 5) & (distance < radius + 8), "ember_sky")


def _wall(canvas, rect, base_y, towers, merlon, colour, edge):
    """Castle silhouette: a crenellated curtain wall plus towers given as (x offset, width, top)."""
    x0, _, x1, y1 = rect
    shape = Canvas(*canvas.size)
    shape.rect((x0, base_y, x1, y1), colour)
    for x in range(x0 + 2, x1, merlon * 2):
        shape.rect((x, base_y - 4, x + merlon, base_y), colour)
    for offset, width, top in towers:
        left = x0 + offset
        shape.rect((left, top + 6, left + width, base_y), colour)
        shape.rect((left - 2, top + 3, left + width + 2, top + 9), colour)
        for x in range(left - 2, left + width + 2, 6):
            shape.rect((x, top - 1, x + 4, top + 3), colour)
    solid = shape.px[..., 3] > 0
    solid &= rect_mask(rect, canvas.size)
    canvas.mask(solid, colour)
    crown = solid.copy()
    crown[1:] &= ~solid[:-1]
    canvas.mask(crown, edge)


def ember_keep(canvas, rect):
    """Warrior: a burning fortress at dusk, rays behind the helm, and a stone dais."""
    x0, y0, x1, y1 = rect
    cx = (x0 + x1) // 2
    horizon = y1 - 38
    _sky(canvas, (x0, y0, x1, horizon), "ember_sky",
         [(22, 0), (46, 1), (74, 2), (98, 3), (116, 4), (horizon - y0, 5)])
    halo = (cx + 8, y0 + 56)
    _rays(canvas, (x0, y0, x1, y1), halo, "ember_sky", horizon)
    _halo(canvas, (x0, y0, x1, horizon), halo, 47)
    # far wall with two towers, then a nearer and darker one
    _wall(canvas, (x0, y0, x1, horizon + 4), horizon - 20, [(5, 17, horizon - 74), (115, 17, horizon - 88)],
          5, col("ember_sky", 1), col("ember_sky", 4))
    # a few small, dim lit windows; anything brighter competes with the figure
    for wx, wy in ((12, -58), (12, -44), (122, -72), (122, -56)):
        canvas.rect((x0 + wx, horizon + wy, x0 + wx + 2, horizon + wy + 4), col("ember_sky", 5))
        canvas.rect((x0 + wx, horizon + wy + 3, x0 + wx + 2, horizon + wy + 4), col("ember_sky", 4))
    _wall(canvas, (x0, y0, x1, horizon + 4), horizon - 5, [(-4, 18, horizon - 28), (124, 20, horizon - 24)],
          7, col("ember_sky", 0), col("ember_sky", 2))
    _ground(canvas, (x0, horizon, x1, y1), cx)
    _dais(canvas, rect, cx)
    _embers(canvas, rect)


def _ground(canvas, rect, cx):
    x0, y0, x1, y1 = rect
    canvas.rect(rect, col("ember_stone", 1))
    canvas.rect((x0, y0, x1, y0 + 1), col("ember_stone", 3))
    seam = col("ember_stone", 0)
    rows = [y0 + 7, y0 + 17, y0 + 31]
    for y in rows:
        canvas.rect((x0, y, x1, y + 1), seam)
        canvas.rect((x0, y + 1, x1, y + 2), col("ember_stone", 2))
    top = y0 + 1
    for band, bottom in enumerate(rows + [y1]):
        spread = 24 + band * 10
        for k in range(-5, 6):
            joint = cx + k * spread + (spread // 2 if band % 2 else 0)
            if x0 <= joint < x1:
                canvas.rect((joint, top, joint + 1, bottom), seam)
        top = bottom + 2


def _dais(canvas, rect, cx):
    """Low octagonal stone step: a lit top face, a shaded front and the figure's contact shadow."""
    x0, _, x1, y1 = rect
    back, front, foot = y1 - 27, y1 - 7, y1 - 1
    top_face = [(cx - 52, back), (cx + 52, back), (cx + 69, back + 8), (cx + 54, front), (cx - 54, front),
                (cx - 69, back + 8)]
    sides = [
        ([(cx - 69, back + 8), (cx - 54, front), (cx - 54, foot), (cx - 69, foot - 9)], 3),
        ([(cx - 54, front), (cx + 54, front), (cx + 54, foot), (cx - 54, foot)], 2),
        ([(cx + 54, front), (cx + 69, back + 8), (cx + 69, foot - 9), (cx + 54, foot)], 0),
    ]
    shadow = poly_mask([(p[0], p[1] + 2) for p in top_face], canvas.size) & rect_mask(rect, canvas.size)
    canvas.mask(shadow, col("ember_stone", 0))
    for points, step in sides:
        canvas.poly(points, col("ember_stone", step), clip=rect)
    canvas.poly(top_face, col("ember_stone", 4), clip=rect)
    # lit rim along the front edge and a seam in the face
    canvas.rect((cx - 54, front - 1, cx + 54, front), col("ember_stone", 4))
    canvas.rect((cx - 54, front, cx + 54, front + 1), col("ember_stone", 0))
    for x in (cx - 20, cx + 26):
        canvas.rect((x, front + 1, x + 1, foot), col("ember_stone", 0))
        canvas.rect((x + 1, front + 1, x + 2, foot), col("ember_stone", 3))


def contact_shadow(canvas, cx, y, half_width, ramp="ember_stone"):
    points = [(cx - half_width, y), (cx - half_width + 12, y - 4), (cx + half_width - 12, y - 4),
              (cx + half_width, y), (cx + half_width - 12, y + 4), (cx - half_width + 12, y + 4)]
    canvas.poly(points, col(ramp, 0))


def _embers(canvas, rect):
    x0, y0, x1, y1 = rect
    rng = random.Random(7)
    for index in range(26):
        x = rng.randrange(x0 + 4, x1 - 5)
        y = rng.randrange(y0 + 30, y1 - 46)
        if index % 4 == 0:
            canvas.rect((x, y, x + 2, y + 2), col("crimson", 4))
            canvas.dot(x, y, col("gold", 4))
            canvas.rect((x + 1, y + 2, x + 2, y + 4), col("crimson", 2))
        else:
            canvas.rect((x, y, x + 2, y + 1), col("ember_sky", 5))


def dormant(canvas, rect):
    """Placeholder for a class whose art is not painted yet: dim forest with a bow-and-arrow emblem."""
    x0, y0, x1, y1 = rect
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    _sky(canvas, rect, "dusk_forest", [(40, 0), (118, 1), (y1 - y0, 0)])
    _rays(canvas, rect, (cx, cy), "dusk_forest", y1)
    emblem = col("dusk_forest", 3)
    light = col("dusk_forest", 4)
    # bow limbs as two stacked arcs, string and a nocked arrow on the diagonal
    outer = [(cx - 30, cy - 46), (cx - 4, cy - 36), (cx + 18, cy - 14), (cx + 26, cy), (cx + 18, cy + 14),
             (cx - 4, cy + 36), (cx - 30, cy + 46), (cx - 30, cy + 40), (cx - 8, cy + 29), (cx + 10, cy + 11),
             (cx + 16, cy), (cx + 10, cy - 11), (cx - 8, cy - 29), (cx - 30, cy - 40)]
    canvas.poly(outer, emblem)
    canvas.rect((cx - 29, cy - 42, cx - 27, cy + 42), emblem)
    canvas.rect((cx - 46, cy - 2, cx + 40, cy + 2), emblem)
    canvas.poly([(cx + 36, cy - 10), (cx + 54, cy), (cx + 36, cy + 10)], emblem)
    for fx in (cx - 46, cx - 37):
        canvas.poly([(fx - 9, cy - 11), (fx - 1, cy - 11), (fx + 9, cy - 1), (fx + 1, cy - 1)], emblem)
        canvas.poly([(fx + 1, cy + 1), (fx + 9, cy + 1), (fx - 1, cy + 11), (fx - 9, cy + 11)], emblem)
    canvas.rect((cx - 46, cy - 2, cx + 40, cy - 1), light)
    canvas.poly([(cx + 36, cy - 10), (cx + 54, cy), (cx + 36, cy - 7)], light)
