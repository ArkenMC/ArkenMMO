"""The painted part of a skill tree page: slab, faint carvings, grooves, sockets, seals and footer.

Layout and frame are shared by every class; a class only changes the backdrop carving and accent.
"""
import random

import numpy as np
from scipy.ndimage import zoom

from . import chrome, layout, lettering
from .draw import Canvas, dilate, frame, poly_mask, rect_mask, shift
from .layout import art, cell
from .palette import col
from .treeicons import ICONS
from .treenodes import channel, shape

SLAB = (8, 34, layout.CANVAS[0] - 8, 214)
FOOTER = (8, 214, layout.CANVAS[0] - 8, 250)

# slot -> (kind, name) and slot -> connector shape, per view
VIEWS = {
    "a": {
        "nodes": {4: ("active", "n1"), 20: ("passive", "n2"), 24: ("passive", "n3"),
                  38: ("active", "n4"), 40: ("passive", "n5"), 42: ("active", "n6"), 0: ("core", "core")},
        "links": {2: "corner_es", 3: "h", 5: "h", 6: "corner_sw", 11: "v", 15: "v",
                  29: "v", 33: "v", 39: "h", 41: "h"},
        "sealed_nodes": (),
        "sealed_links": {},
    },
    "b": {
        "nodes": {2: ("active", "n4"), 4: ("passive", "n5"), 6: ("active", "n6")},
        "links": {3: "h", 5: "h"},
        "sealed_nodes": (20, 24, 40),
        "sealed_links": {11: "v", 15: "v", 29: "v", 33: "v", 38: "corner_ne", 39: "h", 41: "h", 42: "corner_nw"},
    },
}
EDGES_A = {"n1-n2": (2, 3, 11), "n1-n3": (5, 6, 15), "n2-n4": (29,), "n3-n6": (33,),
           "n4-n5": (39,), "n5-n6": (41,)}


def slot_art(slot):
    return art(cell(slot % 9, slot // 9))


def item_origin(slot):
    """Top left of a slot's 16x16 item area in art px."""
    x0, y0, _, _ = slot_art(slot)
    return (x0 + 2, y0 + 2)


def _place(mask, at):
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


# --- the slab ---------------------------------------------------------------------------------

def _noise(rng, size, step):
    w, h = size
    coarse = rng.random((h // step + 3, w // step + 3))
    return zoom(coarse, step, order=1)[:h, :w]


def slab(canvas, seed=11):
    """Weathered stone in three close tones: lighter in the middle, sinking into dark at the edges."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = SLAB
    w, h = x1 - x0, y1 - y0
    ys, xs = np.mgrid[0:h, 0:w]
    edge = np.hypot((xs - w / 2) / (w / 2), (ys - h * 0.45) / (h * 0.75))
    value = (_noise(rng, (w, h), 22) * 0.55 + _noise(rng, (w, h), 9) * 0.3
             + _noise(rng, (w, h), 3) * 0.15) - (edge - 0.65) * 0.55
    tones = np.select([value < 0.24, value < 0.40, value < 0.66], [0, 1, 2], 3)
    colours = np.array([col("iron", 0), col("ember_stone", 0), col("ember_stone", 1), col("ember_stone", 2)],
                       np.uint8)
    region = Canvas(*canvas.size)
    region.px[y0:y1, x0:x1] = colours[tones]
    # raised patches get a lit upper edge, so the tones read as broken stone rather than clouds
    high = np.zeros(canvas.px.shape[:2], bool)
    high[y0:y1, x0:x1] = tones == 3
    top = high & ~shift(high, 0, 1) & (_place(rng.random((h, w)) < 0.7, (x0, y0)))
    region.mask(top, col("ember_stone", 3))
    region.despeckle(1)
    canvas.paste(region)


def pits(canvas, keep_out, seed=5):
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
            canvas.rect((cx + dx, cy + dy + 2, cx + dx + w, cy + dy + 3), col("ember_stone", 3))


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


def _line(canvas, a, b, colour, dy=0):
    steps = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    for i in range(steps + 1):
        t = i / max(1, steps)
        canvas.dot(round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t) + dy, colour)


def cracks(canvas):
    for path in CRACKS:
        for a, b in zip(path, path[1:]):
            _line(canvas, a, b, col("ember_stone", 3), 1)
        for a, b in zip(path, path[1:]):
            _line(canvas, a, b, col("iron", 0))


# --- faint carvings (Warrior) -----------------------------------------------------------------

def _mirror(points, axis=176):
    return [(2 * axis - x, y) for x, y in points]


def _warrior_relief(size):
    """The class carving behind the tree: a great nasal helm over two crossed war axes, half worn away."""
    def polygon(points):
        return poly_mask(points, size)

    helm = polygon([(176, 76), (190, 79), (201, 88), (208, 101), (210, 116), (142, 116), (144, 101),
                    (151, 88), (162, 79)])
    brow = polygon([(140, 119), (212, 119), (212, 127), (140, 127)])
    cheeks = polygon([(142, 130), (160, 130), (163, 150), (170, 168), (156, 164), (146, 150)])
    cheeks |= polygon(_mirror([(142, 130), (160, 130), (163, 150), (170, 168), (156, 164), (146, 150)]))
    nasal = polygon([(171, 130), (181, 130), (180, 156), (176, 161), (172, 156)])
    ridge = polygon([(173, 80), (179, 80), (179, 116), (173, 116)])
    helm_all = (helm & ~ridge) | brow | cheeks | nasal
    haft = polygon([(120, 187), (126, 193), (232, 87), (226, 81)])
    haft = haft | haft[:, ::-1]
    blade = [(222, 62), (241, 66), (252, 77), (256, 96), (244, 90), (236, 90), (232, 84), (226, 78),
             (226, 72)]
    axes = haft | polygon(blade) | polygon(_mirror(blade))
    axes &= ~dilate(dilate(dilate(helm_all)))
    return helm_all | axes


def _stone_sword(size, cx, top, bottom):
    """A tall grave-marker sword cut into each margin, point down."""
    parts = [
        [(cx - 3, top), (cx + 3, top), (cx + 5, top + 6), (cx - 5, top + 6)],
        [(cx - 2, top + 6), (cx + 2, top + 6), (cx + 2, top + 22), (cx - 2, top + 22)],
        [(cx - 13, top + 22), (cx + 13, top + 22), (cx + 13, top + 28), (cx - 13, top + 28)],
        [(cx - 6, top + 30), (cx + 6, top + 30), (cx + 5, bottom - 16), (cx, bottom), (cx - 5, bottom - 16)],
    ]
    mask = np.zeros((size[1], size[0]), bool)
    for points in parts:
        mask |= poly_mask(points, size)
    fuller = rect_mask((cx - 1, top + 34, cx + 1, bottom - 24), size)
    return mask & ~fuller


# invented stave cuts, three px wide strokes in a 10x10 box; they spell nothing in any script
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
        rows = STAVES[order[i % len(order)]]
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch == "X":
                    mask[y + dy, x + 4 + dx] = True
        y += 15
        i += 1
    return mask


def _wear_away(mask, seed, share=0.16):
    """Break pieces out of a carving, so it reads as ancient and never as a button."""
    rng = np.random.default_rng(seed)
    h, w = mask.shape
    lost = _noise(rng, (w, h), 7) < share + 0.14
    return mask & ~lost


def carvings(canvas, keep_out):
    """Within about one ramp step of the slab: found when looked for, gone at a glance."""
    size = canvas.size
    relief = _wear_away(_warrior_relief(size), 3, 0.08)
    swords = _stone_sword(size, 68, 80, 206) | _stone_sword(size, 284, 80, 206)
    bands = _inscription(size, 18, 92, 206, (0, 1, 2, 3, 1, 0)) | _inscription(size, 316, 44, 206, (2, 3, 0, 1))
    clear = ~keep_out
    for mask in (relief, _wear_away(swords, 8, 0.07), _wear_away(bands, 21, 0.10)):
        sunk(canvas, mask & clear, col("ember_stone", 0), col("iron", 0), col("ember_stone", 3))
    # a last trace of old red pigment, lying in the deepest cuts of the class carving
    ys, xs = np.mgrid[0:size[1], 0:size[0]]
    eyes = poly_mask([(148, 131), (169, 131), (166, 139), (152, 139)], size)
    eyes |= eyes[:, ::-1]
    sunk(canvas, eyes & clear, col("iron", 0), None, col("ember_stone", 3))
    traces = (relief | eyes) & clear & (((xs * 3 + ys * 5) // 11) % 5 == 0) & ((xs + ys) % 2 == 0)
    canvas.mask(traces & shift(relief | eyes, 0, 1), col("crimson", 0))


# --- grooves, clamps, sockets -----------------------------------------------------------------

def _piece_mask(kind, slot):
    """A connector groove stretched across the whole 36 px cell."""
    if kind == "corner_ne":
        base = channel("corner_es")[::-1, :]
    elif kind == "corner_nw":
        base = channel("corner_es")[::-1, ::-1]
    else:
        base = channel(kind)
    wide = np.pad(base, 2, mode="edge")
    return _place(wide, slot_art(slot)[:2])


def groove_mask(view):
    mask = np.zeros((layout.CANVAS[1], layout.CANVAS[0]), bool)
    for slot, kind in {**view["links"], **view["sealed_links"]}.items():
        mask |= _piece_mask(kind, slot)
    return mask


def _runs(view):
    """Groove stubs from each linked node toward its neighbours, so no channel stops short of a stone."""
    out = np.zeros((layout.CANVAS[1], layout.CANVAS[0]), bool)
    pieces = {**view["links"], **view["sealed_links"]}
    ends = {"h": "we", "v": "ns", "corner_es": "es", "corner_sw": "sw", "corner_ne": "ne", "corner_nw": "nw"}
    stones = [s for s in view["nodes"] if view["nodes"][s][0] != "core"] + list(view["sealed_nodes"])
    for slot, kind in pieces.items():
        for end in ends[kind]:
            step = {"w": -1, "e": 1, "n": -9, "s": 9}[end]
            other = slot + step
            if other not in stones:
                continue
            x0, y0, _, _ = slot_art(other)
            if end in "we":
                span = (x0 + 18, y0 + 14, x0 + 36, y0 + 22) if end == "w" else (x0, y0 + 14, x0 + 18, y0 + 22)
            else:
                span = (x0 + 14, y0 + 18, x0 + 22, y0 + 36) if end == "n" else (x0 + 14, y0, x0 + 22, y0 + 18)
            out |= rect_mask(span, layout.CANVAS)
    return out


def grooves(canvas, view):
    mask = groove_mask(view) | _runs(view)
    # a worn stone shoulder around the channel lifts it off the slab, so the empty tree can be traced
    shoulder = dilate(dilate(mask)) & ~mask
    canvas.mask(shoulder, col("ember_stone", 2))
    canvas.mask(shoulder & ~shift(shoulder | mask, 0, 1), col("ember_stone", 3))
    canvas.mask(dilate(mask) & ~mask, col("iron", 0))
    sunk(canvas, mask, col("iron", 1), col("iron", 0), col("ember_stone", 4))


def _clamp(canvas, cx, cy, horizontal, dim=False):
    """A stone key across the 4 px slot gap: raised, so it is lit the opposite way to a cut."""
    w, h = (8, 14) if horizontal else (14, 8)
    r = (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)
    canvas.rect((r[0] - 1, r[1] - 1, r[2] + 1, r[3] + 2), col("iron", 0))
    top, face, low = (3, 2, 1) if dim else (4, 3, 1)
    frame(canvas, r, [(col("ember_stone", top), col("ember_stone", low))])
    canvas.rect((r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), col("ember_stone", face))
    pin = (cx - 1, cy - 1, cx + 1, cy + 1)
    canvas.rect(pin, col("iron", 1))
    canvas.rect((pin[0], pin[3], pin[2], pin[3] + 1), col("ember_stone", 4))


def clamps(canvas, view):
    ends = {"h": "we", "v": "ns", "corner_es": "es", "corner_sw": "sw", "corner_ne": "ne", "corner_nw": "nw"}
    spots = {}
    for slot, kind in {**view["links"], **view["sealed_links"]}.items():
        x0, y0, x1, y1 = slot_art(slot)
        for end in ends[kind]:
            at = {"w": (x0, y0 + 18, True), "e": (x1, y0 + 18, True),
                  "n": (x0 + 18, y0, False), "s": (x0 + 18, y1, False)}[end]
            spots[at] = spots.get(at, False) or slot in view["sealed_links"]
    for (cx, cy, horizontal), dim in spots.items():
        _clamp(canvas, cx, cy, horizontal, dim)


def socket(canvas, slot, kind):
    """The seat a node stone sits in, cut to the stone's own outline."""
    at = item_origin(slot)
    body = _place(shape(kind), at)
    rim = dilate(dilate(body))
    outer = dilate(rim)
    canvas.mask(outer, col("iron", 0))
    ys, xs = np.mgrid[0:canvas.size[1], 0:canvas.size[0]]
    upper = (xs - at[0]) + (ys - at[1]) < 31
    canvas.mask(rim & upper, col("iron", 0))
    canvas.mask(rim & ~upper, col("ember_stone", 4))
    canvas.mask(body, col("iron", 1))


def core_plinth(canvas, slot=0):
    """Cleave's own altar: apart from every groove, with a stepped base that marks it as given."""
    x0, y0, x1, y1 = slot_art(slot)
    block = [(x0 - 4, y0), (x1 + 4, y0), (x1 + 4, y1 + 2), (x0 - 4, y1 + 2)]
    canvas.mask(poly_mask(block, canvas.size), col("iron", 0))
    frame(canvas, (x0 - 3, y0 + 1, x1 + 3, y1 + 1), [(col("ember_stone", 4), col("ember_stone", 0)),
                                                     (col("ember_stone", 3), col("ember_stone", 1))])
    canvas.rect((x0 - 1, y0 + 3, x1 + 1, y1 - 1), col("ember_stone", 2))
    for step, (left, top) in enumerate(((-6, y1 + 2), (2, y1 + 8))):
        r = (x0 + left, top, x1 - left, top + 6)
        canvas.rect((r[0] - 1, r[1], r[2] + 1, r[3] + 1), col("iron", 0))
        frame(canvas, r, [(col("ember_stone", 4 - step), col("ember_stone", 0))])
        canvas.rect((r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), col("ember_stone", 3 - step))
    socket(canvas, slot, "core")
    middle = (x0 + x1) // 2
    chrome.gem(canvas, middle, y1 + 5, 3, "crimson")


# --- sealed stones ----------------------------------------------------------------------------

# a rough plug with an outline unlike both node shapes
PLUG = [(11, 2), (21, 1), (28, 6), (31, 15), (28, 22), (30, 27), (21, 30), (12, 29), (4, 31), (1, 22),
        (3, 15), (2, 8)]


def sealed(canvas, slot, grand=False):
    """An unreadable stone wedged into its seat and bound with iron. No hint of a skill."""
    x0, y0, x1, y1 = slot_art(slot)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # the ultimate's stone is wider than a slot in the painted art, but stays above the footer
    wide, tall = (1.5, 1.16) if grand else (1.08, 1.08)
    if grand:
        cy -= 1

    def place(point):
        return (round(cx + (point[0] - 16) * wide), round(cy + (point[1] - 16) * tall))

    def at(points):
        return poly_mask([(cx + (x - 16) * wide, cy + (y - 16) * tall) for x, y in points], canvas.size)

    plug = at(PLUG)
    canvas.mask(dilate(dilate(dilate(plug))), col("iron", 0))
    pit = dilate(dilate(dilate(dilate(plug)))) & ~dilate(dilate(dilate(plug)))
    ys, xs = np.mgrid[0:canvas.size[1], 0:canvas.size[0]]
    canvas.mask(pit & ((xs - cx) + (ys - cy) > 0), col("ember_stone", 4))
    canvas.mask(plug, col("ember_stone", 2))
    canvas.mask(at([(2, 8), (11, 2), (21, 1), (28, 6), (19, 11), (9, 13)]) & plug, col("ember_stone", 3))
    canvas.mask(at([(19, 11), (28, 6), (31, 15), (28, 22), (30, 27), (21, 30), (22, 19)]) & plug,
                col("ember_stone", 1))
    canvas.mask(plug & ~shift(plug, 0, 1), col("ember_stone", 4))
    canvas.mask(plug & ~shift(plug, 0, -1), col("ember_stone", 0))
    # a deep split and scratches that stop mid-stroke: damage, never a shape that could be a skill
    for a, b in (((9, 3), (14, 9)), ((14, 9), (12, 13)), ((24, 6), (21, 11)), ((8, 24), (12, 26))):
        _line(canvas, place(a), place(b), col("ember_stone", 4), 1)
        _line(canvas, place(a), place(b), col("iron", 0))
    # iron bands off centre and askew: one on a keystone, two crossing on the ultimate
    straps = [((-1, 14), (33, 22))]
    if grand:
        straps = [((-1, 8), (33, 25)), ((-1, 25), (33, 8))]
    for (ax, ay), (bx, by) in straps:
        strap = at([(ax, ay), (bx, by), (bx, by + 5), (ax, ay + 5)]) & dilate(dilate(plug))
        canvas.mask(dilate(strap) & dilate(dilate(plug)), col("iron", 0))
        canvas.mask(strap, col("iron", 3))
        canvas.mask(strap & ~shift(strap, 0, 1), col("iron", 5))
        canvas.mask(strap & ~shift(strap, 0, -1), col("iron", 2))
        for t in (0.17, 0.83):
            x, y = place((ax + (bx - ax) * t, ay + (by - ay) * t + 2.5))
            canvas.rect((x - 1, y - 1, x + 1, y + 1), col("iron", 5))
            canvas.rect((x - 1, y + 1, x + 2, y + 2), col("iron", 0))
    if grand:
        # a lump of old wax over the crossing, unstamped, with a trace of dried red
        wax = at([(14, 13), (19, 14), (20, 18), (18, 21), (13, 20), (12, 16)])
        canvas.mask(dilate(wax), col("iron", 0))
        canvas.mask(wax, col("crimson", 1))
        canvas.mask(wax & ~shift(wax, 0, 1), col("crimson", 2))
        canvas.mask(wax & ~shift(wax, 0, -1), col("crimson", 0))


# --- header and footer ------------------------------------------------------------------------

def header(canvas, title):
    """A dark lintel with the branch name; the frame keeps the class menu's metal, but tarnished."""
    width = layout.CANVAS[0]
    plaque = (38, 4, width - 38, 31)
    frame(canvas, plaque, [(col("iron", 0), col("iron", 0)), (col("gold", 2), col("gold", 0)),
                           (col("gold", 0), col("gold", 1)), (col("iron", 0), col("ember_stone", 4))])
    inner = (plaque[0] + 4, plaque[1] + 4, plaque[2] - 4, plaque[3] - 4)
    canvas.rect(inner, col("ember_stone", 0))
    lettering.draw(canvas, title, width // 2, plaque[1] + 5,
                   (("steel", 5), ("steel", 4), ("steel", 6)), ("iron", 0))
    middle = (plaque[1] + plaque[3]) // 2
    for centre, direction in ((22, 1), (width - 22, -1)):
        canvas.poly([(centre, middle - 4), (centre + direction * 17, middle), (centre, middle + 4)],
                    col("iron", 0))
        canvas.poly([(centre, middle - 2), (centre + direction * 13, middle), (centre, middle)], col("gold", 1))
        canvas.poly([(centre, middle), (centre + direction * 13, middle), (centre, middle + 2)], col("gold", 0))
        chrome.gem(canvas, centre, middle, 6, "crimson")
    for x in (inner[0] + 8, inner[2] - 12):
        for y in (middle - 5, middle + 3):
            canvas.rect((x, y, x + 4, y + 2), col("crimson", 1))
    canvas.rect((8, 32, width - 8, 33), col("iron", 0))
    canvas.rect((8, 33, width - 8, 34), col("gold", 0))


def _block_arrow(size, cx, cy, direction):
    """A chunky chiselled arrow pointing "left", "up" or "down"."""
    base = [(-10, 0), (0, -10), (1, -10), (1, -4), (10, -4), (10, 4), (1, 4), (1, 10), (0, 10)]
    turn = {"left": lambda x, y: (x, y), "up": lambda x, y: (y, x), "down": lambda x, y: (y, -x)}[direction]
    return poly_mask([(cx + turn(x, y)[0], cy + turn(x, y)[1]) for x, y in base], size)


def _loadout_symbol(size, cx, cy):
    """Four small stones in a block: the four combo slots."""
    mask = np.zeros((size[1], size[0]), bool)
    for dx in (-9, 2):
        for dy in (-9, 2):
            mask |= poly_mask([(cx + dx + 2, cy + dy), (cx + dx + 5, cy + dy), (cx + dx + 7, cy + dy + 2),
                               (cx + dx + 7, cy + dy + 5), (cx + dx + 5, cy + dy + 7),
                               (cx + dx + 2, cy + dy + 7), (cx + dx, cy + dy + 5), (cx + dx, cy + dy + 2)], size)
    return mask


def _info_symbol(size, cx, cy):
    mask = rect_mask((cx - 2, cy - 10, cx + 2, cy - 6), size)
    mask |= rect_mask((cx - 5, cy - 3, cx + 2, cy), size)
    mask |= rect_mask((cx - 2, cy - 3, cx + 2, cy + 9), size)
    mask |= rect_mask((cx - 5, cy + 7, cx + 5, cy + 10), size)
    return mask


def _footer_button(canvas, slot, symbol, enabled=True):
    x0, y0, x1, y1 = slot_art(slot)
    r = (x0 + 1, y0 + 2, x1 - 1, y1 - 1)
    canvas.rect(r, col("iron", 0))
    if enabled:
        frame(canvas, (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1),
              [(col("ember_stone", 4), col("ember_stone", 0)), (col("ember_stone", 3), col("ember_stone", 1))])
        canvas.rect((r[0] + 3, r[1] + 3, r[2] - 3, r[3] - 3), col("ember_stone", 2))
        mask = symbol(canvas.size, (x0 + x1) // 2, (y0 + y1) // 2)
        backing = dilate(mask)
        canvas.mask(backing | shift(backing, 0, 1), col("iron", 0))
        canvas.mask(mask, col("steel", 4))
        canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 5))
    else:
        # unusable: flush with the ledge and only scratched in
        frame(canvas, (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), [(col("iron", 2), col("iron", 2))])
        canvas.rect((r[0] + 2, r[1] + 2, r[2] - 2, r[3] - 2), col("ember_stone", 0))
        mask = symbol(canvas.size, (x0 + x1) // 2, (y0 + y1) // 2)
        sunk(canvas, mask, col("iron", 0), None, col("ember_stone", 3))


def _tab(canvas, slot, icon, active):
    """Branch tabs: the open one stands tall with a bright sigil and a crimson marker bar; the others
    sit lower in cold iron. Nothing reaches above the footer, so no tab looks joined to a node."""
    x0, y0, x1, y1 = slot_art(slot)
    cx = (x0 + x1) // 2
    r = (x0 + 1, y0 + 1 if active else y0 + 5, x1 - 1, y1 - 1)
    canvas.rect(r, col("iron", 0))
    inner = (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1)
    if active:
        frame(canvas, inner, [(col("gold", 3), col("gold", 1)), (col("ember_stone", 4), col("ember_stone", 1))])
        canvas.rect((inner[0] + 2, inner[1] + 2, inner[2] - 2, inner[3] - 2), col("ember_stone", 2))
        canvas.rect((inner[0] + 4, inner[3] - 5, inner[2] - 4, inner[3] - 2), col("crimson", 3))
        canvas.rect((inner[0] + 4, inner[3] - 5, inner[2] - 4, inner[3] - 4), col("crimson", 4))
    else:
        frame(canvas, inner, [(col("iron", 4), col("iron", 1)), (col("iron", 3), col("iron", 1))])
        canvas.rect((inner[0] + 2, inner[1] + 2, inner[2] - 2, inner[3] - 2), col("iron", 2))
    # the 24 px sigil keeps its two empty rows outside the face
    mask = _place(ICONS[icon], (cx - 12, y0 + 3 if active else y0 + 8))
    if not active:
        mask &= rect_mask((x0, y0, x1, y1 - 3), canvas.size)
    backing = dilate(mask)
    canvas.mask(backing | shift(backing, 0, 1), col("iron", 0))
    canvas.mask(mask, col("steel", 5 if active else 3))
    canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 6 if active else 4))


def footer(canvas, branch, view_name):
    """Slots 45-53 on a stone ledge. Slot 49 only gets a seat; the reset button is an item."""
    x0, y0, x1, y1 = FOOTER
    canvas.rect((x0, y0, x1, y1), col("ember_stone", 0))
    canvas.rect((x0, y0, x1, y0 + 1), col("iron", 0))
    canvas.rect((x0, y0 + 1, x1, y0 + 3), col("ember_stone", 4))
    canvas.rect((x0, y0 + 3, x1, y0 + 4), col("ember_stone", 2))
    canvas.rect((x0, y0 + 4, x1, y0 + 5), col("iron", 0))
    _footer_button(canvas, 45, lambda s, x, y: _block_arrow(s, x, y, "left"))
    for index, name in enumerate(("guardian", "berserker", "duelist")):
        _tab(canvas, 46 + index, f"tab_{name}", name == branch)
    # the reset seat: a deeper round bed, with studs reaching up to the ledge so it reads as special
    seat = _place(shape("active"), item_origin(49))
    canvas.rect(slot_art(49), col("ember_stone", 1))
    canvas.mask(dilate(seat), col("iron", 0))
    sx0, sy0, sx1, _ = slot_art(49)
    for x in (sx0 - 1, sx1 - 1):
        canvas.rect((x, sy0 + 4, x + 2, sy0 + 34), col("gold", 0))
        canvas.rect((x, sy0 + 4, x + 1, sy0 + 34), col("gold", 1))
    _footer_button(canvas, 50, lambda s, x, y: _block_arrow(s, x, y, "up"), enabled=view_name == "b")
    _footer_button(canvas, 51, lambda s, x, y: _block_arrow(s, x, y, "down"), enabled=view_name == "a")
    _footer_button(canvas, 52, _loadout_symbol)
    _footer_button(canvas, 53, _info_symbol)


def dim_label_plate(canvas):
    """One step darker than the class menu's parchment, so it does not outshine the dark slab."""
    x0, y0, x1, y1 = layout.INVENTORY_PLATE
    frame(canvas, (x0, y0 + 1, x1, y1), [(col("iron", 0), col("iron", 0)),
                                         (col("parchment", 2), col("leather", 1))])
    canvas.rect((x0 + 2, y0 + 3, x1 - 2, y1 - 2), col("parchment", 1))
    chrome.gem(canvas, x1 - 8, (y0 + y1) // 2 + 1, 4)


# --- the page ---------------------------------------------------------------------------------

def _keep_out(view):
    """Where no pit or carving may go: grooves and node seats, with a clear margin."""
    mask = groove_mask(view) | _runs(view)
    for slot in list(view["nodes"]) + list(view["sealed_nodes"]):
        x0, y0, x1, y1 = slot_art(slot)
        mask |= rect_mask((x0 - 2, y0 - 2, x1 + 2, y1 + (14 if slot == 0 else 2)), layout.CANVAS)
    for _ in range(3):
        mask = dilate(mask)
    return mask


def page(branch, view_name):
    """One background master: everything on the page that never changes."""
    view = VIEWS[view_name]
    canvas = Canvas(*layout.CANVAS)
    chrome.shell(canvas)
    slab(canvas)
    keep = _keep_out(view)
    carvings(canvas, keep)
    pits(canvas, keep)
    cracks(canvas)
    # inner shadow where the slab sits inside the metal frame
    x0, y0, x1, _ = SLAB
    canvas.rect((x0, y0, x1, y0 + 2), col("iron", 0))
    canvas.rect((x0, y0, x0 + 2, SLAB[3]), col("iron", 0))
    grooves(canvas, view)
    clamps(canvas, view)
    for slot, (kind, _) in view["nodes"].items():
        if kind == "core":
            core_plinth(canvas, slot)
        else:
            socket(canvas, slot, kind)
    for slot in view["sealed_nodes"]:
        sealed(canvas, slot, grand=slot == 40)
    footer(canvas, branch, view_name)
    header(canvas, branch.upper())
    chrome.inventory(canvas)
    dim_label_plate(canvas)
    return canvas.image()
