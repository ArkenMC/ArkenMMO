"""Whole skill menus: grooves, sockets and sealed stones on the class slab, plus the slot maps.

Layout and frame are shared by every class; a class only changes stone, carving and glow.
"""
from . import chrome, layout, lettering, treebars
from .draw import Canvas, dilate, frame, poly_mask, rect_mask, shift
from .palette import col
from .treeicons import ICONS
from .treenodes import channel, shape
from .treeslab import SLAB, carvings, cracks, item_origin, line, pits, place, slab, slot_art, sunk
from .treetheme import ARCHETYPE_NAMES

# slot -> (kind, node id) and slot -> connector shape, per view
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
# edge -> connector slots on each view; an edge's pieces are set when both its ends are owned
EDGES = {
    "a": {"n1-n2": (2, 3, 11), "n1-n3": (5, 6, 15), "n2-n4": (29,), "n3-n6": (33,),
          "n4-n5": (39,), "n5-n6": (41,)},
    "b": {"n4-n5": (3,), "n5-n6": (5,)},
}
# lower view backgrounds: name suffix -> columns whose incoming path (n2-n4, n3-n6) is lit
LOWER_VARIANTS = {"b": (), "b_left": (2,), "b_right": (6,), "b_both": (2, 6)}

LOADOUT_COMBO_SLOTS = (10, 12, 14, 16)
# the nine branch actives, in tab order then n1, n4, n6; the core active sits alone below
LOADOUT_POOL_SLOTS = tuple(range(27, 36))
LOADOUT_CORE_SLOT = 40

ENDS = {"h": "we", "v": "ns", "corner_es": "es", "corner_sw": "sw", "corner_ne": "ne", "corner_nw": "nw"}


# --- grooves, clamps, sockets -----------------------------------------------------------------

def _piece_mask(kind, slot):
    """A connector groove stretched across the whole 36 px cell."""
    if kind == "corner_ne":
        base = channel("corner_es")[::-1, :]
    elif kind == "corner_nw":
        base = channel("corner_es")[::-1, ::-1]
    else:
        base = channel(kind)
    wide = _pad(base)
    return place(wide, slot_art(slot)[:2])


def _pad(tile):
    return tile[[0, 0, *range(tile.shape[0]), -1, -1]][:, [0, 0, *range(tile.shape[1]), -1, -1]]


def groove_mask(view):
    mask = rect_mask((0, 0, 0, 0), layout.CANVAS)
    for slot, kind in {**view["links"], **view["sealed_links"]}.items():
        mask |= _piece_mask(kind, slot)
    return mask


def _runs(view):
    """Groove stubs from each linked node toward its neighbours, so no channel stops short of a stone."""
    out = rect_mask((0, 0, 0, 0), layout.CANVAS)
    stones = [s for s in view["nodes"] if view["nodes"][s][0] != "core"] + list(view["sealed_nodes"])
    for slot, kind in {**view["links"], **view["sealed_links"]}.items():
        for end in ENDS[kind]:
            other = slot + {"w": -1, "e": 1, "n": -9, "s": 9}[end]
            if other not in stones:
                continue
            x0, y0, _, _ = slot_art(other)
            if end in "we":
                span = (x0 + 18, y0 + 14, x0 + 36, y0 + 22) if end == "w" else (x0, y0 + 14, x0 + 18, y0 + 22)
            else:
                span = (x0 + 14, y0 + 18, x0 + 22, y0 + 36) if end == "n" else (x0 + 14, y0, x0 + 22, y0 + 18)
            out |= rect_mask(span, layout.CANVAS)
    return out


def grooves(canvas, theme, view):
    mask = groove_mask(view) | _runs(view)
    # a worn stone shoulder around the channel lifts it off the slab, so the empty tree can be traced
    shoulder = dilate(dilate(mask)) & ~mask
    canvas.mask(shoulder, theme.s(2))
    canvas.mask(shoulder & ~shift(shoulder | mask, 0, 1), theme.s(3))
    canvas.mask(dilate(mask) & ~mask, col("iron", 0))
    sunk(canvas, mask, col("iron", 1), col("iron", 0), theme.s(4))


def _clamp(canvas, theme, cx, cy, horizontal, dim):
    """A stone key across the 4 px slot gap: raised, so it is lit the opposite way to a cut."""
    w, h = (8, 14) if horizontal else (14, 8)
    r = (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)
    canvas.rect((r[0] - 1, r[1] - 1, r[2] + 1, r[3] + 2), col("iron", 0))
    top, face, low = (3, 2, 1) if dim else (4, 3, 1)
    frame(canvas, r, [(theme.s(top), theme.s(low))])
    canvas.rect((r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), theme.s(face))
    pin = (cx - 1, cy - 1, cx + 1, cy + 1)
    canvas.rect(pin, col("iron", 1))
    canvas.rect((pin[0], pin[3], pin[2], pin[3] + 1), theme.s(4))


def clamps(canvas, theme, view):
    spots = {}
    for slot, kind in {**view["links"], **view["sealed_links"]}.items():
        x0, y0, x1, y1 = slot_art(slot)
        for end in ENDS[kind]:
            at = {"w": (x0, y0 + 18, True), "e": (x1, y0 + 18, True),
                  "n": (x0 + 18, y0, False), "s": (x0 + 18, y1, False)}[end]
            spots[at] = spots.get(at, False) or slot in view["sealed_links"]
    for (cx, cy, horizontal), dim in spots.items():
        _clamp(canvas, theme, cx, cy, horizontal, dim)


def socket(canvas, theme, slot, kind):
    """The seat a node stone sits in, cut to the stone's own outline."""
    at = item_origin(slot)
    body = place(shape(kind), at)
    rim = dilate(dilate(body))
    canvas.mask(dilate(rim), col("iron", 0))
    upper = _above_diagonal(canvas, at)
    canvas.mask(rim & upper, col("iron", 0))
    canvas.mask(rim & ~upper, theme.s(4))
    canvas.mask(body, col("iron", 1))


def _above_diagonal(canvas, at):
    mask = rect_mask((0, 0, 0, 0), canvas.size)
    for y in range(canvas.size[1]):
        mask[y, :max(0, min(canvas.size[0], at[0] + 31 - (y - at[1])))] = True
    return mask


def core_plinth(canvas, theme, slot=0):
    """The core skill's own altar: apart from every groove, with a stepped base that marks it as given."""
    x0, y0, x1, y1 = slot_art(slot)
    block = [(x0 - 4, y0), (x1 + 4, y0), (x1 + 4, y1 + 2), (x0 - 4, y1 + 2)]
    canvas.mask(poly_mask(block, canvas.size), col("iron", 0))
    frame(canvas, (x0 - 3, y0 + 1, x1 + 3, y1 + 1), [(theme.s(4), theme.s(0)), (theme.s(3), theme.s(1))])
    canvas.rect((x0 - 1, y0 + 3, x1 + 1, y1 - 1), theme.s(2))
    for step, (left, top) in enumerate(((-6, y1 + 2), (2, y1 + 8))):
        r = (x0 + left, top, x1 - left, top + 6)
        canvas.rect((r[0] - 1, r[1], r[2] + 1, r[3] + 1), col("iron", 0))
        frame(canvas, r, [(theme.s(4 - step), theme.s(0))])
        canvas.rect((r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), theme.s(3 - step))
    socket(canvas, theme, slot, "core")
    chrome.gem(canvas, (x0 + x1) // 2, y1 + 5, 3, theme.gem)


# --- sealed stones ----------------------------------------------------------------------------

# a rough plug with an outline unlike both node shapes
PLUG = [(11, 2), (21, 1), (28, 6), (31, 15), (28, 22), (30, 27), (21, 30), (12, 29), (4, 31), (1, 22),
        (3, 15), (2, 8)]


def sealed(canvas, theme, slot, grand=False):
    """An unreadable stone wedged into its seat and bound with iron. No hint of a skill."""
    x0, y0, x1, y1 = slot_art(slot)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # the ultimate's stone is wider than a slot in the painted art, but stays above the footer
    wide, tall = (1.5, 1.16) if grand else (1.08, 1.08)
    if grand:
        cy -= 1

    def point(p):
        return (round(cx + (p[0] - 16) * wide), round(cy + (p[1] - 16) * tall))

    def at(points):
        return poly_mask([(cx + (x - 16) * wide, cy + (y - 16) * tall) for x, y in points], canvas.size)

    plug = at(PLUG)
    seat = dilate(dilate(dilate(plug)))
    canvas.mask(seat, col("iron", 0))
    below = ~_above_diagonal(canvas, (cx - 15, cy - 15))
    canvas.mask(dilate(seat) & ~seat & below, theme.s(4))
    canvas.mask(plug, theme.s(2))
    canvas.mask(at([(2, 8), (11, 2), (21, 1), (28, 6), (19, 11), (9, 13)]) & plug, theme.s(3))
    canvas.mask(at([(19, 11), (28, 6), (31, 15), (28, 22), (30, 27), (21, 30), (22, 19)]) & plug, theme.s(1))
    canvas.mask(plug & ~shift(plug, 0, 1), theme.s(4))
    canvas.mask(plug & ~shift(plug, 0, -1), theme.s(0))
    # a deep split and scratches that stop mid-stroke: damage, never a shape that could be a skill
    for a, b in (((9, 3), (14, 9)), ((14, 9), (12, 13)), ((24, 6), (21, 11)), ((8, 24), (12, 26))):
        line(canvas, point(a), point(b), theme.s(4), 1)
        line(canvas, point(a), point(b), col("iron", 0))
    # iron bands off centre and askew: one on a keystone, two crossing on the ultimate
    straps = [((-1, 8), (33, 25)), ((-1, 25), (33, 8))] if grand else [((-1, 14), (33, 22))]
    for (ax, ay), (bx, by) in straps:
        strap = at([(ax, ay), (bx, by), (bx, by + 5), (ax, ay + 5)]) & dilate(dilate(plug))
        canvas.mask(dilate(strap) & dilate(dilate(plug)), col("iron", 0))
        canvas.mask(strap, col("iron", 3))
        canvas.mask(strap & ~shift(strap, 0, 1), col("iron", 5))
        canvas.mask(strap & ~shift(strap, 0, -1), col("iron", 2))
        for t in (0.17, 0.83):
            x, y = point((ax + (bx - ax) * t, ay + (by - ay) * t + 2.5))
            canvas.rect((x - 1, y - 1, x + 1, y + 1), col("iron", 5))
            canvas.rect((x - 1, y + 1, x + 2, y + 2), col("iron", 0))
    if grand:
        # a lump of old wax over the crossing, unstamped
        wax = at([(14, 13), (19, 14), (20, 18), (18, 21), (13, 20), (12, 16)])
        canvas.mask(dilate(wax), col("iron", 0))
        canvas.mask(wax, theme.g(1))
        canvas.mask(wax & ~shift(wax, 0, 1), theme.g(2))
        canvas.mask(wax & ~shift(wax, 0, -1), theme.g(0))


# --- whole menus ------------------------------------------------------------------------------

def dim_label_plate(canvas):
    """One step darker than the class menu's parchment, so it does not outshine the dark slab."""
    x0, y0, x1, y1 = layout.INVENTORY_PLATE
    frame(canvas, (x0, y0 + 1, x1, y1), [(col("iron", 0), col("iron", 0)),
                                         (col("parchment", 2), col("leather", 1))])
    canvas.rect((x0 + 2, y0 + 3, x1 - 2, y1 - 2), col("parchment", 1))
    chrome.gem(canvas, x1 - 8, (y0 + y1) // 2 + 1, 4)


def _keep_out(view, extra=()):
    """Where no pit or carving may go: grooves and node seats, with a clear margin."""
    mask = groove_mask(view) | _runs(view)
    for slot in list(view["nodes"]) + list(view["sealed_nodes"]) + list(extra):
        x0, y0, x1, y1 = slot_art(slot)
        mask |= rect_mask((x0 - 2, y0 - 2, x1 + 2, y1 + (14 if slot == 0 else 2)), layout.CANVAS)
    for _ in range(3):
        mask = dilate(mask)
    return mask


def _stone_body(theme, keep, carved=True):
    canvas = Canvas(*layout.CANVAS)
    chrome.shell(canvas)
    slab(canvas, theme)
    if carved:
        carvings(canvas, theme, keep)
    pits(canvas, theme, keep)
    cracks(canvas, theme)
    # inner shadow where the slab sits inside the metal frame
    x0, y0, x1, _ = SLAB
    canvas.rect((x0, y0, x1, y0 + 2), col("iron", 0))
    canvas.rect((x0, y0, x0 + 2, SLAB[3]), col("iron", 0))
    return canvas


def _finish(canvas):
    chrome.inventory(canvas)
    dim_label_plate(canvas)
    return canvas.image()


def page(theme, branch, view_name):
    """One background master; `view_name` is "a" or a key of LOWER_VARIANTS."""
    lower = view_name in LOWER_VARIANTS
    view = VIEWS["b" if lower else "a"]
    canvas = _stone_body(theme, _keep_out(view))
    grooves(canvas, theme, view)
    clamps(canvas, theme, view)
    for slot, (kind, _) in view["nodes"].items():
        if kind == "core":
            core_plinth(canvas, theme, slot)
        else:
            socket(canvas, theme, slot, kind)
    for slot in view["sealed_nodes"]:
        sealed(canvas, theme, slot, grand=slot == 40)
    treebars.footer(canvas, theme, branch, "b" if lower else "a")
    treebars.header(canvas, theme, ARCHETYPE_NAMES[branch].upper())
    if lower:
        treebars.paths_up(canvas, theme, LOWER_VARIANTS[view_name])
    else:
        treebars.paths_down(canvas, theme)
    return _finish(canvas)


def loadout(theme):
    """Four combo seats with their click patterns painted above, and the pool of actives below."""
    empty = {"nodes": {}, "links": {}, "sealed_nodes": (), "sealed_links": {}}
    seats = (*LOADOUT_COMBO_SLOTS, *LOADOUT_POOL_SLOTS, LOADOUT_CORE_SLOT)
    # no carvings here: between the seats they would only show as broken fragments
    canvas = _stone_body(theme, _keep_out(empty, seats + (1, 3, 5, 7, 19, 22, 25)), carved=False)
    for slot, combo in zip(LOADOUT_COMBO_SLOTS, theme.combos):
        x0, y0, x1, y1 = slot_art(slot)
        lettering.draw(canvas, combo, (x0 + x1) // 2, y0 - 25,
                       (("steel", 5), ("steel", 4), ("steel", 6)), ("iron", 0))
        frame(canvas, (x0 - 4, y0 - 3, x1 + 4, y1 + 3),
              [(col("iron", 0), col("iron", 0)), (col("gold", 2), col("gold", 0)), (theme.s(3), theme.s(1))])
        canvas.rect((x0 - 1, y0, x1 + 1, y1), theme.s(1))
        socket(canvas, theme, slot, "active")
    # a ledge parts the equipped four from the pool
    canvas.rect((14, 111, layout.CANVAS[0] - 14, 112), col("iron", 0))
    canvas.rect((14, 112, layout.CANVAS[0] - 14, 114), theme.s(4))
    canvas.rect((14, 114, layout.CANVAS[0] - 14, 115), col("iron", 0))
    # each group of three is marked with its branch sigil, carved and unpainted
    for slot, branch in zip((19, 22, 25), theme.branches):
        x0, y0, _, _ = slot_art(slot)
        mark = place(ICONS[f"tab_{branch}"], (x0 + 6, y0 + 10))
        canvas.mask(dilate(dilate(mark)), col("iron", 0))
        sunk(canvas, mark, col("steel", 3), col("steel", 2), theme.s(4))
    for x in (14 + 3 * 36, 14 + 6 * 36):
        canvas.rect((x - 1, 150, x, 208), col("iron", 0))
        canvas.rect((x, 150, x + 1, 208), theme.s(3))
    for slot in LOADOUT_POOL_SLOTS:
        socket(canvas, theme, slot, "active")
    x0, y0, x1, y1 = slot_art(LOADOUT_CORE_SLOT)
    socket(canvas, theme, LOADOUT_CORE_SLOT, "core")
    for centre in (x0 - 12, x1 + 12):
        chrome.gem(canvas, centre, (y0 + y1) // 2, 4, theme.gem)
    treebars.loadout_footer(canvas, theme)
    treebars.header(canvas, theme, "LOADOUT")
    return _finish(canvas)
