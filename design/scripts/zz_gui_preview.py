"""Renders review images of every GUI screen and sprite to target/previews/gui/. Runs after the generators."""
from PIL import Image

from pixelkit import heroes, layout, preview
from pixelkit.palette import PALETTE

NEAREST = Image.Resampling.NEAREST
SCREENS = {2: (854, 480), 3: (1280, 720), 4: (1920, 1080)}
BACKDROP = (70, 70, 76, 255)
APPROVED = layout.ROOT / "design" / "scripts" / "reference" / "page1_approved_a1.png"


def scaled(image, factor):
    return image.resize((image.width * factor, image.height * factor), NEAREST)


def master(name):
    tiles = [Image.open(layout.ASSETS / "textures" / "font" / "gui" / f"{name}_{part}.png").convert("RGBA")
             for part in ("top", "bottom")]
    image = Image.new("RGBA", layout.CANVAS)
    image.paste(tiles[0], (0, 0))
    image.paste(tiles[1], (0, tiles[0].height))
    return image


def row(images, gap=6, colour=BACKDROP):
    sheet = Image.new("RGBA", (sum(i.width for i in images) + gap * (len(images) + 1),
                               max(i.height for i in images) + gap * 2), colour)
    x = gap
    for image in images:
        sheet.alpha_composite(image, (x, gap))
        x += image.width + gap
    return sheet


def class_panels():
    """The four panels exactly as the two pages show them."""
    pages = [master("class_select_1"), master("class_select_2")]
    rects = [layout.panel_frame_rect(p) for p in (layout.LEFT_PANEL, layout.RIGHT_PANEL)]
    return [page.crop(rect) for page in pages for rect in rects]


def figures(facing):
    return {name: hero.art.build(facing).paint((190, 190), (95, 178)).image()
            for name, hero in heroes.HEROES.items()}


def silhouettes(views):
    out = []
    for figure in views.values():
        black = Image.new("RGBA", figure.size, (232, 228, 220, 255))
        black.paste((0, 0, 0, 255), (0, 0), figure.getchannel("A"))
        out.append(black)
    return out


def report_colours(name, image):
    known = {c for ramp in PALETTE.values() for c in ramp}
    colours = {c for _, c in image.getcolors(100000) if c[3] == 255}
    strays = [c for c in colours if c[:3] not in known]
    partial = sum(n for n, c in image.getcolors(100000) if 1 < c[3] < 255)
    print(f"{name}: {len(colours)} colours, {len(strays)} outside the palette, {partial} partial-alpha px")


def screens(save):
    for name, title in preview.title_strings().items():
        art = master(name)
        report_colours(name, art)
        save(scaled(art, 3), f"{name}_art_x3.png")
        for scale, size in SCREENS.items():
            save(preview.compose(title, scale), f"{name}_menu_scale{scale}.png")
            save(preview.compose(title, scale, screen=size), f"{name}_screen_{size[0]}x{size[1]}_scale{scale}.png")
        leak = preview.compose(title, 2, leak=True, items=False)
        holes = sum(n for n, c in leak.getcolors(1 << 20) if c == preview.LEAK)
        if holes:
            raise ValueError(f"{name}: {holes} screen px of the vanilla panel show through")
        kind = "confirm" if name.startswith("confirm") else "page"
        save(preview.compose(title, 4, items=False, slots=kind), f"{name}_slots.png")
    print("no vanilla panel shows through on any screen")


def art_views(save):
    panels = class_panels()
    for name, panel in zip(heroes.HEROES, panels):
        report_colours(f"{name} panel", panel)
        save(scaled(panel, 8), f"{name}_panel_x8.png")
    save(scaled(row(panels), 4), "contact_sheet_x4.png")
    save(scaled(row(panels), 2), "contact_sheet_x2.png")
    save(row(panels).convert("L"), "contact_sheet_greyscale_x1.png")
    right = figures(1)
    for name, figure in right.items():
        box = figure.getbbox()
        count = len([c for _, c in figure.getcolors(9999) if c[3]])
        print(f"{name} figure: {box[2] - box[0]}x{box[3] - box[1]} art px, {count} colours")
    black = silhouettes(right)
    save(scaled(row(black), 2), "silhouettes_x2.png")
    # art is 2 px per GUI px, so this is the size seen at GUI scale 1
    small = [i.resize((i.width // 2, i.height // 2), NEAREST) for i in black]
    save(row(small), "silhouettes_gui_size.png")
    save(scaled(row([black[0], black[3]]), 3), "silhouette_warrior_vs_captain.png")


def before_after(save):
    rect = layout.panel_frame_rect(layout.LEFT_PANEL)
    old = Image.open(APPROVED).convert("RGBA").crop(rect)
    new = master("class_select_1").crop(rect)
    save(scaled(row([old, new], gap=8), 6), "warrior_before_after.png")
    save(scaled(row([old, new], gap=8), 2), "warrior_before_after_x2.png")


def main():
    layout.PREVIEWS.mkdir(parents=True, exist_ok=True)

    def save(image, filename):
        image.save(layout.PREVIEWS / filename)

    screens(save)
    art_views(save)
    before_after(save)
    preview.sprite_views(save)
    print(f"previews in {layout.PREVIEWS}")


if __name__ == "__main__":
    main()
