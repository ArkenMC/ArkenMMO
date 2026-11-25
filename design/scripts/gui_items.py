"""The non-background assets: tooltip styles, invisible slot highlight, blank item and pack.png."""
from pixelkit import heroes, layout, pack
from pixelkit.draw import Canvas
from pixelkit.palette import col

CLEAR = (0, 0, 0, 0)

# Tooltip sprites are 1x art. The geometry matches the vanilla 26.3 sprites: the background fills
# pixels 8..91 with clipped corners, the frame is a 1 px line at inset 9. The .mcmeta values are
# vanilla's (nine-slice 100x100; border 9 for the background, 10 and stretch_inner for the frame).
INSET, SIZE = 8, 100
BACKGROUND_ALPHA = 240
# class -> (background colour, frame ramp, lightest frame step)
TOOLTIPS = {
    "warrior": (("crimson", 0), "crimson", 4),
    "archer": (("forest", 0), "forest", 4),
    "mage": (("violet", 0), "violet", 4),
    "captain": (("navy", 0), "gold", 4),
}
BACKGROUND_META = {"gui": {"scaling": {"type": "nine_slice", "width": 100, "height": 100, "border": 9}}}
FRAME_META = {"gui": {"scaling": {"type": "nine_slice", "width": 100, "height": 100, "border": 10,
                                  "stretch_inner": True}}}
# both slot highlight sprites keep vanilla's 26.3 geometry and are fully transparent
HIGHLIGHT_META = {"gui": {"scaling": {"type": "nine_slice", "width": 24, "height": 24, "border": 4}}}


def save_sprite(canvas, path, meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.image().save(path, optimize=True)
    pack.write_json(path.with_name(path.name + ".mcmeta"), meta)


def tooltip(class_id):
    background_colour, ramp, light = TOOLTIPS[class_id]
    folder = layout.ASSETS / "textures" / "gui" / "sprites" / "tooltip"
    low, high = INSET, SIZE - INSET

    background = Canvas(SIZE, SIZE)
    background.rect((low, low, high, high), col(*background_colour, BACKGROUND_ALPHA))
    for x in (low, high - 1):
        for y in (low, high - 1):
            background.dot(x, y, CLEAR)
    save_sprite(background, folder / f"{class_id}_background.png", BACKGROUND_META)

    frame = Canvas(SIZE, SIZE)
    first, last = low + 1, high - 2
    # light from above: the sides step down from the top colour to the bottom colour
    third = (last - first) // 3
    for y in range(first, last + 1):
        step = light - min(2, (y - first) // third)
        frame.dot(first, y, col(ramp, step))
        frame.dot(last, y, col(ramp, step))
    frame.rect((first, first, last + 1, first + 1), col(ramp, light))
    frame.rect((first, last, last + 1, last + 1), col(ramp, light - 2))
    # a square gold stud on each corner
    for x in (low, last):
        for y in (low, last):
            frame.rect((x, y, x + 2, y + 2), col("gold", 3))
            frame.dot(x, y, col("gold", 5))
            frame.dot(x + 1, y + 1, col("gold", 1))
    save_sprite(frame, folder / f"{class_id}_frame.png", FRAME_META)


def highlight():
    folder = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "container"
    for name in ("slot_highlight_back", "slot_highlight_front"):
        save_sprite(Canvas(24, 24), folder / f"{name}.png", HIGHLIGHT_META)


def blank_item():
    pack.write_json(layout.ASSETS / "items" / "gui" / "blank.json", {"model": {"type": "minecraft:empty"}})


def pack_icon():
    """128x128: the four heroes' heads, each at native art size on its own backdrop."""
    icon = Canvas(128, 128)
    # class -> (quadrant, facing, crop offset from the head centre)
    quadrants = {"warrior": ((0, 0), 1, (0, -6)), "archer": ((64, 0), -1, (0, -6)),
                 "mage": ((0, 64), 1, (0, -10)), "captain": ((64, 64), -1, (0, -4))}
    for class_id, ((qx, qy), facing, (dx, dy)) in quadrants.items():
        hero = heroes.HEROES[class_id]
        panel = layout.LEFT_PANEL
        scene = Canvas(*layout.CANVAS)
        interior = (15, 41, 151, 207)
        hero.backdrop(scene, interior)
        origin = ((interior[0] + interior[2]) // 2 + facing * hero.nudge, panel[3] - 54)
        figure = hero.art.build(facing)
        scene.paste(figure.paint(scene.size, origin))
        x, y = figure.screen(hero.art.HEAD_CENTRE, origin)
        left, top = x + dx - 32, y + dy - 32
        icon.px[qy:qy + 64, qx:qx + 64] = scene.px[top:top + 64, left:left + 64]
    dark, light, shade = col("iron", 0), col("gold", 3), col("gold", 1)
    icon.rect((62, 0, 66, 128), dark)
    icon.rect((0, 62, 128, 66), dark)
    icon.rect((63, 0, 65, 128), light)
    icon.rect((0, 63, 128, 65), light)
    for r, colour in (((0, 0, 128, 3), light), ((0, 0, 3, 128), light), ((0, 125, 128, 128), shade),
                      ((125, 0, 128, 128), shade), ((3, 3, 125, 4), dark), ((3, 3, 4, 125), dark),
                      ((3, 124, 125, 125), dark), ((124, 3, 125, 125), dark)):
        icon.rect(r, colour)
    icon.image().save(layout.PACK / "pack.png", optimize=True)


def main():
    for class_id in TOOLTIPS:
        tooltip(class_id)
    highlight()
    blank_item()
    pack_icon()
    print(f"{len(TOOLTIPS)} tooltip styles, 2 highlight sprites, blank item and pack.png written")


if __name__ == "__main__":
    main()
