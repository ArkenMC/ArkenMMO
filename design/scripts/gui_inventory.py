"""The player (survival) inventory screen, re-themed in the iron, parchment and gold of the skill menus.

Writes resourcepack/assets/minecraft/textures/gui/container/inventory.png: 512x512, art in the
top-left 352x332 (the vanilla 176x166 on the 2x grid), everything else clear. Spec: design/gui-inventory.md.
Fails when a cell is off the vanilla slot grid, so a layout slip breaks the build instead of the screen.
"""
from pixelkit import chrome, layout
from pixelkit.chrome import DARK, gem, slot_cell
from pixelkit.draw import Canvas, dilate, frame, poly_mask, shift
from pixelkit.layout import DENSITY, art
from pixelkit.palette import PALETTE, col

OUT = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "container" / "inventory.png"
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
# the player model draws over this black box: outer frame, then the box proper
MODEL_OUTER = (25, 7, 76, 79)
MODEL_BOX = (26, 8, 75, 78)
# survival inventory title ("Crafting" at 97, 8 in vanilla, unverified) and the recipe button's area
TITLE_PLATE = (94, 5, 163, 16)
RECIPE_BUTTON = (104, 61, 124, 79)
# arrow between the crafting grid and the result, in GUI px: shaft x135..150, head to x151
ARROW_TIP = (151, 35.5)


def cells():
    return ARMOUR + [OFFHAND] + CRAFTING + [RESULT] + STORAGE + HOTBAR


def cell_rect(origin):
    return art((origin[0], origin[1], origin[0] + SLOT, origin[1] + SLOT))


def model_recess(canvas):
    """A calm, dark sunken box for the player model, with a faint floor line under the feet."""
    outer = art(MODEL_OUTER)
    frame(canvas, outer, [(DARK, col("iron", 4)), (col("iron", 0), col("iron", 2))])
    box = art(MODEL_BOX)
    canvas.rect(box, col("iron", 1))
    floor_top = box[3] - 16
    canvas.rect((box[0], floor_top, box[2], box[3]), col("iron", 0))
    canvas.rect((box[0], floor_top, box[2], floor_top + 1), col("iron", 2))


def title_plate(canvas):
    """Parchment plate behind the vanilla title, ending in a gold gem; built like the menu's "Inventory" plate."""
    px0, py0, px1, py1 = art(TITLE_PLATE)
    frame(canvas, (px0, py0 + 1, px1, py1), [(DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((px0 + 2, py0 + 3, px1 - 2, py1 - 2), col("parchment", 2))
    gem(canvas, px1 - 8, (py0 + py1) // 2 + 1, 4)


def separator(canvas):
    """The gold rule that closes the crafting area, as above the menu's inventory."""
    top = 80 * DENSITY
    width = CANVAS[0]
    canvas.rect((7, top, width - 7, top + 2), DARK)
    canvas.rect((7, top + 2, width - 7, top + 3), col("gold", 2))
    canvas.rect((7, top + 3, width - 7, top + 4), DARK)


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
    chrome.shell(canvas, CANVAS)
    model_recess(canvas)
    title_plate(canvas)
    separator(canvas)
    for origin in cells():
        # the crafting result gets a gold first ring, lit from the top left like every ring
        outer = (col("gold", 3), col("gold", 1)) if origin == RESULT else None
        slot_cell(canvas, cell_rect(origin), outer)
    arrow(canvas)
    for x, dx in ((4, 1), (CANVAS[0] - 4, -1)):
        chrome.corner_bracket(canvas, x, CANVAS[1] - 4, dx, -1, 9)
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
    if int((inside == 0).sum()) != 16 or not set(inside.flatten().tolist()) <= {0, 255}:
        errors.append("alpha must be binary with only the 4 corner texels (2x2 each) clear")
    known = {c for ramp in PALETTE.values() for c in ramp}
    stray = {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]} - known
    if stray:
        errors.append(f"colours outside the palette: {sorted(stray)}")
    iron = {name: tuple(col("iron", step)[:3]) for name, step in (("body", 2), ("lip", 4), ("fill", 3))}
    dark = tuple(DARK[:3])
    for origin in cells():
        x0, y0, x1, y1 = cell_rect(origin)
        at = lambda x, y: tuple(int(v) for v in px[y, x, :3])  # noqa: E731
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
    x0, y0, x1, y1 = art(MODEL_BOX)
    shades = {tuple(int(v) for v in p[:3]) for p in px[y0:y1, x0:x1].reshape(-1, 4)}
    if shades != {tuple(col("iron", 0)[:3]), tuple(col("iron", 1)[:3])} | {tuple(col("iron", 2)[:3])}:
        errors.append("the model box must hold only its three calm iron tones")
    x0, y0, x1, y1 = art(RECIPE_BUTTON)
    plain = {tuple(int(v) for v in p[:3]) for p in px[y0:y1, x0:x1].reshape(-1, 4)}
    if plain != {iron["body"]}:
        errors.append("the recipe book button area must stay plain")
    if errors:
        raise ValueError("inventory.png: " + "; ".join(errors))
    colours = {tuple(p) for p in px[px[..., 3] > 0].reshape(-1, 4)}
    print(f"inventory.png: {len(cells())} cells on the vanilla grid, {len(colours)} colours, 512x512")


def main():
    canvas = build()
    check(canvas)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.image().save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
