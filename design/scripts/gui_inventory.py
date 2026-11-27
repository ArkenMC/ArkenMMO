"""The player (survival) inventory screen, re-themed in the iron, parchment and gold of the skill menus.

Writes resourcepack/assets/minecraft/textures/gui/container/inventory.png: 512x512, art in the
top-left 352x332 (the vanilla 176x166 on the 2x grid), everything else clear, plus two fully clear
recipe book button sprites (the button is hidden everywhere). Spec: design/gui-inventory.md.
Fails when a cell is off the vanilla slot grid, so a layout slip breaks the build instead of the screen.
"""
import numpy as np
from PIL import Image

import gui_slot_icons
import items_accessories
from pixelkit import chrome, invdecor, layout, rounded
from pixelkit.chrome import DARK, corner_bracket, gem, slot_cell
from pixelkit.draw import Canvas, dilate, frame, poly_mask, shift
from pixelkit.layout import DENSITY, art
from pixelkit.palette import PALETTE, col

OUT = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "container" / "inventory.png"
RECIPE_SPRITES = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "recipe_book"
RECIPE_SIZE = (40, 36)  # vanilla 20x18 GUI px on the 2x grid; the sprite stretches to the drawn size
FILE = (512, 512)
# vanilla GUI size; the rest of the 256x256 file (and of our 512x512) stays transparent
GUI = (176, 166)
CANVAS = (GUI[0] * DENSITY, GUI[1] * DENSITY)

SLOT = layout.SLOT
ARMOUR = [(7, 7 + SLOT * i) for i in range(4)]
OFFHAND = (76, 61)
CRAFTING = [(97 + SLOT * c, 17 + SLOT * r) for r in range(2) for c in range(2)]
RESULT = (153, 27)
STORAGE = [(7 + SLOT * c, 83 + SLOT * r) for r in range(3) for c in range(9)]
HOTBAR = [(7 + SLOT * c, 141) for c in range(9)]
# Top-left corner of every 18x18 cell, measured from vanilla 26.2 inventory.png (46 cells).
MEASURED = sorted([(7, 7), (97, 17), (115, 17), (7, 25), (153, 27), (97, 35), (115, 35), (7, 43), (7, 61), (76, 61)]
                  + [(7 + 18 * c, y) for y in (83, 101, 119, 141) for c in range(9)])
# Four flat recessed regions without cell frames: the character panel (armour, model box and the four storage
# cells under it), the L-shaped main inventory block (the other 23 storage cells), the hotbar bar (cells 1..8)
# and the crafting block (behind the 2x2, arrow and result, whose framed cells stay). The game still draws items
# and ghost icons at cell + 1. The offhand cell and the ninth hotbar cell have no art at all: plain shell colour
# (an item in the offhand slot still renders there).
PANEL_CELLS = STORAGE[:4]
BLOCK_CELLS = STORAGE[4:9] + STORAGE[9:]
BAR_CELLS = HOTBAR[:8]
SHELL_CELLS = [OFFHAND]
# the four storage cells in the character panel are the accessory slots (ring, ring, amulet, bracelet): their item
# areas hold a faint silhouette painted into the texture, since a pack cannot give a storage slot a ghost icon
ACCESSORY_SLOTS = dict(zip(PANEL_CELLS, ("ring", "ring", "amulet", "bracelet")))
# framed sockets: the armour column, the crafting grid and result, and the ninth hotbar cell (gold ring, set apart
# from the bar like the result)
SOCKET_GOLD = [RESULT, HOTBAR[8]]
MODEL_OUTER = (25, 7, 76, 79)
# the arched brick niche behind the player model (GUI px) and the top of the dais the model's feet stand on
ALCOVE = (25, 7, 77, 79)
DAIS_TOP = 71
# fluted column between the panel and the crafting block, above the offhand slot, and the crest under the
# crafting block (art px)
PILLAR = (162, 14, 186, 160)
CREST_CENTRE = (267, 134)
# Region shapes in GUI px (every step of every outline is a whole GUI px, so a multiple of 2 art px). A region
# reaches 1 GUI px beyond its cells where there is room. Where cells are contiguous the panel stops 1 GUI px
# inside its cells (on the item area's edge) and the block starts 1 GUI px inside its own, which leaves
# 2 GUI px: ring, 2 art px of shell, ring.
PANEL_BOX = (6, 6, 78, 100)
BLOCK_BOXES = [(79, 82, 170, 102), (6, 102, 170, 138)]
BLOCK_CORNERS = [(80, 82, 1, 1), (169, 82, -1, 1), (6, 137, 1, -1), (169, 137, -1, -1), (6, 102, 1, 1)]
BAR_BOX = (6, 140, 151, 160)
CRAFT_BOX = (96, 16, 171, 54)
SEAM = 2  # GUI px between the panel and the block
FILL = col("iron", 3)
CRAFT_FILL = col("iron", 1)
# survival inventory title: the game draws "Crafting" at (97, 6), 8 px font, cap height 7 (rows y6..y13)
TITLE_PLATE = (94, 4, 163, 15)
# arrow between the crafting grid and the result, in GUI px: shaft x135..150, head to x151
ARROW_TIP = (151, 35.5)
# the gold rule: art row of its top and where it starts (just right of the panel's edge)
RULE_TOP = 79 * DENSITY
RULE_START = 81 * DENSITY
RULE_END = CANVAS[0] - 18
RULE_GEM = (CANVAS[0] - 13, RULE_TOP + 1)


def cells():
    return ARMOUR + [OFFHAND] + CRAFTING + [RESULT] + STORAGE + HOTBAR


def drawn_cells():
    hidden = set(PANEL_CELLS + BLOCK_CELLS + BAR_CELLS + SHELL_CELLS)
    return [origin for origin in cells() if origin not in hidden]


def region_cells():
    return {"panel": PANEL_CELLS, "block": BLOCK_CELLS, "bar": BAR_CELLS}


def grid_cells():
    """The panel row has no hairlines: its cells are the accessory slots, set apart from each other by their icons."""
    return {name: group for name, group in region_cells().items() if name != "panel"}


def cell_rect(origin):
    return art((origin[0], origin[1], origin[0] + SLOT, origin[1] + SLOT))


def rect_mask(rects):
    mask = np.zeros(CANVAS[::-1], bool)
    for x0, y0, x1, y1 in rects:
        mask[y0:y1, x0:x1] = True
    return mask


def shell_mask():
    return rounded.upscale(rounded.rounded_box(GUI, (0, 0) + GUI))


def shell(canvas):
    """Iron body with the menus' bevelled rim, following the stepped corners, and a soft shadow just inside the
    rim along the top and left."""
    mask = shell_mask()
    canvas.mask(mask, col("iron", 2))
    number, lit = rounded.rings(mask, inside=True)
    canvas.mask(((number == 8) | (number == 9)) & lit, col("iron", 1))
    for index, (top_left, bottom_right) in enumerate(chrome.RIM):
        ring = number == index + 1
        canvas.mask(ring & lit, top_left)
        canvas.mask(ring & ~lit, bottom_right)


def region_masks():
    """Fill masks (art px) of the four regions. The block is cut back from the panel by a diamond, so the gap
    is constant and the block's inner corner follows the panel's rounded corner step for step."""
    panel = rounded.rounded_box(GUI, PANEL_BOX)
    block = np.zeros(GUI[::-1], bool)
    for box in BLOCK_BOXES:
        block |= rounded.rect(GUI, box)
    block &= ~rounded.grow(panel, SEAM)
    for x, y, sx, sy in BLOCK_CORNERS:
        rounded.cut_corner(block, x, y, sx, sy)
    bar = rounded.rounded_box(GUI, BAR_BOX)
    craft = rounded.rounded_box(GUI, CRAFT_BOX)
    return {name: rounded.upscale(mask) for name, mask in
            (("panel", panel), ("block", block), ("bar", bar), ("craft", craft))}


def inner_shadow(canvas, fill, colour):
    """A 1 GUI px darker band just inside the top and left edges, where there is room."""
    band = np.zeros_like(fill)
    for step in (1, 2):
        band |= fill & ~np.roll(fill, step, axis=1)
        band |= fill & ~np.roll(fill, step, axis=0)
    # never inside a cell: where regions meet, the edge ring is the only edge
    items = rect_mask(list(map(cell_rect, cells())))
    canvas.mask(band & ~items, colour)


def recessed_regions(canvas):
    """Flat recessed regions in the cells' own style: a dark ring top/left, a lit one bottom/right, 1 art px each."""
    masks = region_masks()
    keep = ~rect_mask([(x0 + 1, y0 + 1, x1 - 1, y1 - 1) for x0, y0, x1, y1 in map(cell_rect, drawn_cells())])
    taken = np.logical_or.reduce(list(masks.values()))
    for name, fill in masks.items():
        colour = CRAFT_FILL if name == "craft" else FILL
        canvas.mask(fill, colour)
        inner_shadow(canvas, fill, DARK if name == "craft" else col("iron", 2))
    for fill in masks.values():
        number, lit = rounded.rings(fill, inside=False)
        ring = (number == 1) & keep & ~taken
        canvas.mask(ring & lit, DARK)
        canvas.mask(ring & ~lit, col("iron", 4))


def ghost_origin(origin):
    """Art px of the item area (cell + 1 GUI px, 16x16 GUI px) where the game draws items and ghost icons."""
    return (origin[0] + 1) * DENSITY, (origin[1] + 1) * DENSITY


def accessory_ghosts(canvas):
    """Paint the ring, amulet and bracelet silhouettes (vanilla's ghost language) under the four accessory cells."""
    icons = gui_slot_icons.accessory_icons()
    for origin, name in ACCESSORY_SLOTS.items():
        x, y = ghost_origin(origin)
        sprite = np.asarray(icons[name])
        solid = sprite[..., 3] > 0
        canvas.px[y:y + 32, x:x + 32][solid] = sprite[solid]


def title_plate(canvas):
    """Parchment plate behind the vanilla title, ending in a gold gem; built like the menu's "Inventory" plate."""
    px0, py0, px1, py1 = art(TITLE_PLATE)
    shadow = np.zeros(CANVAS[::-1], bool)
    shadow[py0 + 2:py1 + 2, px0 + 2:px1 + 2] = True
    shadow[py0:py1, px0:px1] = False
    canvas.mask(shadow, col("iron", 1))
    frame(canvas, (px0, py0, px1, py1), [(DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((px0 + 2, py0 + 2, px1 - 2, py1 - 2), col("parchment", 2))
    gem(canvas, px1 - 8, (py0 + py1) // 2, 4)


def separator(canvas):
    """The gold rule that closes the crafting area; it starts beyond the panel's edge instead of crossing it."""
    top = RULE_TOP
    width = CANVAS[0]
    canvas.rect((RULE_START, top, RULE_END, top + 2), DARK)
    canvas.rect((RULE_START, top + 2, RULE_END, top + 3), col("gold", 2))
    canvas.rect((RULE_START, top + 3, RULE_END, top + 4), DARK)
    gem(canvas, *RULE_GEM, 2)


def arrow(canvas):
    """Gold block arrow pointing at the result, the same build as the menus' page arrow."""
    tip_x, cy = (round(v * DENSITY) for v in ARROW_TIP)
    shape = [(-32, -6), (-14, -6), (-14, -13), (-12, -13), (0, -1), (0, 1), (-12, 13), (-14, 13), (-14, 6), (-32, 6)]
    mask = poly_mask([(tip_x + x, cy + y) for x, y in shape], canvas.size)
    backing = dilate(dilate(mask))
    canvas.mask(backing | shift(backing, 0, 2), DARK)
    canvas.mask(mask, col("gold", 4))
    lower = mask.copy()
    lower[:cy] = False
    canvas.mask(lower, col("gold", 3))


def build():
    canvas = Canvas(*CANVAS)
    shell(canvas)
    title_plate(canvas)
    separator(canvas)
    recessed_regions(canvas)
    invdecor.grid(canvas, grid_cells(), region_masks())
    invdecor.studs(canvas, region_cells(), region_masks())
    accessory_ghosts(canvas)
    invdecor.alcove(canvas, GUI, ALCOVE, DAIS_TOP)
    for origin in drawn_cells():
        # the crafting result and the ninth hotbar cell get a bright gold first ring on all four sides
        outer = (col("gold", 3), col("gold", 3)) if origin in SOCKET_GOLD else None
        slot_cell(canvas, cell_rect(origin), outer)
    arrow(canvas)
    invdecor.pillar(canvas, *PILLAR)
    invdecor.crest(canvas, *CREST_CENTRE)
    for x, dx in ((4, 1), (CANVAS[0] - 4, -1)):
        for y, dy in ((4, 1), (CANVAS[1] - 4, -1)):
            corner_bracket(canvas, x, y, dx, dy, 11)
    full = Canvas(*FILE)
    full.px[:CANVAS[1], :CANVAS[0]] = canvas.px
    return full


# one pixel of each region's outermost GUI px corner: it must be empty (art px)
CORNER_PIXELS = {"panel": [(12, 12), (155, 12), (12, 199), (155, 199)],
                 "block": [(160, 164), (339, 164), (12, 275), (339, 275), (12, 204)],
                 "bar": [(12, 280), (301, 280), (12, 319), (301, 319)],
                 "craft": [(192, 32), (341, 32), (192, 107), (341, 107)]}


def check(canvas):
    """Fail on anything that would misalign with vanilla or break the pack rules."""
    px = canvas.px
    errors = []
    if sorted(cells()) != MEASURED:
        errors.append("generated cell origins differ from the measured vanilla slots")
    if px[:, CANVAS[0]:, 3].any() or px[CANVAS[1]:, :, 3].any():
        errors.append("art outside the 352x332 area")
    inside = px[:CANVAS[1], :CANVAS[0], 3]
    if not set(inside.flatten().tolist()) <= {0, 255}:
        errors.append("alpha must be binary")
    if ((inside > 0) != shell_mask()).any():
        errors.append("the silhouette must be the stepped rounded rectangle, with nothing clear inside it")
    if inside[0, 0] or inside[0, -1] or inside[-1, 0] or inside[-1, -1] or not inside[6, 6]:
        errors.append("the four outer corners must be clear and rounded")
    known = {c for ramp in PALETTE.values() for c in ramp}
    stray = {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]} - known
    if stray:
        errors.append(f"colours outside the palette: {sorted(stray)}")
    iron = {name: tuple(col("iron", step)[:3]) for name, step in (("body", 2), ("lip", 4), ("fill", 3))}
    dark = tuple(DARK[:3])
    at = lambda x, y: tuple(int(v) for v in px[y, x, :3])  # noqa: E731
    for origin in drawn_cells():
        x0, y0, x1, y1 = cell_rect(origin)
        top = {at(x, y0 + 1) for x in range(x0 + 1, x1 - 2)}
        left = {at(x0 + 1, y) for y in range(y0 + 1, y1 - 2)}
        bottom = {at(x, y1 - 2) for x in range(x0 + 2, x1 - 1)}
        right = {at(x1 - 2, y) for y in range(y0 + 2, y1 - 1)}
        # the dark inner wall sits exactly one art px inside the cell: a shifted cell breaks one of these
        if top != {dark} or left != {dark} or bottom != {iron["lip"]} or right != {iron["lip"]}:
            errors.append(f"cell {origin} is off the vanilla grid")
        if at(x0 + 3, y0 + 3) != iron["fill"] or at(x1 - 4, y1 - 4) != iron["fill"]:
            errors.append(f"cell {origin} has no recessed floor")
        if at(x0, y0 + 1) == dark or at(x0 + 1, y0) == dark:
            errors.append(f"cell {origin} has dark edge outside its rect")
    masks = region_masks()
    # every outline step lies on the GUI pixel grid: rows and columns come in identical pairs
    for name, mask in {"shell": shell_mask(), **masks}.items():
        if not (mask[0::2] == mask[1::2]).all() or not (mask[:, 0::2] == mask[:, 1::2]).all():
            errors.append(f"{name} has a step off the GUI pixel grid")
    # cells without a frame: the item area (cell + 1 GUI px) is flat fill apart from its outermost GUI px, which
    # may hold a rounded corner cut. Ninth hotbar cell and offhand: plain shell
    fill = tuple(FILL[:3])
    shrink = lambda r: (r[0] + 4, r[1] + 4, r[2] - 4, r[3] - 4)  # noqa: E731
    flat = [(shrink(cell_rect(origin)), fill) for origin in BLOCK_CELLS + BAR_CELLS]
    ox0, oy0, ox1, oy1 = shrink(cell_rect(OFFHAND))
    # the panel's right ring reaches the cell's first columns, and the pillar stands over the rest of the cell
    flat += [((ox0 + 2, oy0, PILLAR[0], oy1), iron["body"])]
    for (x0, y0, x1, y1), colour in flat:
        if {tuple(int(v) for v in p[:3]) for p in px[y0:y1, x0:x1].reshape(-1, 4)} != {colour}:
            errors.append(f"area {(x0, y0, x1, y1)} is not one flat colour")
    # the four accessory cells: the same area is the fill plus exactly the ghost icon, whose colours are its only others
    icons = gui_slot_icons.accessory_icons()
    for origin, name in ACCESSORY_SLOTS.items():
        sx0, sy0, sx1, sy1 = shrink(cell_rect(origin))
        gx, gy = ghost_origin(origin)
        sprite = np.asarray(icons[name])
        expected = np.tile(np.array(fill + (255,), np.uint8), (32, 32, 1))
        expected[sprite[..., 3] > 0] = sprite[sprite[..., 3] > 0]
        got = px[gy:gy + 32, gx:gx + 32]
        if (got[2:30, 2:30] != expected[2:30, 2:30]).any() or not (sx0, sy0) == (gx + 2, gy + 2):
            errors.append(f"accessory cell {origin} ({name}): item area is not the fill plus its ghost icon")
        # every placeholder pixel is hidden by each item that belongs in the cell: the 16x16 item texture drawn at the
        # item origin, 1 texel = 2x2 art px, leaves no placeholder-coloured pixel in the item area
        for item in gui_slot_icons.COVERS[name]:
            shown = np.kron(items_accessories.DRAW[item]()[..., 3] > 0, np.ones((2, 2), bool))
            if ((got[..., 3] > 0) & (got[..., :3] == np.array(gui_slot_icons.TONE[:3])).all(axis=-1) & ~shown).any():
                errors.append(f"accessory cell {origin}: the placeholder shows beside the {item} item")
        colours = {tuple(int(v) for v in p[:3]) for p in got[2:30, 2:30].reshape(-1, 4)}
        if not colours == {fill, tuple(gui_slot_icons.TONE[:3])}:
            errors.append(f"accessory cell {origin}: colours other than the fill and the icon's one tone")
    for origin in CRAFTING + [RESULT]:
        x0, y0, x1, y1 = cell_rect(origin)
        if not masks["craft"][y0:y1, x0:x1].all():
            errors.append(f"crafting cell {origin} is not inside the crafting block")
    for origin in PANEL_CELLS + BLOCK_CELLS + BAR_CELLS:
        x0, y0, x1, y1 = cell_rect(origin)
        owner = [m for m in (masks["panel"], masks["block"], masks["bar"]) if m[y0 + 2:y1 - 2, x0 + 2:x1 - 2].sum() > 200]
        if len(owner) != 1:
            errors.append(f"cell {origin} is not inside exactly one region")
    # one straight right edge for the whole panel, centred on the column boundary x79 (the gap is art x156..159)
    edge = [int(np.nonzero(masks["panel"][y])[0].max()) for y in range(34, 190)]
    if set(edge) != {155}:
        errors.append("the panel's right edge is not one straight line")
    gap = masks["block"][34:190, 156:160]
    if gap.any():
        errors.append("the seam between panel and block must stay free")
    for name, points in CORNER_PIXELS.items():
        if any(masks[name][y, x] for x, y in points):
            errors.append(f"{name} has a square corner")
        if masks[name].sum() < 5000:
            errors.append(f"{name} is missing")
    overlap = [(a, b) for a in masks for b in masks if a < b and (masks[a] & masks[b]).any()]
    if overlap:
        errors.append(f"regions overlap: {overlap}")
    # the two gold sockets have one bright gold ring on all four sides
    gold3 = tuple(col("gold", 3)[:3])
    for origin in SOCKET_GOLD:
        x0, y0, x1, y1 = cell_rect(origin)
        ring = {at(x, y0) for x in range(x0 + 2, x1 - 2)} | {at(x, y1 - 1) for x in range(x0 + 2, x1 - 2)}
        ring |= {at(x0, y) for y in range(y0 + 2, y1 - 2)} | {at(x1 - 1, y) for y in range(y0 + 2, y1 - 2)}
        if ring != {gold3}:
            errors.append(f"socket {origin}: the gold ring is not one bright gold on all four sides")
    # the pillar's gold base stands on the gold rule: its last row touches the rule's top row
    if PILLAR[3] != RULE_TOP + 2 or at((PILLAR[0] + PILLAR[2]) // 2, RULE_TOP + 1) != dark:
        errors.append("the pillar must end on the gold rule")
    # the grid lines lie in the margins: the 1 art px line between two gridless cells is the grid colour
    line = tuple(col("iron", 4)[:3])
    for a, b, vertical in ((BLOCK_CELLS[0], BLOCK_CELLS[1], True), (BAR_CELLS[0], BAR_CELLS[1], True),
                           (BLOCK_CELLS[0], STORAGE[9 + 4], False)):
        x0, y0, _, _ = cell_rect(b)
        probe = (x0 - 1, y0 + 18) if vertical else (x0 + 18, y0 - 1)
        if at(*probe) != line:
            errors.append(f"missing grid line between {a} and {b}")
    # the panel row has none: the margin between two accessory cells is plain fill
    for a, b in zip(PANEL_CELLS, PANEL_CELLS[1:]):
        x0, y0, _, _ = cell_rect(b)
        if at(x0 - 1, y0 + 18) != fill or at(x0 - 1, y0 + 5) != fill:
            errors.append(f"unexpected grid line between the accessory cells {a} and {b}")
    rule_rows = px[RULE_TOP + 2]
    gold = tuple(col("gold", 2)[:3])
    gold_columns = [x for x in range(CANVAS[0]) if tuple(int(v) for v in rule_rows[x, :3]) == gold]
    if not gold_columns or min(gold_columns) != RULE_START or max(gold_columns) < RULE_END - 1:
        errors.append("the gold rule must run from the panel's edge to the right wall, and not cross the panel")
    alcove = rounded.upscale(invdecor._arched(GUI, ALCOVE))
    if (alcove & ~masks["panel"]).any() or (alcove & rect_mask(list(map(cell_rect, ARMOUR)))).any():
        errors.append("the alcove must lie inside the panel and clear of the armour sockets")
    if not alcove[art(MODEL_OUTER)[1] + 30:art(MODEL_OUTER)[3] - 4, 60:142].all():
        errors.append("the alcove must fill the model box behind the player")
    if errors:
        raise ValueError("inventory.png: " + "; ".join(errors))
    colours = {tuple(p) for p in px[px[..., 3] > 0].reshape(-1, 4)}
    print(f"inventory.png: {len(drawn_cells())} framed cells on the vanilla grid, "
          f"{len(PANEL_CELLS + BLOCK_CELLS + BAR_CELLS)} gridless cells in 3 flat regions plus the crafting block, "
          f"{len(SHELL_CELLS)} shell cells plain, {len(colours)} colours, 512x512")


def recipe_sprite():
    """Fully clear sprite: the recipe book button is hidden everywhere (it stays clickable)."""
    return Image.new("RGBA", RECIPE_SIZE, (0, 0, 0, 0))


def check_recipe_sprite(image):
    if image.size != RECIPE_SIZE or np.asarray(image)[..., 3].any():
        raise ValueError(f"recipe book sprite must be {RECIPE_SIZE} and fully transparent")


def main():
    canvas = build()
    check(canvas)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.image().save(OUT)
    print(f"wrote {OUT}")
    sprite = recipe_sprite()
    check_recipe_sprite(sprite)
    RECIPE_SPRITES.mkdir(parents=True, exist_ok=True)
    for name in ("button", "button_highlighted"):
        sprite.save(RECIPE_SPRITES / f"{name}.png")
    print(f"wrote 2 clear recipe book sprites to {RECIPE_SPRITES}")


if __name__ == "__main__":
    main()
