"""Review images of the creative inventory art to target/previews/gui/. Runs after gui_creative_inventory.py.

Everything vanilla here (panel colours, text, figure, items, tab icons) is our own mock-up built from
the measured layout; the Mojang textures are never read or copied.
"""
from PIL import Image, ImageDraw, ImageFont

import gui_creative_inventory as cr
from pixelkit import layout, preview

NEAREST = Image.Resampling.NEAREST
SCREENS = {2: (854, 480), 3: (1280, 720), 4: (1920, 1080)}
GUI_W, GUI_H = cr.GUI
BACKDROP = (70, 70, 76, 255)
MAGENTA, CYAN, GREEN = (255, 0, 255, 255), (0, 255, 255, 255), (120, 255, 60, 255)
TITLES = {"items": "Building Blocks", "search": "Search Items", "inventory": None}
# which tab is open in each view: (top row?, column)
OPEN_TAB = {"items": (True, 1), "search": (True, 6), "inventory": (False, 6)}
FILES = {"inventory": "tab_inventory", "items": "tab_items", "search": "tab_item_search"}


def background(kind):
    return Image.open(cr.BACKGROUNDS / f"{FILES[kind]}.png").convert("RGBA").crop((0, 0) + cr.CANVAS)


def sprite(name):
    return Image.open(cr.SPRITES / f"{name}.png").convert("RGBA")


def put(image, source, x, y, size, scale, origin):
    """Draw `source` covering `size` GUI px at GUI (x, y), sampled nearest like the client."""
    scaled = source.resize((size[0] * scale, size[1] * scale), NEAREST)
    image.alpha_composite(scaled, ((origin[0] + x) * scale, (origin[1] + y) * scale))


def text(image, label, x, y, scale, origin, colour=(64, 64, 64, 255)):
    """Stand-in text: a small font drawn at GUI size, thresholded so it keeps hard pixels."""
    mask = Image.new("L", (GUI_W, 12))
    ImageDraw.Draw(mask).text((0, -1), label, font=ImageFont.load_default(size=8), fill=255)
    layer = Image.new("RGBA", mask.size, colour)
    layer.putalpha(mask.point(lambda v: 255 if v > 120 else 0))
    put(image, layer, x, y, mask.size, scale, origin)


def figure(draw, origin, scale):
    parts = [((84, 36, 90, 48), (52, 80, 140)), ((91, 36, 97, 48), (52, 80, 140)),
             ((82, 18, 98, 36), (60, 150, 160)), ((76, 18, 82, 34), (60, 150, 160)), ((98, 18, 104, 34), (60, 150, 160)),
             ((83, 8, 97, 18), (200, 150, 110))]
    for (x0, y0, x1, y1), colour in parts:
        draw.rectangle(((origin[0] + x0) * scale, (origin[1] + y0) * scale, (origin[0] + x1) * scale - 1,
                        (origin[1] + y1) * scale - 1), fill=colour + (255,))


def tab_icon(image, top, column, scale, origin, index):
    """Stand-in 16x16 item in a tab; the real icon offset is assumed (top +9, bottom +6)."""
    y = (cr.TAB_TOP_Y + 9) if top else (cr.TAB_BOTTOM_Y + 6)
    kinds = ["log", "gem", "apple", "bread", "coal", "sword", "gem"]
    sprite16 = preview._sample_item(kinds[index % len(kinds)]).resize((16 * scale, 16 * scale), NEAREST)
    image.alpha_composite(sprite16, ((origin[0] + cr.tab_x(column) + 5) * scale, (origin[1] + y) * scale))


def tabs(image, kind, scale, origin, behind):
    """Unselected tabs go behind the panel, the open one on top, as the client orders them."""
    open_top, open_column = OPEN_TAB[kind]
    for top in (True, False):
        for column in range(7):
            selected = (top, column) == (open_top, open_column)
            if selected == behind:
                continue
            name = f"tab_{'top' if top else 'bottom'}_{'selected' if selected else 'unselected'}_{column + 1}"
            y = cr.TAB_TOP_Y if top else cr.TAB_BOTTOM_Y
            put(image, sprite(name), cr.tab_x(column), y, cr.TAB_GUI, scale, origin)
            if not behind:
                tab_icon(image, top, column, scale, origin, column)
    if behind:
        return
    for top in (True, False):
        for column in range(7):
            if (top, column) != (open_top, open_column):
                tab_icon(image, top, column, scale, origin, column)


def screen(kind, size, scale):
    image = preview._world(size, scale)
    origin = ((size[0] // scale - GUI_W) // 2, (size[1] // scale - GUI_H) // 2)
    tabs(image, kind, scale, origin, behind=True)
    put(image, background(kind), 0, 0, cr.GUI, scale, origin)
    gui = Image.new("RGBA", (GUI_W * scale, GUI_H * scale))
    draw = ImageDraw.Draw(gui)
    if kind == "inventory":
        figure(draw, (0, 0), scale)
    image.alpha_composite(gui, (origin[0] * scale, origin[1] * scale))
    if TITLES[kind]:
        text(image, TITLES[kind], 8, 6, scale, origin)
    if kind != "inventory":
        thumb = sprite("scroller").resize((12 * scale, 15 * scale), NEAREST)
        image.alpha_composite(thumb, ((origin[0] + 175) * scale, (origin[1] + 18 + 30) * scale))
    if kind == "search":
        text(image, "stone", 82, 6, scale, origin, (255, 255, 255, 255))
    kinds = ["sword", "bread", "apple", "coal", "gem", "log"]
    cells = cr.INVENTORY_CELLS if kind == "inventory" else cr.ITEM_CELLS
    for index, (x, y) in enumerate(cells):
        if index % 2 == 0 or kind != "inventory":
            sprite16 = preview._sample_item(kinds[index % len(kinds)]).resize((16 * scale, 16 * scale), NEAREST)
            image.alpha_composite(sprite16, ((origin[0] + x + 1) * scale, (origin[1] + y + 1) * scale))
    tabs(image, kind, scale, origin, behind=False)
    return image


def vanilla_mock(kind):
    image = Image.new("RGBA", cr.GUI, (198, 198, 198, 255))
    draw = ImageDraw.Draw(image)
    cells = cr.INVENTORY_CELLS if kind == "inventory" else cr.ITEM_CELLS
    for x, y in cells:
        draw.rectangle((x, y, x + 17, y + 17), fill=(139, 139, 139, 255), outline=(55, 55, 55, 255))
    if kind == "inventory":
        x, y = cr.DESTROY
        draw.rectangle((x, y, x + 17, y + 17), fill=(171, 127, 127, 255), outline=(55, 55, 55, 255))
        draw.line((x + 3, y + 3, x + 14, y + 14), fill=(31, 31, 31, 255), width=2)
        draw.line((x + 3, y + 14, x + 14, y + 3), fill=(31, 31, 31, 255), width=2)
        draw.rectangle((72, 5, 105, 49), fill=(0, 0, 0, 255), outline=(55, 55, 55, 255))
    else:
        draw.rectangle((174, 17, 187, 128), fill=(139, 139, 139, 255), outline=(55, 55, 55, 255))
    if kind == "search":
        draw.rectangle((80, 4, 169, 15), fill=(139, 139, 139, 255), outline=(85, 85, 85, 255))
    return image


def overlay(kind):
    art = background(kind).resize((GUI_W * 4, GUI_H * 4), NEAREST)
    draw = ImageDraw.Draw(art)
    cells = cr.INVENTORY_CELLS if kind == "inventory" else cr.ITEM_CELLS
    for x, y in cells + ([cr.DESTROY] if kind == "inventory" else []):
        draw.rectangle((x * 4, y * 4, (x + 18) * 4 - 1, (y + 18) * 4 - 1), outline=MAGENTA)
    boxes = [cr.MODEL_OUTER] if kind == "inventory" else [cr.TRACK]
    boxes += [cr.SEARCH_FIELD] if kind == "search" else []
    boxes += [cr.ITEMS_PLATE] if kind == "items" else [cr.SEARCH_PLATE] if kind == "search" else []
    for x0, y0, x1, y1 in boxes:
        draw.rectangle((x0 * 4, y0 * 4, x1 * 4 - 1, y1 * 4 - 1), outline=CYAN)
    mock = vanilla_mock(kind).resize((GUI_W * 4, GUI_H * 4), NEAREST)
    sheet = Image.new("RGBA", (art.width * 2 + 36, art.height + 24), BACKDROP)
    sheet.alpha_composite(art, (12, 12))
    sheet.alpha_composite(mock, (art.width + 24, 12))
    return sheet


def tab_strips():
    """Every tab column in one row against the panel edge, at x4 (art px doubled): selected and unselected, top and bottom."""
    art = background("items")
    strips = []
    for top in (True, False):
        for selected in (True, False):
            strip = Image.new("RGBA", (cr.CANVAS[0], 112))
            panel_y, tab_y = (56, 0) if top else (0, 48)
            sources = [(f"tab_{'top' if top else 'bottom'}_{'selected' if selected else 'unselected'}_{c + 1}", cr.tab_x(c) * 2)
                       for c in range(7)]
            if not selected:
                for name, x in sources:
                    strip.alpha_composite(sprite(name), (x, tab_y))
            rows = (0, 56) if top else (cr.CANVAS[1] - 56, cr.CANVAS[1])
            strip.alpha_composite(art.crop((0, rows[0], cr.CANVAS[0], rows[1])), (0, panel_y))
            if selected:
                for name, x in sources:
                    strip.alpha_composite(sprite(name), (x, tab_y))
            strips.append(strip)
    sheet = Image.new("RGBA", (cr.CANVAS[0] * 2 + 24, len(strips) * 112 * 2 + 12 * (len(strips) + 1)), BACKDROP)
    for index, strip in enumerate(strips):
        sheet.alpha_composite(strip.resize((strip.width * 2, strip.height * 2), NEAREST), (12, 12 + index * (224 + 12)))
    return sheet


def main():
    layout.PREVIEWS.mkdir(parents=True, exist_ok=True)

    def save(image, name):
        image.save(layout.PREVIEWS / name)

    for kind, file in FILES.items():
        base = background(kind)
        for factor in (2, 4):
            sheet = Image.new("RGBA", (base.width * factor // 2 * 2 + 24, base.height * factor // 2 * 2 + 24), BACKDROP)
            sheet.alpha_composite(base.resize((base.width * factor, base.height * factor), NEAREST), (12, 12))
            save(sheet, f"creative_{kind}_art_x{factor}.png")
        for scale, size in SCREENS.items():
            save(screen(kind, size, scale), f"creative_{kind}_screen_{size[0]}x{size[1]}_scale{scale}.png")
        save(overlay(kind), f"creative_{kind}_vs_vanilla_layout.png")
    save(tab_strips(), "creative_tabs_all_positions_x4.png")
    print(f"creative inventory previews in {layout.PREVIEWS}")


if __name__ == "__main__":
    main()
