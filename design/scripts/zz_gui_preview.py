"""Renders review images of every GUI background to target/previews/gui/. Runs after the generators."""
from PIL import Image

from pixelkit import layout, preview, warrior
from pixelkit.palette import PALETTE

NEAREST = Image.Resampling.NEAREST
SCREENS = {2: (854, 480), 3: (1280, 720), 4: (1920, 1080)}


def master(name):
    tiles = [Image.open(layout.ASSETS / "textures" / "font" / "gui" / f"{name}_{part}.png").convert("RGBA")
             for part in ("top", "bottom")]
    image = Image.new("RGBA", layout.CANVAS)
    image.paste(tiles[0], (0, 0))
    image.paste(tiles[1], (0, tiles[0].height))
    return image


def figure_views(rig_module):
    """The figure alone: black silhouette and greyscale, both at GUI scale 2 and enlarged."""
    figure = rig_module.paint(rig_module.figure(), (180, 180), (94, 168)).image()
    sheet = Image.new("RGBA", (180 * 4, 180 * 2), (232, 228, 220, 255))
    silhouette = Image.new("RGBA", figure.size)
    silhouette.paste((0, 0, 0, 255), (0, 0), figure.getchannel("A"))
    sheet.alpha_composite(silhouette, (0, 0))
    sheet.alpha_composite(silhouette.resize((90, 90), NEAREST), (45, 200))
    dark = Image.new("RGBA", figure.size, (40, 40, 44, 255))
    dark.alpha_composite(figure)
    sheet.paste(dark.convert("L").convert("RGBA"), (180, 0))
    sheet.paste(dark.resize((360, 360), NEAREST), (360, 0))
    return sheet.resize((sheet.width * 2, sheet.height * 2), NEAREST), figure


def report_colours(name, image):
    known = {c for ramp in PALETTE.values() for c in ramp}
    for label, box in (("whole page", None), ("left panel", layout.panel_frame_rect(layout.LEFT_PANEL))):
        part = image.crop(box) if box else image
        colours = {c for _, c in part.getcolors(100000) if c[3] == 255}
        strays = sorted(c for c in colours if c[:3] not in known)
        print(f"{name} {label}: {len(colours)} colours, {len(strays)} outside the palette")
    partial = sum(n for n, c in image.getcolors(100000) if 1 < c[3] < 255)
    print(f"{name}: {partial} partially transparent pixels")


def main():
    layout.PREVIEWS.mkdir(parents=True, exist_ok=True)

    def save(image, filename):
        image.save(layout.PREVIEWS / filename)

    for name, title in preview.title_strings().items():
        art = master(name)
        report_colours(name, art)
        save(art.resize((art.width * 3, art.height * 3), NEAREST), f"{name}_art_x3.png")
        save(art.convert("L"), f"{name}_greyscale.png")
        left = art.crop(layout.panel_frame_rect(layout.LEFT_PANEL))
        save(left.resize((left.width * 8, left.height * 8), NEAREST), f"{name}_left_panel_x8.png")
        for scale, size in SCREENS.items():
            save(preview.compose(title, scale), f"{name}_menu_scale{scale}.png")
            save(preview.compose(title, scale, screen=size), f"{name}_screen_{size[0]}x{size[1]}_scale{scale}.png")
        leak = preview.compose(title, 2, leak=True, items=False)
        holes = sum(n for n, c in leak.getcolors(1 << 20) if c == preview.LEAK)
        print(f"{name}: {holes} screen px of vanilla panel showing through at scale 2")
        save(leak, f"{name}_leak.png")
        save(preview.compose(title, 4, items=False, slots=True), f"{name}_slots.png")
    sheet, figure = figure_views(warrior)
    save(sheet, "warrior_silhouette_greyscale.png")
    save(figure.resize((figure.width * 8, figure.height * 8), NEAREST), "warrior_figure_x8.png")
    print(f"warrior figure: {len([c for _, c in figure.getcolors(9999) if c[3]])} colours, "
          f"{figure.getbbox()[2] - figure.getbbox()[0]}x{figure.getbbox()[3] - figure.getbbox()[1]} art px")
    print(f"previews in {layout.PREVIEWS}")


if __name__ == "__main__":
    main()
