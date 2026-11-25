"""The four classes and how each one's panel is composed."""
from dataclasses import dataclass
from types import ModuleType
from typing import Callable

from . import archer, backdrops, captain, chrome, mage, warrior


@dataclass(frozen=True)
class Hero:
    """`nudge` moves the right-facing figure sideways to centre it; shadows are (dx, dy, half width)
    under the right-facing pose. Both are mirrored for a left-facing figure."""

    name: str
    art: ModuleType
    backdrop: Callable
    ground: str
    nudge: int
    shadows: tuple
    plate: str
    letters: tuple
    lift: int = 0


GOLD_LETTERS = (("gold", 5), ("gold", 4), ("steel", 6))
IVORY_LETTERS = (("ivory", 4), ("ivory", 3), ("steel", 6))

HEROES = {
    "warrior": Hero("WARRIOR", warrior, backdrops.ember_keep, "ember_stone", -2,
                    ((-15, 1, 22), (21, 4, 25)), "crimson", GOLD_LETTERS),
    "archer": Hero("ARCHER", archer, backdrops.twilight_woods, "dusk_forest", -10,
                   ((-23, 1, 22), (36, 4, 22)), "forest", GOLD_LETTERS),
    "mage": Hero("MAGE", mage, backdrops.star_sanctum, "night_teal", -2,
                 ((0, 3, 44),), "violet", GOLD_LETTERS),
    "captain": Hero("CAPTAIN", captain, backdrops.dawn_camp, "dawn_stone", -9,
                    ((-14, 1, 22), (28, 5, 26)), "navy", IVORY_LETTERS),
}


def check_inside(name, figure, interior):
    """Fail the build if a pose change would clip a figure against its panel."""
    left, top, right, bottom = figure.image().getbbox()
    margins = (left - interior[0], top - interior[1], interior[2] - right, interior[3] - bottom)
    print(f"{name}: margins inside the panel (left, top, right, bottom) {margins}, "
          f"figure {right - left}x{bottom - top}")
    if min(margins) < 0:
        raise ValueError(f"{name} does not fit its panel")


def paint_panel(canvas, panel, class_id, facing=1):
    """Frame, backdrop, figure and name plate for one class. `facing` is 1 right, -1 left."""
    hero = HEROES[class_id]
    interior = chrome.panel_frame(canvas, panel)
    hero.backdrop(canvas, interior)
    centre = (interior[0] + interior[2]) // 2
    feet = interior[3] - 10 - hero.lift
    for dx, dy, half in hero.shadows:
        backdrops.contact_shadow(canvas, centre + facing * dx, feet + dy, half, hero.ground)
    figure = hero.art.build(facing).paint(canvas.size, (centre + facing * hero.nudge, feet - 1))
    check_inside(class_id, figure, interior)
    canvas.paste(figure, clip=interior)
    chrome.panel_corners(canvas, panel)
    chrome.name_plate(canvas, panel, hero.name, hero.plate, hero.letters)
