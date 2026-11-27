"""Review images of the player inventory texture to target/previews/gui/. Runs after gui_inventory.py.

Everything vanilla here (panel, slot colours, label, figure, items) is our own mock-up built from the
measured layout; the Mojang texture is never read or copied.
"""
from PIL import Image, ImageDraw

import gui_inventory as inv
import items_accessories as acc
from pixelkit import layout, preview

NEAREST = Image.Resampling.NEAREST
SCREENS = {2: (854, 480), 3: (1280, 720), 4: (1920, 1080)}
GUI_W, GUI_H = inv.GUI
BACKDROP = (70, 70, 76, 255)
MAGENTA = (255, 0, 255, 255)
CYAN = (0, 255, 255, 255)
# "Crafting" in the vanilla font is drawn at (97, 6) in colour #404040; our own 5x7 stand-in letters
LETTERS = dict(preview.LABEL_FONT)
LETTERS.update({
    "C": (".###.|#...#|#....|#....|#....|#...#|.###.", 5),
    "a": (".....|.....|.###.|....#|.####|#...#|.####", 5),
    "f": ("..##|.#..|###.|.#..|.#..|.#..|.#..", 4),
    "i": ("#|.|#|#|#|#|#", 1),
    "g": (".....|.....|.####|#...#|.####|....#|.###.", 5),
})


def texture():
    return inv_image().crop((0, 0) + inv.CANVAS)


def inv_image():
    return Image.open(inv.OUT).convert("RGBA")


def scaled(image, factor):
    return image.resize((image.width * factor, image.height * factor), NEAREST)


def stand_in_figure(draw, scale):
    """A blocky player stand-in over the model box, in GUI px."""
    parts = [((40, 62, 46, 76), (52, 80, 140)), ((47, 62, 53, 76), (52, 80, 140)),
             ((38, 36, 54, 62), (60, 150, 160)), ((32, 36, 38, 60), (60, 150, 160)), ((54, 36, 60, 60), (60, 150, 160)),
             ((39, 20, 53, 36), (200, 150, 110))]
    for (x0, y0, x1, y1), colour in parts:
        draw.rectangle((x0 * scale, y0 * scale, x1 * scale - 1, y1 * scale - 1), fill=colour + (255,))
    for x, y in ((42, 27), (49, 27)):
        draw.rectangle((x * scale, y * scale, (x + 2) * scale - 1, (y + 1) * scale - 1), fill=(30, 30, 40, 255))


def vanilla_mock():
    """The vanilla layout as flat panel, cells and boxes (GUI px), for overlaying and comparing."""
    image = Image.new("RGBA", inv.GUI, (198, 198, 198, 255))
    draw = ImageDraw.Draw(image)
    for x, y in inv.cells():
        draw.rectangle((x, y, x + 17, y + 17), fill=(139, 139, 139, 255), outline=(55, 55, 55, 255))
    draw.rectangle((25, 7, 75, 78), fill=(0, 0, 0, 255), outline=(55, 55, 55, 255))
    draw.polygon([(135, 34), (144, 34), (144, 29), (151, 35), (144, 41), (144, 36), (135, 36)], fill=(139, 139, 139, 255))
    return image


def screen(size, scale):
    """Our texture over a dimmed world with items, label and a figure; the recipe button is hidden."""
    image = preview._world(size, scale)
    origin = ((size[0] // scale - GUI_W) // 2, (size[1] // scale - GUI_H) // 2)
    panel = texture().resize((GUI_W * scale, GUI_H * scale), NEAREST)
    image.alpha_composite(panel, (origin[0] * scale, origin[1] * scale))
    gui = Image.new("RGBA", (GUI_W * scale, GUI_H * scale))
    draw = ImageDraw.Draw(gui)
    stand_in_figure(draw, scale)
    x = 97
    for char in "Crafting":
        rows, width = LETTERS[char]
        for dy, row in enumerate(rows.split("|")):
            for dx, pixel in enumerate(row):
                if pixel == "#":
                    draw.rectangle(((x + dx) * scale, (6 + dy) * scale, (x + dx + 1) * scale - 1, (6 + dy + 1) * scale - 1),
                                   fill=(64, 64, 64, 255))
        x += width + 1
    image.alpha_composite(gui, (origin[0] * scale, origin[1] * scale))
    kinds = ["sword", "bread", "apple", "coal", "gem", "log"]
    for index, (x, y) in enumerate(inv.cells()):
        if index % 3 == 0 and (x, y) != inv.RESULT and (x, y) not in inv.ARMOUR + [inv.OFFHAND]:
            sprite = preview._sample_item(kinds[index % len(kinds)]).resize((16 * scale, 16 * scale), NEAREST)
            image.alpha_composite(sprite, ((origin[0] + x + 1) * scale, (origin[1] + y + 1) * scale))
    # the accessory items at the models' gui scale 0.5, centred in the item area (nearest neighbour like the game)
    shrunk = round(16 * scale * acc.GUI_SCALE)
    for (cx, cy), name in zip(inv.PANEL_CELLS, acc.IDS):
        sprite = Image.open(layout.ASSETS / "textures" / "item" / f"{name}.png").convert("RGBA").resize((shrunk, shrunk), NEAREST)
        offset = (16 * scale - shrunk) // 2
        image.alpha_composite(sprite, ((origin[0] + cx + 1) * scale + offset, (origin[1] + cy + 1) * scale + offset))
    return image


def corners():
    """Zoomed crops (x8) of the shell corner, the panel/block seam and the crafting block corner."""
    base = texture()
    boxes = [(0, 0, 60, 60), (110, 150, 200, 230), (180, 20, 260, 80)]
    tiles = [scaled(base.crop(box), 8) for box in boxes]
    sheet = Image.new("RGBA", (sum(t.width for t in tiles) + 12 * (len(tiles) + 1), max(t.height for t in tiles) + 24), BACKDROP)
    x = 12
    for tile in tiles:
        sheet.alpha_composite(tile, (x, 12))
        x += tile.width + 12
    return sheet


def overlay():
    """Left: our art with the vanilla slot outlines on top. Right: the vanilla layout mock. Both x4."""
    art = scaled(texture(), 2)
    draw = ImageDraw.Draw(art)
    for x, y in inv.cells():
        draw.rectangle((x * 4, y * 4, (x + 18) * 4 - 1, (y + 18) * 4 - 1), outline=MAGENTA)
    mx0, my0, mx1, my1 = inv.MODEL_OUTER
    draw.rectangle((mx0 * 4, my0 * 4, mx1 * 4 - 1, my1 * 4 - 1), outline=CYAN)
    px0, py0, px1, py1 = inv.TITLE_PLATE
    draw.rectangle((px0 * 4, py0 * 4, px1 * 4 - 1, py1 * 4 - 1), outline=CYAN)
    mock = scaled(vanilla_mock(), 4)
    sheet = Image.new("RGBA", (art.width + mock.width + 36, art.height + 24), BACKDROP)
    sheet.alpha_composite(art, (12, 12))
    sheet.alpha_composite(mock, (art.width + 24, 12))
    return sheet


def main():
    layout.PREVIEWS.mkdir(parents=True, exist_ok=True)

    def save(image, name):
        image.save(layout.PREVIEWS / name)

    base = texture()
    for factor in (2, 4):
        sheet = Image.new("RGBA", (base.width * factor + 24, base.height * factor + 24), BACKDROP)
        sheet.alpha_composite(scaled(base, factor), (12, 12))
        save(sheet, f"inventory_art_x{factor}.png")
    for scale, size in SCREENS.items():
        save(screen(size, scale), f"inventory_screen_{size[0]}x{size[1]}_scale{scale}.png")
    save(corners(), "inventory_corners_x8.png")
    save(overlay(), "inventory_vs_vanilla_layout.png")
    print(f"inventory previews in {layout.PREVIEWS}")


if __name__ == "__main__":
    main()
