"""Builds the skill menus into the pack: backgrounds, font glyphs, title strings and item models."""
import shutil

from pixelkit import layout, pack, treenodes, treestone
from pixelkit.treetheme import STATES, THEMES

LINKS = ("h", "v", "corner_es", "corner_sw")
RESETS = {"reset": "ready", "reset_confirm": "confirm", "reset_unavailable": "unavailable"}
# the core skill is always owned; "confirm" marks it as picked in the loadout menu
CORE_STATES = ("owned", "confirm")

# private use area blocks; every background takes four characters (TL, TR, BL, BR)
TREE_BASE = {"warrior": 0xE201, "archer": 0xE221, "mage": 0xE241, "captain": 0xE261}
LOADOUT_BASE = 0xE281
LOWER_LIT_BASE = 0xE301
TREE_VIEWS = ("a", "b")
LIT_VIEWS = ("b_left", "b_right", "b_both")
# the folders this script owns inside textures/item, models/item and items
ITEM_FOLDERS = ("gui/skill", "gui/button")


def four(first):
    return [chr(first + i) for i in range(4)]


def backgrounds():
    """(title key, glyphs, painter) for every skill menu background."""
    for class_index, theme in enumerate(THEMES.values()):
        for branch_index, branch in enumerate(theme.branches):
            blocks = [(view, TREE_BASE[theme.class_id] + (branch_index * len(TREE_VIEWS) + i) * 4)
                      for i, view in enumerate(TREE_VIEWS)]
            lit_start = LOWER_LIT_BASE + (class_index * len(theme.branches) + branch_index) * len(LIT_VIEWS) * 4
            blocks += [(view, lit_start + i * 4) for i, view in enumerate(LIT_VIEWS)]
            for view, first in blocks:
                yield (f"tree_{theme.class_id}_{branch}_{view}", four(first),
                       lambda t=theme, b=branch, v=view: treestone.page(t, b, v))
        yield (f"loadout_{theme.class_id}", four(LOADOUT_BASE + class_index * 4),
               lambda t=theme: treestone.loadout(t))


def items():
    """item model key (without the namespace) -> 32x32 texture."""
    for theme in THEMES.values():
        folder = f"gui/skill/{theme.class_id}"
        for skill, kind in theme.skill_kinds().items():
            for state in CORE_STATES if kind == "core" else STATES:
                yield f"{folder}/{skill}/{state}", treenodes.node(theme, skill, kind, state)
        for shape in LINKS:
            yield f"{folder}/link/{shape}", treenodes.link(theme, shape)
    for name, state in RESETS.items():
        yield f"gui/button/{name}", treenodes.reset(state)


def write_item(key, image):
    texture = layout.ASSETS / "textures" / "item" / f"{key}.png"
    texture.parent.mkdir(parents=True, exist_ok=True)
    image.save(texture, optimize=True)
    pack.write_json(layout.ASSETS / "models" / "item" / f"{key}.json",
                    {"parent": "minecraft:item/generated", "gui_light": "front",
                     "textures": {"layer0": f"arkenmmo:item/{key}"}})
    pack.write_json(layout.ASSETS / "items" / f"{key}.json",
                    {"model": {"type": "minecraft:model", "model": f"arkenmmo:item/{key}"}})


class _Master:
    """What pack.save_background needs: something with an image()."""

    def __init__(self, image):
        self._image = image

    def image(self):
        return self._image


def main():
    for folder in ITEM_FOLDERS:
        for root in ("textures/item", "models/item", "items"):
            shutil.rmtree(layout.ASSETS / root / folder, ignore_errors=True)
    bitmaps, titles = [], {}
    for name, glyphs, paint in backgrounds():
        bitmaps += pack.save_background(_Master(paint()), name, glyphs)
        titles[name] = pack.title(glyphs)
    pack.write_font(bitmaps)
    pack.write_titles(titles)
    count = 0
    for key, image in items():
        write_item(key, image)
        count += 1
    print(f"{len(titles)} skill menu backgrounds and {count} items written")


if __name__ == "__main__":
    main()
