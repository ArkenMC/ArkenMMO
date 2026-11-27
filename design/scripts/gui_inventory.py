"""The player (survival) inventory screen, re-themed in the iron, parchment and gold of the skill menus.

Writes resourcepack/assets/minecraft/textures/gui/container/inventory.png: 512x512, art in the
top-left 352x332 (the vanilla 176x166 on the 2x grid), everything else clear, plus two fully clear
recipe book button sprites (the button is hidden everywhere). Spec: design/gui-inventory.md.
Fails when a cell is off the vanilla slot grid, so a layout slip breaks the build instead of the screen.
"""
import numpy as np
from PIL import Image

from pixelkit import chrome, layout, rounded
from pixelkit.chrome import DARK, gem, slot_cell
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
SHELL_RADIUS = 8  # art px (4 GUI px)

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
# The character panel: armour, model box and the first four storage cells are one flat region without cell
# frames (the game still draws items and ghost icons at cell + 1). The offhand cell and the ninth hotbar cell
# have no art at all: plain shell colour (an item in the offhand slot still renders there).
PANEL_CELLS = ARMOUR + STORAGE[:4]
SHELL_CELLS = [OFFHAND] + [HOTBAR[8]]
# model box outer rect, and the two rects that make up the panel (GUI px)
MODEL_OUTER = (25, 7, 76, 79)
PANEL_TOP = (7, 7, 76, 79)
PANEL_BASE = (7, 79, 79, 101)
PANEL_PAD = 2  # art px of panel colour beyond the cell rects, where there is room
PANEL_CORNER = 6  # art px radius of the panel's outer corners
PANEL_FILL = col("iron", 1)
# survival inventory title: the game draws "Crafting" at (97, 6), 8 px font, cap height 7 (rows y6..y13)
TITLE_PLATE = (94, 4, 163, 15)
# arrow between the crafting grid and the result, in GUI px: shaft x135..150, head to x151
ARROW_TIP = (151, 35.5)
# the gold rule starts here (art px): just right of the panel's edge
RULE_START = 81 * DENSITY


def cells():
    return ARMOUR + [OFFHAND] + CRAFTING + [RESULT] + STORAGE + HOTBAR


def drawn_cells():
    hidden = set(PANEL_CELLS + SHELL_CELLS)
    return [origin for origin in cells() if origin not in hidden]


def cell_rect(origin):
    return art((origin[0], origin[1], origin[0] + SLOT, origin[1] + SLOT))


def rect_mask(rects):
    mask = np.zeros(CANVAS[::-1], bool)
    for x0, y0, x1, y1 in rects:
        mask[y0:y1, x0:x1] = True
    return mask


def shell_mask():
    return rounded.rounded_rect(CANVAS, SHELL_RADIUS)


def shell(canvas):
    """Iron body with the menus' bevelled rim, following rounded corners."""
    mask = shell_mask()
    canvas.mask(mask, col("iron", 2))
    number, lit = rounded.rings(mask, inside=True)
    for index, (top_left, bottom_right) in enumerate(chrome.RIM):
        ring = number == index + 1
        canvas.mask(ring & lit, top_left)
        canvas.mask(ring & ~lit, bottom_right)


def panel_mask():
    """The character panel: the model/armour block over the four storage cells, plus a little air where there is room, outer corners rounded.
    The drawn cells next to it are added as support while rounding, so its flat bottom and right
    sides stay square and no hidden cell loses a corner."""
    top, base = (art(rect) for rect in (PANEL_TOP, PANEL_BASE))
    pad = PANEL_PAD
    mask = rect_mask([(top[0] - pad, top[1] - pad, top[2] + pad, top[3]),
                      (base[0] - pad, base[1], base[2], base[3])])
    mask = rounded.round_concave(mask, 3)
    # the strip right of the base, above the next cell, is support too, so the base's top corner stays square
    support = rect_mask([cell_rect(origin) for origin in drawn_cells()] + [(base[2], base[1], base[2] + 8, base[1] + 8)])
    return rounded.round_convex(mask | support, PANEL_CORNER) & ~support


def character_panel(canvas):
    """One flat recessed region under the armour, model, offhand and first storage cells, with a recessed edge."""
    fill = panel_mask()
    canvas.mask(fill, PANEL_FILL)
    number, lit = rounded.rings(fill, inside=False)
    # a ring may not enter a drawn cell's inside; on the cell's own outer ring it forms the panel's lip
    keep = ~rect_mask([(x0 + 1, y0 + 1, x1 - 1, y1 - 1) for x0, y0, x1, y1 in map(cell_rect, drawn_cells())])
    for index, (top_left, bottom_right) in ((1, (col("iron", 1), col("iron", 3))), (2, (DARK, col("iron", 4)))):
        ring = (number == index) & keep
        canvas.mask(ring & lit, top_left)
        canvas.mask(ring & ~lit, bottom_right)


def title_plate(canvas):
    """Parchment plate behind the vanilla title, ending in a gold gem; built like the menu's "Inventory" plate."""
    px0, py0, px1, py1 = art(TITLE_PLATE)
    frame(canvas, (px0, py0, px1, py1), [(DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((px0 + 2, py0 + 2, px1 - 2, py1 - 2), col("parchment", 2))
    gem(canvas, px1 - 8, (py0 + py1) // 2, 4)


def separator(canvas):
    """The gold rule that closes the crafting area; it starts beyond the panel's edge instead of crossing it."""
    top = 80 * DENSITY
    width = CANVAS[0]
    canvas.rect((RULE_START, top, width - 7, top + 2), DARK)
    canvas.rect((RULE_START, top + 2, width - 7, top + 3), col("gold", 2))
    canvas.rect((RULE_START, top + 3, width - 7, top + 4), DARK)


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
    for origin in drawn_cells():
        # the crafting result gets a gold first ring, lit from the top left like every ring
        outer = (col("gold", 3), col("gold", 1)) if origin == RESULT else None
        slot_cell(canvas, cell_rect(origin), outer)
    character_panel(canvas)
    arrow(canvas)
    full = Canvas(*FILE)
    full.px[:CANVAS[1], :CANVAS[0]] = canvas.px
    return full


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
        errors.append("the silhouette must be the rounded rectangle, with nothing clear inside it")
    if inside[0, 0] or inside[0, -1] or inside[-1, 0] or inside[-1, -1] or not inside[SHELL_RADIUS, SHELL_RADIUS]:
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
    # hidden cells: flat panel colour, no frame pixels; the offhand and ninth hotbar cells are plain shell
    fill = tuple(PANEL_FILL[:3])
    flat = [(cell_rect(origin), fill) for origin in PANEL_CELLS]
    flat += [(art(rect), fill) for rect in (MODEL_OUTER, (7, 79, 79, 83))]
    flat += [(cell_rect(HOTBAR[8]), iron["body"])]
    # the offhand area may only hold the panel's own edge (its first eight art columns); the rest is shell
    ox0, oy0, ox1, oy1 = cell_rect(OFFHAND)
    flat += [((ox0 + 8, oy0, ox1, oy1), iron["body"])]
    for (x0, y0, x1, y1), colour in flat:
        if {tuple(int(v) for v in p[:3]) for p in px[y0:y1, x0:x1].reshape(-1, 4)} != {colour}:
            errors.append(f"hidden area {(x0, y0, x1, y1)} is not one flat colour")
    rule_rows = px[80 * DENSITY + 2]
    gold = tuple(col("gold", 2)[:3])
    gold_columns = [x for x in range(CANVAS[0]) if tuple(int(v) for v in rule_rows[x, :3]) == gold]
    if not gold_columns or min(gold_columns) != RULE_START or max(gold_columns) != CANVAS[0] - 8:
        errors.append("the gold rule must run from the panel's edge to the right wall, and not cross the panel")
    if errors:
        raise ValueError("inventory.png: " + "; ".join(errors))
    colours = {tuple(p) for p in px[px[..., 3] > 0].reshape(-1, 4)}
    print(f"inventory.png: {len(drawn_cells())} drawn cells on the vanilla grid, {len(PANEL_CELLS)} panel cells flat, "
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
