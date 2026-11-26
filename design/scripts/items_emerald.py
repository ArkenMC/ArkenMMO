"""The emerald item: 16x16 texture, item definition, model and the emerald tooltip style (see design/item-emerald.md)."""
from pixelkit import layout, pack
from pixelkit.draw import Canvas
from pixelkit.palette import col

from gui_items import BACKGROUND_ALPHA, BACKGROUND_META, CLEAR, FRAME_META, INSET, SIZE, save_sprite

RAMP = "emerald"
# o outline, then ramp steps: a shadow, b dark, c mid, d bright, e light, w glint
LEGEND = {"o": (RAMP, 0), "a": (RAMP, 1), "b": (RAMP, 2), "c": (RAMP, 3), "d": (RAMP, 4),
          "e": (RAMP, 5), "w": (RAMP, 6)}
# Tall step-cut gem: pointed ends, bright facets on the upper left, darker on the lower right.
_ROWS = [
    "oo",
    "oedo",
    "oewdco",
    "oewddcco",
    "oewdddccbo",
    "oedddcccbo",
    "oeddcccbbo",
    "odcccbbaao",
    "occcbbaaao",
    "occbbaaaao",
    "ocbbaaao",
    "obbaao",
    "obao",
    "oo",
]
# centred in 16 columns, one blank row on top and bottom
GEM = ["." * 16] + [row.center(16, ".") for row in _ROWS] + ["." * 16]


def texture():
    canvas = Canvas(16, 16)
    canvas.grid(GEM, LEGEND, (0, 0))
    path = layout.ASSETS / "textures" / "item" / "emerald.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.image().save(path, optimize=True)


def definitions():
    pack.write_json(layout.ASSETS / "items" / "emerald.json",
                    {"model": {"type": "minecraft:model", "model": "arkenmmo:item/emerald"}})
    pack.write_json(layout.ASSETS / "models" / "item" / "emerald.json",
                    {"parent": "minecraft:item/generated", "textures": {"layer0": "arkenmmo:item/emerald"}})


def tooltip():
    """Same geometry as the class tooltips; emerald frame, small emerald gems on the corners."""
    folder = layout.ASSETS / "textures" / "gui" / "sprites" / "tooltip"
    low, high = INSET, SIZE - INSET

    background = Canvas(SIZE, SIZE)
    background.rect((low, low, high, high), col(RAMP, 0, BACKGROUND_ALPHA))
    for x in (low, high - 1):
        for y in (low, high - 1):
            background.dot(x, y, CLEAR)
    save_sprite(background, folder / "emerald_background.png", BACKGROUND_META)

    frame = Canvas(SIZE, SIZE)
    first, last = low + 1, high - 2
    third = (last - first) // 3
    light = 4
    for y in range(first, last + 1):
        step = light - min(2, (y - first) // third)
        frame.dot(first, y, col(RAMP, step))
        frame.dot(last, y, col(RAMP, step))
    frame.rect((first, first, last + 1, first + 1), col(RAMP, light))
    frame.rect((first, last, last + 1, last + 1), col(RAMP, light - 2))
    # corner gems, 2x2 with the glint top left and the shade bottom right
    for x in (low, last):
        for y in (low, last):
            frame.dot(x, y, col(RAMP, 6))
            frame.dot(x + 1, y, col(RAMP, 5))
            frame.dot(x, y + 1, col(RAMP, 3))
            frame.dot(x + 1, y + 1, col(RAMP, 2))
    save_sprite(frame, folder / "emerald_frame.png", FRAME_META)


def main():
    texture()
    definitions()
    tooltip()
    print("emerald item texture, definition, model and tooltip style written")


if __name__ == "__main__":
    main()
