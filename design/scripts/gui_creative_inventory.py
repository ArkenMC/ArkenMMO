"""The creative inventory, re-themed like the survival inventory (gui_inventory.py): iron, parchment, gold.

Writes three 512x512 backgrounds (art in the top-left 390x272 = vanilla 195x136 on the 2x grid) to
textures/gui/container/creative_inventory/ and the 30 sprites (tabs, scrollers) to
textures/gui/sprites/container/creative_inventory/. Spec: design/gui-inventory.md.
Fails when a cell, field or track is off the vanilla layout, so a slip breaks the build, not the screen.
"""
import numpy as np

from pixelkit import chrome, layout
from pixelkit.chrome import DARK, RIM, gem, slot_cell
from pixelkit.draw import Canvas, dilate, frame, shift
from pixelkit.layout import DENSITY, art
from pixelkit.palette import PALETTE, col

BACKGROUNDS = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "container" / "creative_inventory"
SPRITES = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "container" / "creative_inventory"
FILE = (512, 512)
GUI = (195, 136)
CANVAS = (GUI[0] * DENSITY, GUI[1] * DENSITY)
TAB_GUI = (26, 32)
SCROLLER_GUI = (12, 15)
SLOT = layout.SLOT

XS = [8 + SLOT * c for c in range(9)]
ITEM_CELLS = [(x, y) for y in (17, 35, 53, 71, 89, 111) for x in XS]
INVENTORY_CELLS = [(53, 5), (53, 32), (107, 5), (107, 32), (34, 19)] + [(x, y) for y in (53, 71, 89, 111) for x in XS]
DESTROY = (172, 111)
# Measured from vanilla 26.2 (every 18x18 cell: 55 grey top-left ring, 139 floor, white bottom-right), kept literal.
MEASURED_ITEMS = sorted((x, y) for y in (17, 35, 53, 71, 89, 111) for x in (8, 26, 44, 62, 80, 98, 116, 134, 152))
MEASURED_INVENTORY = sorted([(53, 5), (107, 5), (34, 19), (53, 32), (107, 32)]
                            + [(x, y) for y in (53, 71, 89, 111) for x in (8, 26, 44, 62, 80, 98, 116, 134, 152)])
MEASURED_DESTROY = (172, 111)  # a cell whose floor is red with a dark X in vanilla
MODEL_OUTER, MODEL_BOX = (72, 5, 106, 50), (73, 6, 105, 49)
TRACK = (174, 17, 188, 129)
SEARCH_FIELD = (80, 4, 170, 16)
# the game draws the category title at (8, 6) in #404040; the survival tab and the search tab differ (see spec)
ITEMS_PLATE, SEARCH_PLATE = (5, 4, 130, 15), (5, 4, 76, 15)
TAB_TOP_Y, TAB_BOTTOM_Y = -28, GUI[1] - 4
SEPARATOR_TOP = 108 * DENSITY


def tab_x(column):
    """Left edge of a tab column in GUI px; the seventh column is right-aligned to the panel."""
    return 27 * column if column < 6 else GUI[0] - 27 + 1


def cell_rect(origin):
    return art((origin[0], origin[1], origin[0] + SLOT, origin[1] + SLOT))


def recess(canvas, outer, box, floor_line=False):
    """A calm sunken box: dark wall top and left, lighter lip bottom and right, one dark iron floor."""
    frame(canvas, art(outer), [(DARK, col("iron", 4)), (col("iron", 0), col("iron", 2))])
    x0, y0, x1, y1 = art(box)
    canvas.rect((x0, y0, x1, y1), col("iron", 1))
    if floor_line:
        canvas.rect((x0, y1 - 16, x1, y1), col("iron", 0))
        canvas.rect((x0, y1 - 16, x1, y1 - 15), col("iron", 2))


def sunk(canvas, rect):
    """Track or field: a two-ring wall around an iron 1 floor; the floor is exactly the vanilla inner size."""
    x0, y0, x1, y1 = art(rect)
    frame(canvas, (x0, y0, x1, y1), [(DARK, col("iron", 4)), (DARK, col("iron", 3))])
    canvas.rect((x0 + 2, y0 + 2, x1 - 2, y1 - 2), col("iron", 1))


def title_plate(canvas, plate, with_gem, rule):
    """Parchment plate behind the category title, built like the menus' "Inventory" plate."""
    px0, py0, px1, py1 = art(plate)
    frame(canvas, (px0, py0 + 1, px1, py1), [(DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((px0 + 2, py0 + 3, px1 - 2, py1 - 2), col("parchment", 2))
    middle = (py0 + py1) // 2
    if with_gem:
        gem(canvas, px1 - 8, middle + 1, 4)
    if rule:
        width = CANVAS[0]
        canvas.rect((px1 + 5, middle, width - 18, middle + 1), DARK)
        canvas.rect((px1 + 5, middle + 1, width - 18, middle + 2), col("iron", 4))
        gem(canvas, width - 16, middle + 1, 3)


def separator(canvas, right):
    """The gold rule between the main rows and the hotbar, as in the survival inventory; it stops short of the track."""
    canvas.rect((7, SEPARATOR_TOP, right, SEPARATOR_TOP + 2), DARK)
    canvas.rect((7, SEPARATOR_TOP + 2, right, SEPARATOR_TOP + 3), col("gold", 2))
    canvas.rect((7, SEPARATOR_TOP + 3, right, SEPARATOR_TOP + 4), DARK)


def destroy_slot(canvas):
    """A cell with a darker floor and a steel X: it reads as "destroy" by shape, not by colour."""
    x0, y0, x1, y1 = cell_rect(DESTROY)
    slot_cell(canvas, (x0, y0, x1, y1))
    canvas.rect((x0 + 3, y0 + 3, x1 - 3, y1 - 3), col("iron", 1))
    rows, width = 22, 26
    mask = np.zeros(canvas.px.shape[:2], bool)
    left, top = x0 + 3 + (30 - width) // 2, y0 + 3 + (30 - rows) // 2
    for r in range(rows):
        mask[top + r, left + r:left + r + 5] = True
        mask[top + r, left + rows - 1 - r:left + rows + 4 - r] = True
    canvas.mask(dilate(mask), DARK)
    canvas.mask(mask, col("steel", 5))
    canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 6))


def background(kind):
    canvas = Canvas(*CANVAS)
    chrome.shell(canvas, CANVAS)
    cells = INVENTORY_CELLS if kind == "inventory" else ITEM_CELLS
    separator(canvas, CANVAS[0] - 7 if kind == "inventory" else art(TRACK)[0] - 4)
    if kind == "inventory":
        recess(canvas, MODEL_OUTER, MODEL_BOX, floor_line=True)
    else:
        sunk(canvas, TRACK)
        title_plate(canvas, ITEMS_PLATE if kind == "items" else SEARCH_PLATE, kind == "items", kind == "items")
    if kind == "search":
        sunk(canvas, SEARCH_FIELD)
    for origin in cells:
        slot_cell(canvas, cell_rect(origin))
    if kind == "inventory":
        destroy_slot(canvas)
    full = Canvas(*FILE)
    full.px[:CANVAS[1], :CANVAS[0]] = canvas.px
    return full


# ---- sprites ----

def _unselected_rim():
    iron = lambda s: col("iron", s)  # noqa: E731
    return [(DARK, DARK), (DARK, DARK), (iron(4), iron(1)), (iron(3), iron(1)), (iron(2), iron(0)), (iron(2), iron(0)),
            (DARK, iron(2))]


def _gold_crest(canvas, top):
    """A gold line along the open tab's outer edge, away from the corners, so the side walls stay the panel's."""
    w, h = canvas.size
    y = 2 if top else h - 3
    canvas.rect((6, y, w - 6, y + 1), col("gold", 4 if top else 1))


def tab_sprite(top, selected, column):
    """One 52x64 tab. The selected one is the panel's iron and opens into it over the 4 GUI px it overlaps."""
    w, h = (v * DENSITY for v in TAB_GUI)
    body = col("iron", 2) if selected else col("iron", 1)
    rim = RIM if selected else _unselected_rim()
    canvas = Canvas(w, h)
    # the tab's open end is drawn past the sprite, so no rim shows there
    if top:
        start = 0 if selected else 4
        edge = (0, start, w, h + 100)
        canvas.rect((0, start, w, h), body)
    else:
        end = h if selected else h - 8
        edge = (0, -100, w, end)
        canvas.rect((0, 0, w, end), body)
    frame(canvas, edge, rim)
    shape = np.ones((h, w), bool)
    if top:
        shape[:start] = False
        rows = [(start, 4), (start + 1, 4), (start + 2, 2), (start + 3, 2)]
    else:
        shape[end:] = False
        rows = [(end - 1, 4), (end - 2, 4), (end - 3, 2), (end - 4, 2)]
    for y, cut in rows:
        shape[y, :cut] = False
        shape[y, w - cut:] = False
    # a 2 px dark outline along the cut corners
    outline = shape & dilate(dilate(~shape))
    zone = np.zeros_like(shape)
    if top:
        zone[start:start + 8] = True
    else:
        zone[end - 8:end] = True
    canvas.px[~shape] = 0
    canvas.mask(outline & zone, DARK)
    if selected:
        _gold_crest(canvas, top)
        # the overlap rows: panel body runs straight through, but tab 1 and 7 keep the panel's side wall
        open_row = h - 1 if top else 0
        keep_left, keep_right = column == 0, column == 6
        x0, x1 = (7 if keep_left else 0), (w - 7 if keep_right else w)
        canvas.rect((x0, open_row, x1, open_row + 1), body)
    return canvas


def scroller(enabled):
    w, h = (v * DENSITY for v in SCROLLER_GUI)
    ramp, hi, lo = ("gold", 4, 1) if enabled else ("iron", 3, 1)
    canvas = Canvas(w, h)
    frame(canvas, (0, 0, w, h), [(DARK, DARK), (col(ramp, hi), col(ramp, lo)), (col(ramp, hi - 1), col(ramp, lo + 1))])
    canvas.rect((3, 3, w - 3, h - 3), col(ramp, 3 if enabled else 2))
    for y in (10, 14, 18):
        canvas.rect((6, y, w - 6, y + 1), col(ramp, lo))
        canvas.rect((6, y + 1, w - 6, y + 2), col(ramp, hi))
    return canvas


def sprites():
    out = {"scroller": scroller(True), "scroller_disabled": scroller(False)}
    for top, name in ((True, "top"), (False, "bottom")):
        for selected in (True, False):
            for column in range(7):
                out[f"tab_{name}_{'selected' if selected else 'unselected'}_{column + 1}"] = tab_sprite(top, selected, column)
    return out


# ---- checks ----

def _tones(px, rect):
    x0, y0, x1, y1 = rect
    return {tuple(int(v) for v in p[:3]) for p in px[y0:y1, x0:x1].reshape(-1, 4)}


def _iron(step):
    return tuple(col("iron", step)[:3])


def check_cells(px, cells, floor, errors, label):
    dark = tuple(DARK[:3])
    for origin in cells:
        x0, y0, x1, y1 = cell_rect(origin)
        at = lambda x, y: tuple(int(v) for v in px[y, x, :3])  # noqa: E731
        walls = ({at(x, y0 + 1) for x in range(x0 + 1, x1 - 2)} | {at(x0 + 1, y) for y in range(y0 + 1, y1 - 2)},
                 {at(x, y1 - 2) for x in range(x0 + 2, x1 - 1)} | {at(x1 - 2, y) for y in range(y0 + 2, y1 - 1)})
        # the dark inner wall sits exactly one art px inside the cell: a shifted cell breaks this
        if walls != ({dark}, {_iron(4)}):
            errors.append(f"{label} cell {origin} is off the vanilla grid")
        if at(x0 + 3, y0 + 3) != floor(origin) or at(x1 - 4, y1 - 4) != floor(origin):
            errors.append(f"{label} cell {origin} has the wrong floor")
        if at(x0, y0 + 1) == dark or at(x0 + 1, y0) == dark:
            errors.append(f"{label} cell {origin} has dark edge outside its rect")


def check_background(kind, canvas, errors):
    px = canvas.px
    label = f"{kind}"
    cells = INVENTORY_CELLS if kind == "inventory" else ITEM_CELLS
    measured = MEASURED_INVENTORY if kind == "inventory" else MEASURED_ITEMS
    if sorted(cells) != measured:
        errors.append(f"{label}: generated cells differ from the measured vanilla slots")
    if px[:, CANVAS[0]:, 3].any() or px[CANVAS[1]:, :, 3].any():
        errors.append(f"{label}: art outside 390x272")
    inside = px[:CANVAS[1], :CANVAS[0], 3]
    if int((inside == 0).sum()) != 16 or not set(inside.flatten().tolist()) <= {0, 255}:
        errors.append(f"{label}: alpha must be binary with only the 4 corner texels (2x2 each) clear")
    check_cells(px, cells, lambda origin: _iron(3), errors, label)
    if kind == "inventory":
        if DESTROY != MEASURED_DESTROY:
            errors.append("destroy slot moved")
        check_cells(px, [DESTROY], lambda origin: _iron(1), errors, "destroy")
        if _tones(px, art(MODEL_BOX)) != {_iron(0), _iron(1), _iron(2)}:
            errors.append("the model box must hold only its three calm iron tones")
    else:
        if _tones(px, tuple(v + 2 for v in art(TRACK)[:2]) + tuple(v - 2 for v in art(TRACK)[2:])) != {_iron(1)}:
            errors.append("the scroll track must stay plain")
    if kind == "search":
        x0, y0, x1, y1 = art(SEARCH_FIELD)
        if _tones(px, (x0 + 2, y0 + 2, x1 - 2, y1 - 2)) != {_iron(1)}:
            errors.append("the search field must stay plain")
        px0, py0, px1, py1 = art(SEARCH_PLATE)
        if px1 >= x0:
            errors.append("the title plate must stay clear of the search field")


def check_sprites(images, errors):
    for name, canvas in images.items():
        w, h = canvas.size
        expected = tuple(v * DENSITY for v in (SCROLLER_GUI if name.startswith("scroller") else TAB_GUI))
        if (w, h) != expected:
            errors.append(f"{name}: size {w}x{h}, want {expected}")
        alpha = set(canvas.px[..., 3].flatten().tolist())
        if not alpha <= {0, 255}:
            errors.append(f"{name}: alpha must be binary")
    pairs = (("top", "selected"), ("bottom", "selected"))
    for kind, state in pairs:
        middle = images[f"tab_{kind}_{state}_2"].px
        if any((images[f"tab_{kind}_{state}_{i}"].px != middle).any() for i in range(3, 7)):
            errors.append(f"tab_{kind}_{state} 2..6 must be identical")
        for column in (1, 7):
            if not (images[f"tab_{kind}_{state}_{column}"].px != middle).any():
                errors.append(f"tab_{kind}_{state}_{column} must differ from the middle tabs")


def palette_errors(images):
    known = {c for ramp in PALETTE.values() for c in ramp}
    stray = {tuple(int(v) for v in p[:3]) for image in images for p in image.px[image.px[..., 3] > 0]} - known
    return [f"colours outside the palette: {sorted(stray)}"] if stray else []


def colours(canvas):
    return len({tuple(p) for p in canvas.px[canvas.px[..., 3] > 0].reshape(-1, 4)})


def main():
    backgrounds = {name: background(name) for name in ("inventory", "items", "search")}
    images = sprites()
    errors = palette_errors(list(backgrounds.values()) + list(images.values()))
    for name, canvas in backgrounds.items():
        check_background(name, canvas, errors)
    check_sprites(images, errors)
    if errors:
        raise ValueError("creative inventory: " + "; ".join(errors))
    BACKGROUNDS.mkdir(parents=True, exist_ok=True)
    SPRITES.mkdir(parents=True, exist_ok=True)
    files = {"inventory": "tab_inventory", "items": "tab_items", "search": "tab_item_search"}
    for name, canvas in backgrounds.items():
        canvas.image().save(BACKGROUNDS / f"{files[name]}.png")
        print(f"{files[name]}.png: {colours(canvas)} colours, 512x512")
    for name, canvas in images.items():
        canvas.image().save(SPRITES / f"{name}.png")
    total = {tuple(p) for image in images.values() for p in image.px[image.px[..., 3] > 0].reshape(-1, 4)}
    print(f"{len(images)} sprites written, {len(total)} colours in all of them together")


if __name__ == "__main__":
    main()
