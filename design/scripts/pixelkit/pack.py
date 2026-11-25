"""Font glyph ids, the title string and the writers for pack files."""
import json

from . import layout

FONT = "arkenmmo:gui"
# U+F801..F809 move left and U+F821..F829 move right by 1, 2, 4 ... 256 GUI px
SHIFTS = {-(1 << i): chr(0xF801 + i) for i in range(9)} | {1 << i: chr(0xF821 + i) for i in range(9)}
CELL_W = layout.CANVAS[0] // 2
TILE_H = layout.CANVAS[1] // 2
GUI_CELL_W, GUI_TILE_H = CELL_W // layout.DENSITY, TILE_H // layout.DENSITY


def shift(pixels):
    sign = 1 if pixels > 0 else -1
    return "".join(SHIFTS[sign * bit] for bit in (256, 128, 64, 32, 16, 8, 4, 2, 1) if abs(pixels) & bit)


def advance(ink_width):
    """Client rule for bitmap glyphs: scaled ink width rounded, plus one."""
    return int(0.5 + ink_width / layout.DENSITY) + 1


def title(glyphs):
    """Title string for a background whose four glyphs are given as TL, TR, BL, BR."""
    top_left, top_right, bottom_left, bottom_right = glyphs
    tile = advance(CELL_W)
    row_end = tile * 2 - 1
    return (shift(-layout.TITLE_X) + top_left + shift(-1) + top_right
            + shift(-row_end) + bottom_left + shift(-1) + bottom_right)


def save_background(master, name, glyphs):
    """Cut the master into two tiles, write them and return the two bitmap providers."""
    image = master.image()
    providers = []
    for part, top, row in (("top", 0, glyphs[:2]), ("bottom", TILE_H, glyphs[2:])):
        tile = image.crop((0, top, image.width, top + TILE_H))
        # a fixed advance needs ink in each cell's last column
        for x in (CELL_W - 1, CELL_W * 2 - 1):
            if tile.crop((x, 0, x + 1, TILE_H)).getchannel("A").getextrema()[1] == 0:
                tile.putpixel((x, TILE_H - 1), (0, 0, 0, 1))
        path = layout.ASSETS / "textures" / "font" / "gui" / f"{name}_{part}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        tile.save(path, optimize=True)
        providers.append({"type": "bitmap", "file": f"arkenmmo:font/gui/{name}_{part}.png",
                          "ascent": layout.FONT_ORIGIN_ASCENT - top // layout.DENSITY, "height": GUI_TILE_H,
                          "chars": ["".join(row)]})
    return providers


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_font(bitmaps):
    advances = {char: pixels for pixels, char in sorted(SHIFTS.items(), key=lambda item: item[1])}
    write_json(layout.ASSETS / "font" / "gui.json", {"providers": [{"type": "space", "advances": advances}, *bitmaps]})
