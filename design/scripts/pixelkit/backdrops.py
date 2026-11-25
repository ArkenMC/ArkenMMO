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
    x0, y0, x1, _ = rect
    mask = np.zeros(canvas.px.shape[:2], bool)
    for start in range(-180, 180, 30):
        a, b = np.radians((start, start + 11))
        mask |= poly_mask([centre, (centre[0] + 260 * np.cos(a), centre[1] + 260 * np.sin(a)),
                           (centre[0] + 260 * np.cos(b), centre[1] + 260 * np.sin(b))], canvas.size)
    mask &= rect_mask((x0, y0, x1, limit), canvas.size)
    _lift(canvas, mask, ramp)


def _halo(canvas, rect, centre, radius, ramp):
    """A disc behind the head: it frames the face, the focal point."""
    # measured from 6 px block centres, so the circle is stair-stepped like a block build
    ys, xs = np.mgrid[0:canvas.size[1], 0:canvas.size[0]] // 6 * 6 + 3
    distance = np.hypot(xs - centre[0], ys - centre[1])
    inside = rect_mask(rect, canvas.size)
    _lift(canvas, inside & (distance < radius), ramp)


def _clouds(canvas, rect, ramp, clouds):
    """Flat blocky clouds given as (x, y, [(dx, dy, w, h)]), one ramp step above the sky behind them."""
    mask = np.zeros(canvas.px.shape[:2], bool)
    for x, y, blocks in clouds:
        for dx, dy, w, h in blocks:
            left, top = rect[0] + x + dx, rect[1] + y + dy
            mask |= rect_mask((left, top, left + w, top + h), canvas.size)
    _lift(canvas, mask & rect_mask(rect, canvas.size), ramp)


def _bricks(canvas, mask, colour, course=7, length=12):
    """Mortar lines of a staggered stone-brick bond, drawn only inside `mask`."""
    ys, xs = np.mgrid[0:canvas.size[1], 0:canvas.size[0]]
    stagger = (ys // course) % 2 * (length // 2)
    canvas.mask(mask & ((ys % course == 0) | ((xs + stagger) % length == 0)), colour)


def _crest_line(canvas, solid, colour):
    crown = solid.copy()
    crown[1:] &= ~solid[:-1]
    canvas.mask(crown, colour)


def _wall(canvas, rect, base_y, towers, merlon, colour, edge, mortar):
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
    solid = (shape.px[..., 3] > 0) & rect_mask(rect, canvas.size)
    canvas.mask(solid, colour)
    _bricks(canvas, solid, mortar)
    _crest_line(canvas, solid, edge)


def ember_keep(canvas, rect):
    """Warrior: a burning stone-brick fortress at dusk, rays behind the helm, and a stone dais."""
    x0, y0, x1, y1 = rect
    cx = (x0 + x1) // 2
    horizon = y1 - 38
    _sky(canvas, (x0, y0, x1, horizon), "ember_sky",
         [(22, 0), (46, 1), (74, 2), (98, 3), (116, 4), (horizon - y0, 5)])
    halo = (cx + 8, y0 + 56)
    _rays(canvas, rect, halo, "ember_sky", horizon)
    _halo(canvas, (x0, y0, x1, horizon), halo, 47, "ember_sky")
    _clouds(canvas, (x0, y0, x1, horizon), "ember_sky",
            [(0, 34, [(0, 6, 30, 6), (6, 0, 18, 6)]), (106, 18, [(0, 6, 36, 6), (12, 0, 18, 6)])])
    # far wall with two towers, then a nearer and darker one
    _wall(canvas, (x0, y0, x1, horizon + 4), horizon - 20, [(5, 17, horizon - 74), (115, 17, horizon - 88)],
          6, col("ember_sky", 1), col("ember_sky", 4), col("ember_sky", 2))
    # a few small, dim lit windows; anything brighter competes with the figure
    for wx, wy in ((12, -58), (12, -44), (122, -72), (122, -56)):
        canvas.rect((x0 + wx, horizon + wy, x0 + wx + 4, horizon + wy + 4), col("ember_sky", 5))
    _wall(canvas, (x0, y0, x1, horizon + 4), horizon - 5, [(-4, 18, horizon - 28), (124, 20, horizon - 24)],
          7, col("ember_sky", 0), col("ember_sky", 2), col("ember_sky", 1))
    _ground(canvas, (x0, horizon, x1, y1), cx, "ember_stone")
    _dais(canvas, rect, cx, "ember_stone")
    _sparks(canvas, rect, 7, 26, hot=(("crimson", 4), ("gold", 4)), faint=("ember_sky", 5))


def _ground(canvas, rect, cx, ramp):
    x0, y0, x1, y1 = rect
    canvas.rect(rect, col(ramp, 1))
    canvas.rect((x0, y0, x1, y0 + 1), col(ramp, 3))
    seam = col(ramp, 0)
    rows = [y0 + 7, y0 + 17, y0 + 31]
    for y in rows:
        canvas.rect((x0, y, x1, y + 1), seam)
        canvas.rect((x0, y + 1, x1, y + 2), col(ramp, 2))
    top = y0 + 1
    for band, bottom in enumerate(rows + [y1]):
        spread = 24 + band * 10
        for k in range(-5, 6):
            joint = cx + k * spread + (spread // 2 if band % 2 else 0)
            if x0 <= joint < x1:
                canvas.rect((joint, top, joint + 1, bottom), seam)
        top = bottom + 2


def _dais(canvas, rect, cx, ramp):
    """Low octagonal step of stone blocks: a lit top face and a shaded front."""
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
    canvas.mask(shadow, col(ramp, 0))
    for points, step in sides:
        canvas.poly(points, col(ramp, step), clip=rect)
    canvas.poly(top_face, col(ramp, 4), clip=rect)
    # block joints across the top face
    top = poly_mask(top_face, canvas.size) & rect_mask(rect, canvas.size)
    middle = (back + front) // 2 - 2
    canvas.mask(top & rect_mask((x0, middle, x1, middle + 1), canvas.size), col(ramp, 2))
    for row, offset in ((back, 0), (middle + 1, 12)):
        for x in range(cx - 60 + offset, cx + 61, 24):
            canvas.mask(top & rect_mask((x, row, x + 1, row + middle - back), canvas.size), col(ramp, 2))
    # lit rim along the front edge and block joints in the face
    canvas.rect((cx - 54, front - 1, cx + 54, front), col(ramp, 4))
    canvas.rect((cx - 54, front, cx + 54, front + 1), col(ramp, 0))
    for x in (cx - 36, cx - 18, cx, cx + 18, cx + 36):
        canvas.rect((x, front + 1, x + 1, foot), col(ramp, 0))
        canvas.rect((x + 1, front + 1, x + 2, foot), col(ramp, 3))


def contact_shadow(canvas, cx, y, half_width, ramp):
    points = [(cx - half_width, y), (cx - half_width + 12, y - 4), (cx + half_width - 12, y - 4),
              (cx + half_width, y), (cx + half_width - 12, y + 4), (cx - half_width + 12, y + 4)]
    canvas.poly(points, col(ramp, 0))


def _sparks(canvas, rect, seed, count, hot, faint):
    """Square motes: every fourth is a 4 px block with a hot 2 px corner."""
    x0, y0, x1, y1 = rect
    rng = random.Random(seed)
    for index in range(count):
        x = rng.randrange(x0 + 4, x1 - 6)
        y = rng.randrange(y0 + 30, y1 - 46)
        if index % 4 == 0:
            canvas.rect((x, y, x + 4, y + 4), col(*hot[0]))
            canvas.rect((x, y, x + 2, y + 2), col(*hot[1]))
        else:
            canvas.rect((x, y, x + 2, y + 2), col(*faint))


def _silhouette(canvas, rect, blocks, colour, edge, mortar=None):
    """A layer built from rectangles given relative to the panel's left edge and the horizon."""
    x0, _, _, horizon = rect
    solid = np.zeros(canvas.px.shape[:2], bool)
    for x, up, width, height in blocks:
        solid |= rect_mask((x0 + x, horizon - up, x0 + x + width, horizon - up + height), canvas.size)
    solid &= rect_mask((rect[0], rect[1], rect[2], horizon + 4), canvas.size)
    canvas.mask(solid, colour)
    if mortar:
        _bricks(canvas, solid, mortar, 8, 8)
    _crest_line(canvas, solid, edge)


def _tree(x, height, crown):
    """A block tree: a trunk under three stacked leaf slabs."""
    half = crown // 2
    return [(x - 3, height - 6, 6, height + 4),
            (x - half, height - 2, crown, 14),
            (x - half + 5, height + 8, crown - 10, 10),
            (x - 5, height + 16, 10, 8)]


def _scene(canvas, rect, sky, bands, halo_offset, clouds=()):
    """Sky, rays, halo and clouds; returns the interior's centre and horizon."""
    x0, y0, x1, y1 = rect
    cx = (x0 + x1) // 2
    horizon = y1 - 38
    _sky(canvas, (x0, y0, x1, horizon), sky, bands + [(horizon - y0, len(bands))])
    halo = (cx + halo_offset, y0 + 56)
    _rays(canvas, rect, halo, sky, horizon)
    _halo(canvas, (x0, y0, x1, horizon), halo, 47, sky)
    _clouds(canvas, (x0, y0, x1, horizon), sky, clouds)
    return cx, horizon


def twilight_woods(canvas, rect):
    """Archer: block trees against an indigo dusk with an amber horizon, and a slate dais."""
    x0, y0, x1, y1 = rect
    cx, horizon = _scene(canvas, rect, "dusk_sky", [(22, 0), (46, 1), (74, 2), (98, 3), (116, 4)], -8,
                         [(2, 20, [(0, 6, 24, 6), (6, 0, 12, 6)]), (104, 40, [(0, 6, 34, 6), (12, 0, 18, 6)])])
    layer = (x0, y0, x1, horizon)
    far = [(0, 22, 136, 30)]
    for x, height, crown in ((12, 52, 26), (38, 38, 22), (96, 36, 24), (124, 62, 30)):
        far += _tree(x, height, crown)
    _silhouette(canvas, layer, far, col("dusk_sky", 1), col("dusk_sky", 4))
    near = [(0, 6, 136, 14)]
    for x, height, crown in ((2, 58, 30), (24, 18, 20), (112, 16, 22), (136, 38, 28)):
        near += _tree(x, height, crown)
    _silhouette(canvas, layer, near, col("dusk_forest", 0), col("dusk_forest", 2))
    # slate stone, so the green and leather figure stands off the floor in both hue and value
    _ground(canvas, (x0, horizon, x1, y1), cx, "dusk_sky")
    _dais(canvas, rect, cx, "dusk_sky")
    _sparks(canvas, rect, 5, 20, hot=(("gold", 3), ("gold", 5)), faint=("dusk_sky", 5))


def star_sanctum(canvas, rect):
    """Mage: a night sky with floating block islands, rune pillars and a rune circle on the dais."""
    x0, y0, x1, y1 = rect
    cx, horizon = _scene(canvas, rect, "night_teal", [(22, 0), (46, 1), (74, 2), (98, 3), (116, 4)], 4)
    layer = (x0, y0, x1, horizon)
    islands = [(4, 104, 28, 6), (8, 98, 20, 6), (12, 92, 12, 6), (14, 86, 6, 6),
               (106, 92, 28, 6), (110, 86, 20, 6), (116, 80, 10, 6)]
    far = [(0, 18, 136, 26), (8, 54, 14, 40), (6, 60, 18, 6), (108, 66, 16, 52), (106, 72, 20, 6),
           (30, 30, 10, 14), (94, 38, 10, 22)]
    _silhouette(canvas, layer, islands + far, col("night_teal", 1), col("night_teal", 4))
    near = [(0, 6, 136, 14), (-4, 30, 20, 26), (-4, 36, 10, 6), (122, 24, 20, 20), (132, 34, 10, 10)]
    _silhouette(canvas, layer, near, col("night_teal", 0), col("night_teal", 2), col("night_teal", 1))
    for x, up in ((14, 46), (14, 32), (115, 58), (115, 42)):
        canvas.rect((x0 + x, horizon - up, x0 + x + 2, horizon - up + 6), col("arcane", 1))
        canvas.rect((x0 + x - 2, horizon - up + 2, x0 + x + 4, horizon - up + 4), col("arcane", 1))
    for x, y in ((8, 10), (34, 20), (126, 8), (100, 24), (20, 62), (118, 68), (60, 6), (90, 8), (46, 46)):
        canvas.rect((x0 + x, y0 + y, x0 + x + 2, y0 + y + 2), col("night_teal", 5))
    _ground(canvas, (x0, horizon, x1, y1), cx, "night_teal")
    _dais(canvas, rect, cx, "night_teal")
    for dx, dy in ((-50, -19), (-34, -13), (-12, -11), (12, -11), (34, -13), (50, -19)):
        canvas.rect((cx + dx - 3, y1 + dy, cx + dx + 3, y1 + dy + 2), col("arcane", 1))
    _sparks(canvas, rect, 23, 16, hot=(("arcane", 1), ("arcane", 3)), faint=("night_teal", 5))


def dawn_camp(canvas, rect):
    """Captain: sunrise behind block hills and the tents of his company."""
    x0, y0, x1, y1 = rect
    cx, horizon = _scene(canvas, rect, "dawn_sky", [(22, 0), (46, 1), (74, 2), (98, 3), (116, 4)], 8,
                         [(0, 76, [(0, 6, 28, 6), (6, 0, 14, 6)]), (110, 26, [(0, 6, 30, 6), (8, 0, 16, 6)])])
    layer = (x0, y0, x1, horizon)
    hills = [(0, 40, 22, 48), (22, 32, 14, 40), (36, 22, 20, 30), (56, 16, 30, 24), (86, 26, 14, 34),
             (100, 38, 14, 46), (114, 50, 22, 58)]
    _silhouette(canvas, layer, hills, col("dawn_sky", 2), col("dawn_sky", 5))
    camp = [(0, 6, 136, 14)]
    for left in (-6, 106):
        # a stepped tent with a pole and pennant
        camp += [(left, 14, 40, 10), (left + 5, 21, 30, 7), (left + 10, 28, 20, 7), (left + 15, 35, 10, 7),
                 (left + 19, 52, 2, 18), (left + 21, 52, 11, 4), (left + 21, 48, 6, 3)]
    _silhouette(canvas, layer, camp, col("dawn_sky", 0), col("dawn_sky", 3))
    for left in (14, 126):
        canvas.rect((x0 + left, horizon - 10, x0 + left + 4, horizon), col("dawn_sky", 3))
    _ground(canvas, (x0, horizon, x1, y1), cx, "dawn_stone")
    _dais(canvas, rect, cx, "dawn_stone")
    _sparks(canvas, rect, 31, 16, hot=(("gold", 3), ("gold", 5)), faint=("dawn_sky", 5))
