"""Review images of the accessory items and the eight ghost icons to target/previews/accessories/. Runs after
gui_slot_icons.py, gui_inventory.py and items_accessories.py. The surroundings are our own mock-up."""
import numpy as np
from PIL import Image

import gui_inventory as inv
import gui_slot_icons as slot_icons
import items_accessories as acc
from pixelkit import layout, preview

NEAREST = Image.Resampling.NEAREST
OUT = layout.ROOT / "target" / "previews" / "accessories"
BACKDROP = (58, 62, 80, 255)
FLOOR = (58, 62, 80, 255)  # iron 3


def scaled(image, factor):
    return image.resize((image.width * factor, image.height * factor), NEAREST)


def item(name):
    return Image.open(layout.ASSETS / "textures" / "item" / f"{name}.png").convert("RGBA")


def sheet(images, factor, gap=12, columns=None, bg=BACKDROP):
    columns = columns or len(images)
    rows = -(-len(images) // columns)
    w, h = images[0].width * factor, images[0].height * factor
    out = Image.new("RGBA", (columns * (w + gap) + gap, rows * (h + gap) + gap), bg)
    for i, image in enumerate(images):
        out.alpha_composite(scaled(image, factor), (gap + i % columns * (w + gap), gap + i // columns * (h + gap)))
    return out


def ghosts():
    return list(slot_icons.accessory_icons().values())


def panel_row(scale):
    """The accessory row of the character panel: ghosts painted in, then the four items on top."""
    base = Image.open(inv.OUT).convert("RGBA").crop((0, 0) + inv.CANVAS)
    x0, y0 = inv.PANEL_CELLS[0][0] - 2, inv.PANEL_CELLS[0][1] - 2
    box = (x0 * 2, y0 * 2, (inv.PANEL_CELLS[-1][0] + 20) * 2, (y0 + 22) * 2)
    empty = base.crop(box)
    filled = empty.copy()
    for (cx, cy), name in zip(inv.PANEL_CELLS, acc.IDS):
        # 32x32 textures: one texel is one art px, on the item area
        filled.alpha_composite(item(name), ((cx + 1) * 2 + slot_icons.ITEM_AT - box[0], (cy + 1) * 2 + slot_icons.ITEM_AT - box[1]))
    out = Image.new("RGBA", (empty.width, empty.height * 2 + 4), BACKDROP)
    out.alpha_composite(empty, (0, 0))
    out.alpha_composite(filled, (0, empty.height + 4))
    return scaled(out, scale // 2)


def visible_placeholder_pixels():
    """Draw each matching item over its placeholder at the real position and count the placeholder-coloured pixels left."""
    base = Image.open(inv.OUT).convert("RGBA").crop((0, 0) + inv.CANVAS)
    tone = tuple(slot_icons.TONE[:3])
    total = 0
    for origin, name in inv.ACCESSORY_SLOTS.items():
        for item_name in slot_icons.COVERS[name]:
            x, y = inv.ghost_origin(origin)
            cell = base.copy()
            cell.alpha_composite(item(item_name), (x + slot_icons.ITEM_AT, y + slot_icons.ITEM_AT))
            area = cell.crop((x, y, x + 32, y + 32))
            total += int((np.asarray(area)[..., :3] == np.array(tone)).all(axis=-1).sum())
    return total


def tooltip_view():
    box = preview.tooltip(acc.TOOLTIP, 110, 44)
    return scaled(box, 3)


def hotbar(scale):
    """The items in a mock hotbar over the dimmed world at a GUI scale (nearest neighbour; a 32x32 texture fills the
    16 GUI px slot, its art about 12 of them). Bottom row: the old half-size look (8 GUI px) for comparison."""
    size = (20 * 4 * scale + 40, 2 * 16 * scale + 60)
    out = preview._world(size, scale)
    full, half = 16 * scale, 8 * scale
    for i, name in enumerate(acc.IDS):
        x = 20 + i * 20 * scale
        out.alpha_composite(item(name).resize((full, full), NEAREST), (x, 20))
        out.alpha_composite(item(name).resize((half, half), NEAREST), (x + (full - half) // 2, 40 + full + (full - half) // 2))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet(ghosts(), 8, columns=3).save(OUT / "ghost_icons_x8.png")
    sheet(ghosts(), 3, columns=3, bg=FLOOR).save(OUT / "ghost_icons_x3.png")
    sheet([item(n) for n in acc.IDS], 16).save(OUT / "items_x16.png")
    sheet([item(n) for n in acc.IDS] + [Image.open(layout.ASSETS / "textures" / "item" / "emerald.png").convert("RGBA")],
          6).save(OUT / "items_with_emerald_x6.png")
    panel_row(8).save(OUT / "panel_accessory_row_x4.png")
    print(f"placeholder pixels visible beside the matching items: {visible_placeholder_pixels()} (must be 0)")
    tooltip_view().save(OUT / "tooltip_accessory_x3.png")
    for scale in (2, 3, 4):
        hotbar(scale).save(OUT / f"items_hotbar_scale{scale}.png")
    print(f"accessory previews in {OUT}")


if __name__ == "__main__":
    main()
