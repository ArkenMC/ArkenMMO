"""Builds every menu background: two class pages and four confirm screens.

Writes the font tiles, font/gui.json, pack.mcmeta and the title strings.
"""
from pixelkit import chrome, heroes, layout, pack
from pixelkit.draw import Canvas


def glyphs(first):
    return [chr(c) for c in range(first, first + 4)]


# page -> (left class, right class, glyphs)
PAGES = {
    "class_select_1": ("warrior", "archer", glyphs(0xE001)),
    "class_select_2": ("mage", "captain", glyphs(0xE005)),
}
CONFIRMS = {
    "confirm_warrior": ("warrior", glyphs(0xE101)),
    "confirm_archer": ("archer", glyphs(0xE105)),
    "confirm_mage": ("mage", glyphs(0xE109)),
    "confirm_captain": ("captain", glyphs(0xE10D)),
}
# resource pack format 97.1 is Java Edition 26.3 (minecraft.wiki/w/Pack_format)
PACK_MCMETA = {"pack": {"description": "ArkenMMO", "min_format": [97, 1], "max_format": 97}}


def background(body):
    """The shell and inventory area every screen shares, around whatever `body` paints."""
    canvas = Canvas(*layout.CANVAS)
    chrome.shell(canvas)
    body(canvas)
    chrome.inventory(canvas)
    return canvas


def page(index, left, right):
    def body(canvas):
        chrome.header(canvas)
        chrome.divider(canvas, index)
        # the two heroes face each other across the divider
        heroes.paint_panel(canvas, layout.LEFT_PANEL, left, facing=1)
        heroes.paint_panel(canvas, layout.RIGHT_PANEL, right, facing=-1)
    return background(body)


def confirm(class_id):
    def body(canvas):
        chrome.header(canvas, "CONFIRM CHOICE")
        chrome.confirm_column(canvas, heroes.HEROES[class_id].plate)
        # facing right, toward the buttons: the figure is lit in 3D, not flipped
        heroes.paint_panel(canvas, layout.LEFT_PANEL, class_id, facing=1)
    return background(body)


def main():
    bitmaps, titles = [], {}
    for index, (name, (left, right, chars)) in enumerate(PAGES.items()):
        bitmaps += pack.save_background(page(index, left, right), name, chars)
        titles[name] = pack.title(chars)
    for name, (class_id, chars) in CONFIRMS.items():
        bitmaps += pack.save_background(confirm(class_id), name, chars)
        titles[name] = pack.title(chars)
    pack.write_font(bitmaps)
    pack.write_json(layout.PACK / "pack.mcmeta", PACK_MCMETA)
    pack.write_titles(titles)
    print(f"{len(titles)} backgrounds written")


if __name__ == "__main__":
    main()
