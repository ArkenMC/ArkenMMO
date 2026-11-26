"""Skill tree item textures (32x32): node states, lit connectors and the reset button."""
import numpy as np

from .draw import Canvas, dilate, poly_mask, shift
from .palette import col
from .treeicons import ICONS

TILE = 32
ICON_AT = 4
STATES = ("locked", "available", "confirm", "owned")
# lit pieces stop short of the tile edge so the painted clamp across the slot gap shows whole
CLAMP_REACH = 2


def _chamfered(inset, cut):
    """A square tile mask `inset` px in, with 45 degree corners `cut` px long."""
    ys, xs = np.mgrid[0:TILE, 0:TILE]
    lo, hi = inset, TILE - 1 - inset
    inside = (xs >= lo) & (xs <= hi) & (ys >= lo) & (ys <= hi)
    for cx in (xs - lo, hi - xs):
        for cy in (ys - lo, hi - ys):
            inside &= cx + cy >= cut
    return inside


def shape(kind, inset=0):
    """Actives (and the core) are near squares; passives are octagons."""
    cut = 9 if kind == "passive" else 3
    return _chamfered(inset, max(0, cut - inset // 2))


def _lit_side(mask):
    """Pixels of `mask` whose upper or left neighbour is outside it."""
    return mask & (~shift(mask, 0, 1) | ~shift(mask, 1, 0))


def _bevel(canvas, kind, inset, top, bottom):
    ring = shape(kind, inset) & ~shape(kind, inset + 1)
    ys, xs = np.mgrid[0:TILE, 0:TILE]
    canvas.mask(ring & (xs + ys < TILE - 1), top)
    canvas.mask(ring & (xs + ys >= TILE - 1), bottom)


def icon_mask(name):
    mask = np.zeros((TILE, TILE), bool)
    icon = ICONS[name]
    mask[ICON_AT:ICON_AT + icon.shape[0], ICON_AT:ICON_AT + icon.shape[1]] = icon
    return mask


def _carve(canvas, mask, floor, wall, lip, plate):
    """A sunken cut lit from the top left: shadow inside the upper wall, a lit lip below and right."""
    outer_lip = (shift(mask, 1, 1) | shift(mask, 0, 1)) & ~mask & plate
    canvas.mask(outer_lip, lip)
    canvas.mask(mask, floor)
    canvas.mask(mask & ~shift(mask, 0, 1), wall)


# weathering on the plate, kept to a few clusters clear of the sigil's middle
WEAR = ((6, 24, 3, 1), (23, 5, 2, 2), (8, 6, 2, 1), (24, 23, 1, 3))


def _wear(canvas, area, colour):
    for x, y, w, h in WEAR:
        patch = np.zeros_like(area)
        patch[y:y + h, x:x + w] = True
        canvas.mask(patch & area, colour)


def _corner_brackets(canvas):
    """Gold L-shaped marks, 2 px thick: the shape that says "click again"."""
    for fx in (False, True):
        for fy in (False, True):
            mark = np.zeros((TILE, TILE), bool)
            mark[0:3, 0:10] = True
            mark[0:10, 0:3] = True
            mark = mark[::-1 if fy else 1, ::-1 if fx else 1]
            canvas.mask(dilate(mark), col("iron", 0))
            canvas.mask(mark, col("gold", 4))
            canvas.mask(mark & ~shift(mark, 0, 1), col("gold", 5))
            canvas.mask(mark & ~shift(mark, 0, -1), col("gold", 2))


def _studs(canvas, kind):
    """Four small ember rivets on the ring of an owned stone: a second, non-colour cue."""
    if kind == "passive":
        spots = ((15, 1), (15, 29), (1, 15), (29, 15))
    else:
        spots = ((2, 2), (28, 2), (2, 28), (28, 28))
    for x, y in spots:
        canvas.rect((x - 1, y - 1, x + 3, y + 3), col("iron", 0))
        canvas.rect((x, y, x + 2, y + 2), col("crimson", 4))
        canvas.dot(x, y, col("crimson", 5))


def node(name, kind, state):
    """`kind` is "active", "passive" or "core"."""
    canvas = Canvas(TILE, TILE)
    outline = col("iron", 0)
    canvas.mask(shape(kind), outline)
    mask = icon_mask(name)
    if state == "locked":
        plate = shape(kind, 2)
        _bevel(canvas, kind, 1, col("ember_stone", 3), col("ember_stone", 0))
        canvas.mask(plate, col("ember_stone", 1))
        _wear(canvas, plate & ~dilate(mask), col("ember_stone", 0))
        _carve(canvas, mask, col("iron", 0), col("iron", 0), col("ember_stone", 4), plate)
        # a trace of grit along the floor keeps the dull rune readable
        canvas.mask(mask & shift(mask, 0, 1) & shift(mask, 1, 0), col("steel", 2))
    elif state in ("available", "confirm"):
        _bevel(canvas, kind, 1, col("steel", 4), col("steel", 2))
        _bevel(canvas, kind, 2, col("steel", 3), col("steel", 2))
        canvas.mask(shape(kind, 3), outline)
        plate = shape(kind, 4)
        canvas.mask(plate, col("ember_stone", 2))
        _wear(canvas, plate & ~dilate(mask), col("ember_stone", 1))
        floor, wall = ((col("steel", 3), col("steel", 2)) if state == "available"
                       else (col("steel", 6), col("steel", 5)))
        canvas.mask(dilate(mask) & ~mask & shape(kind, 3), col("iron", 0))
        _carve(canvas, mask, floor, wall, col("ember_stone", 4), plate)
        if state == "confirm":
            _corner_brackets(canvas)
    elif state == "owned":
        _bevel(canvas, kind, 1, col("crimson", 3), col("crimson", 2))
        _bevel(canvas, kind, 2, col("crimson", 2), col("crimson", 2))
        _bevel(canvas, kind, 3, col("crimson", 1), col("crimson", 1))
        plate = shape(kind, 4)
        canvas.mask(plate, col("crimson", 0))
        # still glow: one solid step around the cut, then a checker fringe
        near = dilate(mask)
        far = dilate(dilate(near))
        ys, xs = np.mgrid[0:TILE, 0:TILE]
        canvas.mask(far & plate & ((xs + ys) % 2 == 0), col("crimson", 1))
        canvas.mask(near & shape(kind, 3), col("crimson", 1))
        canvas.mask(mask, col("crimson", 4))
        heart = mask & shift(mask, 0, 1) & shift(mask, 0, -1) & shift(mask, 1, 0) & shift(mask, -1, 0)
        canvas.mask(heart, col("crimson", 5))
        canvas.mask(mask & ~shift(mask, 0, 1), col("crimson", 3))
        _studs(canvas, kind)
    else:
        raise ValueError(state)
    if kind == "core":
        for x, y in ((14, 1), (14, 29)):
            canvas.rect((x, y, x + 4, y + 2), col("gold", 3))
            canvas.rect((x, y, x + 4, y + 1), col("gold", 4))
    return canvas.image()


# --- connectors -------------------------------------------------------------------------------

BAND = (12, 20)


def channel(kind, x0=0, x1=TILE):
    """Boolean tile mask of the 8 px groove for a piece; corners are cut at 45 degrees."""
    lo, hi = BAND
    if kind == "h":
        mask = np.zeros((TILE, TILE), bool)
        mask[lo:hi, x0:x1] = True
        return mask
    if kind == "v":
        mask = np.zeros((TILE, TILE), bool)
        mask[x0:x1, lo:hi] = True
        return mask
    if kind == "corner_es":
        points = [(32, 12), (32, 20), (23, 20), (20, 23), (20, 32), (12, 32), (12, 18), (18, 12)]
        return poly_mask(points, (TILE, TILE))
    if kind == "corner_sw":
        return channel("corner_es")[:, ::-1]
    raise ValueError(kind)


def _depth(mask):
    """How many px each pixel is from the groove wall, ignoring the open tile edges."""
    padded = np.pad(mask, 4, mode="edge")
    depth = np.zeros(padded.shape, int)
    inner = padded.copy()
    for _ in range(4):
        depth += inner
        inner = inner & shift(inner, 0, 1) & shift(inner, 0, -1) & shift(inner, 1, 0) & shift(inner, -1, 0)
    return depth[4:-4, 4:-4]


def link(kind):
    canvas = Canvas(TILE, TILE)
    mask = channel(kind)
    depth = _depth(mask)
    # one step quieter than an owned stone: light lying in the cut, not a neon bar
    canvas.mask(mask & (depth == 1), col("crimson", 0))
    canvas.mask(mask & (depth == 2), col("crimson", 1))
    canvas.mask(mask & (depth >= 3), col("crimson", 2))
    ys, xs = np.mgrid[0:TILE, 0:TILE]
    # still, uneven pools of brighter pigment in the floor of the cut
    pools = ((xs + ys) % 16) < 7
    canvas.mask(mask & (depth >= 4) & pools, col("crimson", 3))
    ends = {"h": "we", "v": "ns", "corner_es": "es", "corner_sw": "sw"}[kind]
    if "w" in ends:
        canvas.px[:, :CLAMP_REACH] = 0
    if "e" in ends:
        canvas.px[:, TILE - CLAMP_REACH:] = 0
    if "n" in ends:
        canvas.px[:CLAMP_REACH, :] = 0
    if "s" in ends:
        canvas.px[TILE - CLAMP_REACH:, :] = 0
    return canvas.image()


# --- reset ------------------------------------------------------------------------------------

def _returning_arrow():
    """One broken ring that comes back on itself, with a head at its end."""
    ys, xs = np.mgrid[0:TILE, 0:TILE] + 0.5
    radius = np.hypot(xs - 16, ys - 17)
    angle = np.degrees(np.arctan2(ys - 17, xs - 16)) % 360
    ring = (radius <= 10) & (radius >= 6) & ~((angle > 195) & (angle < 285))
    head = poly_mask([(17, 3), (17, 17), (9, 10)], (TILE, TILE))
    return ring | head


def reset(state):
    """`state` is "ready", "confirm" or "unavailable"."""
    canvas = Canvas(TILE, TILE)
    disc = _chamfered(0, 10)
    canvas.mask(disc, col("iron", 0))
    rim, rim_dark, plate = {"ready": (("gold", 2), ("gold", 1), ("iron", 2)),
                            "confirm": (("gold", 4), ("gold", 2), ("leather", 0)),
                            "unavailable": (("iron", 3), ("iron", 2), ("iron", 1))}[state]
    for inset in (1, 2):
        ring = _chamfered(inset, 10 - inset // 2) & ~_chamfered(inset + 1, 9 - inset // 2)
        ys, xs = np.mgrid[0:TILE, 0:TILE]
        canvas.mask(ring & (xs + ys < TILE - 1), col(*rim))
        canvas.mask(ring & (xs + ys >= TILE - 1), col(*rim_dark))
    face = _chamfered(4, 7)
    canvas.mask(face, col(*plate))
    arrow = _returning_arrow()
    if state == "unavailable":
        _carve(canvas, arrow, col("iron", 0), col("iron", 0), col("iron", 4), face)
        canvas.mask(arrow & shift(arrow, 0, 1) & shift(arrow, 1, 0), col("steel", 1))
        # a dead stone: a crack across the face, a shape cue besides the dimming
        for i in range(20):
            x, y = 6 + i, 24 - i * 3 // 4 - (1 if 7 < i < 13 else 0)
            canvas.rect((x, y, x + 1, y + 2), col("iron", 0))
    else:
        ink, top = (("steel", 5), ("steel", 6)) if state == "ready" else (("gold", 4), ("gold", 5))
        backing = dilate(arrow)
        canvas.mask(backing | shift(backing, 0, 1), col("iron", 0))
        canvas.mask(arrow, col(*ink))
        canvas.mask(arrow & ~shift(arrow, 0, 1), col(*top))
        canvas.mask(arrow & ~shift(arrow, 0, -1), col("steel", 3) if state == "ready" else col("gold", 2))
    if state == "confirm":
        _corner_brackets(canvas)
    return canvas.image()
