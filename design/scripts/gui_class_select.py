"""Builds the class selection pages: font tiles, font/gui.json, pack.mcmeta and the title strings."""
from pixelkit import backdrops, chrome, layout, pack, warrior
from pixelkit.draw import Canvas

PAGE_1_GLYPHS = [chr(c) for c in range(0xE001, 0xE005)]
# resource pack format 97.1 is Java Edition 26.3 (minecraft.wiki/w/Pack_format)
PACK_MCMETA = {"pack": {"description": "ArkenMMO", "min_format": [97, 1], "max_format": 97}}


def check_inside(figure, interior):
    """Fail the build if a pose change would clip the figure against its panel."""
    left, top, right, bottom = figure.image().getbbox()
    margins = (left - interior[0], top - interior[1], interior[2] - right, interior[3] - bottom)
    print(f"figure margins inside the panel (left, top, right, bottom): {margins}")
    if min(margins) < 0:
        raise ValueError("figure does not fit its panel")


def warrior_panel(canvas, panel):
    interior = chrome.panel_frame(canvas, panel)
    backdrops.ember_keep(canvas, interior)
    centre = (interior[0] + interior[2]) // 2
    feet = interior[3] - 10
    backdrops.contact_shadow(canvas, centre - 17, feet + 1, 22)
    backdrops.contact_shadow(canvas, centre + 19, feet + 4, 25)
    figure = warrior.paint(warrior.figure(), canvas.size, (centre - 2, feet - 1))
    canvas.paste(figure, clip=interior)
    check_inside(figure, interior)
    chrome.panel_corners(canvas, panel)
    chrome.name_plate(canvas, panel, "WARRIOR", "crimson", (("gold", 5), ("gold", 4), ("steel", 6)))


def archer_placeholder(canvas, panel):
    interior = chrome.panel_frame(canvas, panel)
    backdrops.dormant(canvas, interior)
    chrome.panel_corners(canvas, panel)
    chrome.name_plate(canvas, panel, "ARCHER", "dusk_forest",
                      (("iron", 5), ("iron", 5), ("iron", 5)), trim="iron", trim_step=1)


def page(index, left, right):
    canvas = Canvas(*layout.CANVAS)
    chrome.shell(canvas)
    chrome.header(canvas)
    chrome.divider(canvas, index)
    left(canvas, layout.LEFT_PANEL)
    right(canvas, layout.RIGHT_PANEL)
    chrome.inventory(canvas)
    return canvas


def main():
    bitmaps = pack.save_background(page(0, warrior_panel, archer_placeholder), "class_select_1", PAGE_1_GLYPHS)
    pack.write_font(bitmaps)
    pack.write_json(layout.PACK / "pack.mcmeta", PACK_MCMETA)
    pack.write_json(layout.TITLES, {"class_select_1": pack.title(PAGE_1_GLYPHS)})
    print("class_select_1 written")


if __name__ == "__main__":
    main()
