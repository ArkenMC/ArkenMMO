"""The weathered slab behind every skill menu: stone tones, pits, cracks and faint carvings."""
import random

import numpy as np
from scipy.ndimage import zoom

from . import layout
from .draw import Canvas, rect_mask, shift
from .layout import art, cell
from .palette import col
from .treerelief import RELIEFS

SLAB = (8, 34, layout.CANVAS[0] - 8, 214)


def slot_art(slot):
    return art(cell(slot % 9, slot // 9))


def item_origin(slot):
    """Top left of a slot's 16x16 item area in art px."""
    x0, y0, _, _ = slot_art(slot)
    return (x0 + 2, y0 + 2)


def place(mask, at):
    """A tile mask moved onto the page."""
    out = np.zeros((layout.CANVAS[1], layout.CANVAS[0]), bool)
    h, w = mask.shape
    x, y = at
    out[y:y + h, x:x + w] = mask
    return out


def sunk(canvas, mask, floor, wall, lip, clip=None):
    """The one carving rule: shadow inside the top and left wall, light on the lip below and right."""
    if clip is not None:
        mask = mask & rect_mask(clip, canvas.size)
    canvas.mask((shift(mask, 0, 1) | shift(mask, 1, 1)) & ~mask, lip)
    canvas.mask(mask, floor)
    if wall is not None:
        canvas.mask(mask & (~shift(mask, 0, 1) | ~shift(mask, 1, 0)), wall)


def line(canvas, a, b, colour, dy=0):
    steps = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    for i in range(steps + 1):
        t = i / max(1, steps)
        canvas.dot(round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t) + dy, colour)


def _noise(rng, size, step):
    w, h = size
    coarse = rng.random((h // step + 3, w // step + 3))
    return zoom(coarse, step, order=1)[:h, :w]


def slab(canvas, theme, seed=11):
    """Weathered stone in three close tones: lighter in the middle, sinking into dark at the edges."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = SLAB
    w, h = x1 - x0, y1 - y0
    ys, xs = np.mgrid[0:h, 0:w]
    edge = np.hypot((xs - w / 2) / (w / 2), (ys - h * 0.45) / (h * 0.75))
    value = (_noise(rng, (w, h), 22) * 0.55 + _noise(rng, (w, h), 9) * 0.3
             + _noise(rng, (w, h), 3) * 0.15) - (edge - 0.65) * 0.55
    tones = np.select([value < 0.24, value < 0.40, value < 0.66], [0, 1, 2], 3)
    colours = np.array([col("iron", 0), theme.s(0), theme.s(1), theme.s(2)], np.uint8)
    region = Canvas(*canvas.size)
    region.px[y0:y1, x0:x1] = colours[tones]
    # raised patches get a lit upper edge, so the tones read as broken stone rather than clouds
    high = np.zeros(canvas.px.shape[:2], bool)
    high[y0:y1, x0:x1] = tones == 3
    top = high & ~shift(high, 0, 1) & place(rng.random((h, w)) < 0.7, (x0, y0))
    region.mask(top, theme.s(3))
    region.despeckle(1)
    canvas.paste(region)


def pits(canvas, theme, keep_out, seed=5):
    """Sparse clusters of chisel pits, each with its lit lower lip."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = SLAB
    placed = 0
    while placed < 26:
        cx, cy = rng.randrange(x0 + 6, x1 - 8), rng.randrange(y0 + 6, y1 - 8)
        if keep_out[cy - 3:cy + 8, cx - 3:cx + 8].any():
            continue
        placed += 1
        for dx, dy, w in ((0, 0, 3), (4, 3, 2), (1, 5, 2))[:rng.randrange(1, 4)]:
            canvas.rect((cx + dx, cy + dy, cx + dx + w, cy + dy + 2), col("iron", 0))
            canvas.rect((cx + dx, cy + dy + 2, cx + dx + w, cy + dy + 3), theme.s(3))


# hand-routed so no crack runs along or into a groove, and none looks like a connector
CRACKS = (
    ((344, 66), (329, 72), (324, 83), (309, 88), (303, 99), (296, 101)),
    ((324, 83), (327, 96), (321, 106)),
    ((8, 178), (21, 171), (27, 173), (40, 163), (52, 162), (58, 154)),
    ((40, 163), (43, 176), (52, 184), (51, 191)),
    ((231, 34), (238, 44), (252, 49), (256, 60)),
    ((140, 214), (146, 204), (143, 197)),
    ((300, 214), (292, 200), (297, 190), (288, 180)),
    ((8, 96), (16, 101), (18, 112)),
)


def cracks(canvas, theme):
    for path in CRACKS:
        for a, b in zip(path, path[1:]):
            line(canvas, a, b, theme.s(3), 1)
        for a, b in zip(path, path[1:]):
            line(canvas, a, b, col("iron", 0))


# invented stave cuts, two px wide strokes in a 10x10 box; they spell nothing in any script
STAVES = (
    ("XX......XX", "XX....XX..", "XX..XX....", "XXXX......", "XX........", "XXXX......", "XX..XX....",
     "XX....XX..", "XX......XX", "XX........"),
    ("....XX....", "....XX....", "XX..XX....", "..XXXX....", "....XX....", "....XXXX..", "....XX..XX",
     "....XX....", "....XX....", "....XX...."),
    ("XXXXXXXX..", "......XX..", "......XX..", "..XXXXXX..", "..XX......", "..XX......", "..XXXXXXXX",
     "..........", "XXXX..XXXX", ".........."),
    ("XX....XX..", "XX....XX..", ".XX...XX..", "..XX..XX..", "...XX.XX..", "....XXXX..", "......XX..",
     "......XX..", "......XX..", "......XX.."),
)


def _inscription(size, x, top, bottom, order):
    """A vertical band: two rails with worn stave cuts between them."""
    mask = rect_mask((x, top, x + 2, bottom), size) | rect_mask((x + 16, top, x + 18, bottom), size)
    y, i = top + 4, 0
    while y + 10 <= bottom - 2:
        for dy, row in enumerate(STAVES[order[i % len(order)]]):
            for dx, ch in enumerate(row):
                if ch == "X":
                    mask[y + dy, x + 4 + dx] = True
        y += 15
        i += 1
    return mask


def _wear_away(mask, seed, share):
    """Break pieces out of a carving, so it reads as ancient and never as a button."""
    rng = np.random.default_rng(seed)
    h, w = mask.shape
    return mask & ~(_noise(rng, (w, h), 7) < share + 0.14)


def carvings(canvas, theme, keep_out):
    """Within about one ramp step of the slab: found when looked for, gone at a glance."""
    size = canvas.size
    relief_of, hollows_of, margins_of, trace = RELIEFS[theme.class_id]
    relief = _wear_away(relief_of(size), 3, 0.08)
    bands = _inscription(size, 18, 92, 206, (0, 1, 2, 3, 1, 0)) | _inscription(size, 316, 44, 206, (2, 3, 0, 1))
    clear = ~keep_out
    for mask in (relief, _wear_away(margins_of(size), 8, 0.07), _wear_away(bands, 21, 0.10)):
        sunk(canvas, mask & clear, theme.s(0), col("iron", 0), theme.s(3))
    # a last trace of old pigment, lying in the deepest cuts of the class carving
    ys, xs = np.mgrid[0:size[1], 0:size[0]]
    hollows = hollows_of(size)
    sunk(canvas, hollows & clear, col("iron", 0), None, theme.s(3))
    shown = relief | hollows
    traces = shown & clear & (((xs * 3 + ys * 5) // 11) % 5 == 0) & ((xs + ys) % 2 == 0)
    canvas.mask(traces & shift(shown, 0, 1), col(*trace))
