"""Header lintel, footer ledge and buttons, and the path mouths that lead to the other view."""
from . import chrome, layout, lettering
from .draw import Canvas, dilate, frame, poly_mask, rect_mask, shift
from .palette import col
from .treeicons import ICONS
from .treenodes import depth, paint_glow, shape
from .treeslab import item_origin, place, slot_art, sunk

FOOTER = (8, 214, layout.CANVAS[0] - 8, 250)
# footer buttons start below a 6 px ledge, which leaves room for the paths that run off the page
BUTTON_TOP = 6
# the two columns whose paths cross the view edge: n2-n4 and n4-n7 on one side, n3-n6 and n6-n8
EDGE_COLUMNS = (2, 6)
# first art row below the title lettering
TITLE_BOTTOM = 25


def header(canvas, theme, title):
    """A dark lintel with the page name; the frame keeps the class menu's metal, but tarnished."""
    width = layout.CANVAS[0]
    plaque = (38, 4, width - 38, 31)
    frame(canvas, plaque, [(col("iron", 0), col("iron", 0)), (col("gold", 2), col("gold", 0)),
                           (col("gold", 0), col("gold", 1)), (col("iron", 0), theme.s(4))])
    inner = (plaque[0] + 4, plaque[1] + 4, plaque[2] - 4, plaque[3] - 4)
    canvas.rect(inner, theme.s(0))
    lettering.draw(canvas, title, width // 2, plaque[1] + 5,
                   (("steel", 5), ("steel", 4), ("steel", 6)), ("iron", 0))
    middle = (plaque[1] + plaque[3]) // 2
    for centre, direction in ((22, 1), (width - 22, -1)):
        canvas.poly([(centre, middle - 4), (centre + direction * 17, middle), (centre, middle + 4)],
                    col("iron", 0))
        canvas.poly([(centre, middle - 2), (centre + direction * 13, middle), (centre, middle)], col("gold", 1))
        canvas.poly([(centre, middle), (centre + direction * 13, middle), (centre, middle + 2)], col("gold", 0))
        chrome.gem(canvas, centre, middle, 6, theme.gem)
    if lettering.width(title) < inner[2] - inner[0] - 32:
        for x in (inner[0] + 8, inner[2] - 12):
            for y in (middle - 5, middle + 3):
                canvas.rect((x, y, x + 4, y + 2), theme.g(1))
    canvas.rect((8, 32, width - 8, 33), col("iron", 0))
    canvas.rect((8, 33, width - 8, 34), col("gold", 0))


def _block_arrow(size, cx, cy, direction):
    """A chunky chiselled arrow pointing "left", "up" or "down"."""
    base = [(-10, 0), (0, -10), (1, -10), (1, -4), (10, -4), (10, 4), (1, 4), (1, 10), (0, 10)]
    turn = {"left": lambda x, y: (x, y), "up": lambda x, y: (y, x), "down": lambda x, y: (y, -x)}[direction]
    return poly_mask([(cx + turn(x, y)[0], cy + turn(x, y)[1]) for x, y in base], size)


def _loadout_symbol(size, cx, cy):
    """Four small stones in a block: the four combo slots."""
    mask = rect_mask((0, 0, 0, 0), size)
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


def _footer_button(canvas, theme, slot, symbol, enabled=True):
    x0, y0, x1, y1 = slot_art(slot)
    r = (x0 + 1, y0 + BUTTON_TOP, x1 - 1, y1 - 1)
    centre = ((x0 + x1) // 2, (r[1] + r[3]) // 2)
    canvas.rect(r, col("iron", 0))
    if enabled:
        frame(canvas, (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1),
              [(theme.s(4), theme.s(0)), (theme.s(3), theme.s(1))])
        canvas.rect((r[0] + 3, r[1] + 3, r[2] - 3, r[3] - 3), theme.s(2))
        mask = symbol(canvas.size, *centre)
        backing = dilate(mask)
        canvas.mask(backing | shift(backing, 0, 1), col("iron", 0))
        canvas.mask(mask, col("steel", 4))
        canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 5))
    else:
        # unusable: flush with the ledge and only scratched in
        frame(canvas, (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1), [(col("iron", 2), col("iron", 2))])
        canvas.rect((r[0] + 2, r[1] + 2, r[2] - 2, r[3] - 2), theme.s(0))
        sunk(canvas, symbol(canvas.size, *centre), col("iron", 0), None, theme.s(3))


def _tab(canvas, theme, slot, icon, active):
    """Branch tabs: the open one stands taller with a bright sigil and a class marker bar; the
    others sit lower in cold iron. Nothing reaches above the footer."""
    x0, y0, x1, y1 = slot_art(slot)
    cx = (x0 + x1) // 2
    r = (x0 + 1, y0 + (BUTTON_TOP if active else BUTTON_TOP + 2), x1 - 1, y1 - 1)
    canvas.rect(r, col("iron", 0))
    inner = (r[0] + 1, r[1] + 1, r[2] - 1, r[3] - 1)
    if active:
        frame(canvas, inner, [(col("gold", 3), col("gold", 1)), (theme.s(4), theme.s(1))])
        canvas.rect((inner[0] + 2, inner[1] + 2, inner[2] - 2, inner[3] - 2), theme.s(2))
        canvas.rect((inner[0] + 4, inner[3] - 4, inner[2] - 4, inner[3] - 2), theme.g(3))
        canvas.rect((inner[0] + 4, inner[3] - 4, inner[2] - 4, inner[3] - 3), theme.g(4))
    else:
        frame(canvas, inner, [(col("iron", 4), col("iron", 1)), (col("iron", 3), col("iron", 1))])
        canvas.rect((inner[0] + 2, inner[1] + 2, inner[2] - 2, inner[3] - 2), col("iron", 2))
    # the 24 px sigil keeps its empty rows outside the face
    mask = place(ICONS[icon], (cx - 12, y0 + (BUTTON_TOP + 1 if active else BUTTON_TOP + 3)))
    mask &= rect_mask((x0, y0, x1, y1 - (4 if active else 3)), canvas.size)
    backing = dilate(mask)
    canvas.mask(backing | shift(backing, 0, 1), col("iron", 0))
    canvas.mask(mask, col("steel", 5 if active else 3))
    canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 6 if active else 4))


def ledge(canvas, theme):
    x0, y0, x1, y1 = FOOTER
    canvas.rect((x0, y0, x1, y1), theme.s(0))
    canvas.rect((x0, y0, x1, y0 + 1), col("iron", 0))
    canvas.rect((x0, y0 + 1, x1, y0 + 3), theme.s(4))
    canvas.rect((x0, y0 + 3, x1, y0 + 5), theme.s(2))
    canvas.rect((x0, y0 + 5, x1, y0 + 6), col("iron", 0))


def footer(canvas, theme, branch, view_name):
    """Slots 45-53 of a tree page. Slot 49 only gets a seat; the reset button is an item."""
    ledge(canvas, theme)
    _footer_button(canvas, theme, 45, lambda s, x, y: _block_arrow(s, x, y, "left"))
    for index, name in enumerate(theme.branches):
        _tab(canvas, theme, 46 + index, f"tab_{name}", name == branch)
    # the reset seat: a deeper round bed with studs up to the ledge, so it reads as special
    seat = place(shape("active"), item_origin(49))
    canvas.rect(slot_art(49), theme.s(1))
    canvas.mask(dilate(seat), col("iron", 0))
    sx0, sy0, sx1, _ = slot_art(49)
    for x in (sx0 - 1, sx1 - 1):
        canvas.rect((x, sy0 + 4, x + 2, sy0 + 34), col("gold", 0))
        canvas.rect((x, sy0 + 4, x + 1, sy0 + 34), col("gold", 1))
    _footer_button(canvas, theme, 50, lambda s, x, y: _block_arrow(s, x, y, "up"), enabled=view_name == "b")
    _footer_button(canvas, theme, 51, lambda s, x, y: _block_arrow(s, x, y, "down"), enabled=view_name == "a")
    _footer_button(canvas, theme, 52, _loadout_symbol)
    _footer_button(canvas, theme, 53, _info_symbol)


def loadout_footer(canvas, theme):
    """The loadout menu has back and info only; the other slots are plain ledge."""
    ledge(canvas, theme)
    _footer_button(canvas, theme, 45, lambda s, x, y: _block_arrow(s, x, y, "left"))
    _footer_button(canvas, theme, 53, _info_symbol)


# --- paths that cross the view edge -----------------------------------------------------------

def _mouth(canvas, theme, cx, top, bottom, tip, base, lit):
    """A groove running off the page, ending in an arrowhead the shape of the scroll button's.
    `top`..`bottom` is the groove; the head's point is at `tip` and its back at `base`."""
    groove = rect_mask((cx - 4, top, cx + 4, bottom), canvas.size)
    head = poly_mask([(cx, tip), (cx + 11, base), (cx - 11, base)], canvas.size)
    both = groove | head
    # break the frame or ledge open around the path
    outline = dilate(dilate(both)) & ~both
    # on the lower view the head sits under the title: the outline must not nick the letters
    outline[:TITLE_BOTTOM] = False
    canvas.mask(outline, col("iron", 0))
    canvas.mask((shift(both, 0, 1) | shift(both, 1, 1)) & ~dilate(both), theme.s(4))
    if lit:
        layer = Canvas(*canvas.size)
        paint_glow(layer, theme, groove, depth(groove))
        canvas.paste(layer)
        canvas.mask(head, theme.g(3))
        canvas.mask(head & ~shift(head, 0, 1 if tip < base else -1), theme.g(4))
    else:
        canvas.mask(groove, col("iron", 1))
        canvas.mask(groove & ~shift(groove, 1, 0), col("iron", 0))
        # the same pale steel as a usable scroll arrow, one step quieter: "the path goes on"
        canvas.mask(head, col("steel", 3))
        canvas.mask(head & ~shift(head, 0, 1), col("steel", 4))


def paths_down(canvas, theme):
    """Upper view: under n4 and n6 the paths break through the ledge toward the sealed keystones."""
    for column in EDGE_COLUMNS:
        x0, _, _, y1 = slot_art(36 + column)
        _mouth(canvas, theme, x0 + 18, y1 - 6, y1 + 3, tip=y1 + 9, base=y1 + 1, lit=False)


def paths_up(canvas, theme, lit_columns=()):
    """Lower view: the paths from n2 and n3 come in through the lintel into n4 and n6. A column
    in `lit_columns` has both ends of that connection owned."""
    for column in EDGE_COLUMNS:
        x0, y0, _, _ = slot_art(column)
        _mouth(canvas, theme, x0 + 18, y0 - 3, y0 + 4, tip=y0 - 8, base=y0 - 1, lit=column in lit_columns)
