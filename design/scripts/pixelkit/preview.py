"""Simulates the client drawing a 9x6 chest whose title is our glyph string.

It reads the real pack files (font json, textures, title string), so a wrong ascent, shift or
tile cut shows up here. The vanilla panel, label font and player items are our own mock-ups.
"""
import json
import math

from PIL import Image, ImageDraw

from . import layout
from .layout import cell, player_cell

NEAREST = Image.Resampling.NEAREST
LEAK = (255, 0, 255, 255)
VANILLA_GREY = (198, 198, 198, 255)
LABEL_COLOUR = (64, 64, 64, 255)
# 5x7 stand-in letters for the vanilla "Inventory" label: (rows, width)
LABEL_FONT = {
    "I": ("###|.#.|.#.|.#.|.#.|.#.|###", 3),
    "n": (".....|.....|####.|#...#|#...#|#...#|#...#", 5),
    "v": (".....|.....|#...#|#...#|#...#|.#.#.|..#..", 5),
    "e": (".....|.....|.###.|#...#|#####|#....|.####", 5),
    "t": (".#.|.#.|###|.#.|.#.|.#.|..#", 3),
    "o": (".....|.....|.###.|#...#|#...#|#...#|.###.", 5),
    "r": (".....|.....|#.##.|##..#|#....|#....|#....", 5),
    "y": (".....|.....|#...#|#...#|.####|....#|####.", 5),
}


def load_font():
    providers = json.loads((layout.ASSETS / "font" / "gui.json").read_text(encoding="utf-8"))["providers"]
    advances, glyphs = {}, {}
    for provider in providers:
        if provider["type"] == "space":
            advances.update(provider["advances"])
            continue
        namespace, path = provider["file"].split(":")
        sheet = Image.open(layout.PACK / "assets" / namespace / "textures" / path).convert("RGBA")
        rows = provider["chars"]
        cell_w, cell_h = sheet.width // len(rows[0]), sheet.height // len(rows)
        if cell_w > 256 or cell_h > 256 or provider["ascent"] > provider["height"]:
            raise ValueError(f"{provider['file']}: breaks the bitmap provider limits")
        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                image = sheet.crop((c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h))
                box = image.getchannel("A").getbbox()
                scale = provider["height"] / cell_h
                glyphs[char] = {"image": image, "ascent": provider["ascent"], "scale": scale,
                                "advance": int(0.5 + (box[2] if box else 0) * scale) + 1}
    return advances, glyphs


def layout_title(title):
    """Yield (glyph, left, top) in GUI px relative to the panel, and return nothing past the end."""
    advances, glyphs = load_font()
    pen = layout.TITLE_X
    placed = []
    for char in title:
        if char in advances:
            pen += advances[char]
        else:
            glyph = glyphs[char]
            placed.append((glyph, pen, layout.FONT_ORIGIN_ASCENT - glyph["ascent"]))
            pen += glyph["advance"]
    return placed


def title_strings():
    return json.loads(layout.TITLES.read_text(encoding="utf-8"))


class Screen:
    """A screen at one GUI scale; all coordinates passed in are panel-relative GUI px."""

    def __init__(self, scale, screen=None, margin=12):
        self.scale = scale
        if screen:
            gui_w, gui_h = math.ceil(screen[0] / scale), math.ceil(screen[1] / scale)
            self.origin = ((gui_w - layout.PANEL_W) // 2, (gui_h - layout.PANEL_H) // 2)
            size = screen
        else:
            self.origin = (margin, margin)
            size = ((layout.PANEL_W + margin * 2) * scale, (layout.PANEL_H + margin * 2) * scale)
        self.image = _world(size, scale)

    def px(self, x, y):
        return ((self.origin[0] + x) * self.scale, (self.origin[1] + y) * self.scale)

    def fill(self, rect, colour):
        x0, y0 = self.px(rect[0], rect[1])
        x1, y1 = self.px(rect[2], rect[3])
        if colour[3] == 255:
            self.image.paste(colour, (x0, y0, x1, y1))
        else:
            self.image.alpha_composite(Image.new("RGBA", (x1 - x0, y1 - y0), colour), (x0, y0))

    def stamp(self, texture, x, y, width, height):
        """Draw a texture covering `width` x `height` GUI px, sampled nearest like the client."""
        scaled = texture.resize((width * self.scale, height * self.scale), NEAREST)
        self.image.alpha_composite(scaled, self.px(x, y))


def _world(size, scale):
    """A stand-in for the dimmed game world behind the screen."""
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    block = 16 * scale
    shades = [(74, 110, 150), (84, 120, 160), (62, 98, 50), (72, 108, 56), (96, 74, 52)]
    for by in range(0, size[1], block):
        for bx in range(0, size[0], block):
            sky = by < size[1] * 0.55
            shade = shades[(bx // block * 7 + by // block * 3) % 2 + (0 if sky else 2)]
            draw.rectangle((bx, by, bx + block - 1, by + block - 1), fill=shade + (255,))
    image.alpha_composite(Image.new("RGBA", size, (16, 16, 16, 192)))
    return image


def _vanilla_panel(screen, colour):
    width, height = layout.PANEL_W, layout.VANILLA_H
    screen.fill((1, 0, width - 1, height), colour)
    screen.fill((0, 1, width, height - 1), colour)
    if colour == LEAK:
        return
    cells = [cell(c, r) for r in range(6) for c in range(9)] + [player_cell(c, r) for r in range(4) for c in range(9)]
    for x0, y0, x1, y1 in cells:
        screen.fill((x0, y0, x1, y1), (139, 139, 139, 255))


def _label(screen):
    x = layout.LABEL_X
    for char in "Inventory":
        rows, width = LABEL_FONT[char]
        for dy, row in enumerate(rows.split("|")):
            for dx, pixel in enumerate(row):
                if pixel == "#":
                    screen.fill((x + dx, layout.LABEL_Y + dy, x + dx + 1, layout.LABEL_Y + dy + 1), LABEL_COLOUR)
        x += width + 1


# Our own 16x16 stand-ins for player items: bright, dark and mid-toned, so contrast is tested.
def _sample_item(kind):
    image = Image.new("RGBA", (16, 16))
    d = ImageDraw.Draw(image)
    if kind == "bread":
        d.polygon([(2, 9), (9, 3), (13, 6), (7, 13)], fill=(206, 150, 62), outline=(104, 66, 28))
        d.line([(5, 9), (9, 6)], fill=(240, 204, 120))
    elif kind == "coal":
        d.polygon([(3, 6), (7, 3), (12, 5), (13, 11), (8, 13), (4, 11)], fill=(44, 42, 48), outline=(18, 16, 20))
        d.rectangle((6, 6, 7, 7), fill=(96, 92, 104))
    elif kind == "gem":
        d.polygon([(8, 2), (14, 7), (8, 14), (2, 7)], fill=(70, 214, 200), outline=(20, 92, 96))
        d.polygon([(8, 3), (4, 7), (8, 7)], fill=(190, 250, 238))
    elif kind == "sword":
        d.line([(5, 10), (13, 2)], fill=(214, 220, 228), width=3)
        d.line([(3, 8), (8, 13)], fill=(120, 84, 40), width=2)
        d.line([(2, 13), (4, 11)], fill=(90, 62, 30), width=2)
    elif kind == "log":
        d.rectangle((2, 3, 13, 13), fill=(112, 80, 46), outline=(58, 40, 24))
        d.rectangle((4, 5, 11, 11), outline=(178, 138, 84))
    elif kind == "apple":
        d.ellipse((3, 4, 12, 13), fill=(200, 46, 40), outline=(100, 18, 20))
        d.rectangle((7, 2, 8, 4), fill=(80, 120, 40))
    return image


SAMPLE_ITEMS = {(0, 3): "sword", (1, 3): "bread", (2, 3): "apple", (3, 3): "coal", (8, 3): "gem",
                (0, 0): "log", (4, 1): "coal", (5, 1): "gem", (7, 2): "bread", (8, 0): "apple"}


def compose(title, scale, screen=None, leak=False, items=True, slots=False):
    view = Screen(scale, screen)
    _vanilla_panel(view, LEAK if leak else VANILLA_GREY)
    for glyph, x, y in layout_title(title):
        image = glyph["image"]
        width, height = (int(round(v * glyph["scale"])) for v in image.size)
        view.stamp(image, x, y, width, height)
    _label(view)
    if items:
        for (column, row), kind in SAMPLE_ITEMS.items():
            x0, y0, _, _ = player_cell(column, row)
            view.stamp(_sample_item(kind), x0 + 1, y0 + 1, 16, 16)
    if slots:
        _slot_lines(view)
    return view.image


def _slot_lines(view):
    """1 px outlines of every slot, with the three click regions coloured."""
    draw = ImageDraw.Draw(view.image)
    cells = [(cell(c, r), (80, 220, 255) if c < 4 else (120, 255, 120) if c > 4 else
              (255, 230, 60) if r >= 4 else (150, 150, 150)) for r in range(6) for c in range(9)]
    cells += [(player_cell(c, r), (255, 255, 255)) for r in range(4) for c in range(9)]
    for (x0, y0, x1, y1), colour in cells:
        (ax, ay), (bx, by) = view.px(x0, y0), view.px(x1, y1)
        draw.rectangle((ax, ay, bx - 1, by - 1), outline=colour)
