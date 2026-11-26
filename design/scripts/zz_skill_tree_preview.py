"""Review images of the skill menus, drawn from the real pack files, in target/previews/skills/.

Also checks them: frozen palette, binary alpha, every item definition resolves, and no title lets
the vanilla panel show through.
"""
import json

from PIL import Image, ImageDraw

from pixelkit import layout, preview, treestone
from pixelkit.palette import PALETTE
from pixelkit.treetheme import ARCHETYPE_NAMES, STATES, THEMES

NEAREST = Image.Resampling.NEAREST
OUT = layout.ROOT / "target" / "previews" / "skills"
SHEET = (40, 40, 46, 255)
INK = (222, 218, 208, 255)

# upper view examples: stone states, owned edges, reset state
UPPER = {
    "all_states": ({"n1": "owned", "n2": "owned", "n3": "available", "n4": "confirm"}, ("n1-n2",), "ready"),
    "fresh": ({"n1": "available"}, (), "unavailable"),
    "full": ({node: "owned" for node in ("n1", "n2", "n3", "n4", "n5", "n6")},
             tuple(treestone.EDGES["a"]), "ready"),
}
# lower view examples: background variant, stone states, owned edges
LOWER = {
    "b": ({"n4": "available"}, ()),
    "b_left": ({"n4": "owned", "n5": "owned", "n6": "available"}, ("n4-n5",)),
    "b_right": ({"n6": "owned", "n5": "owned", "n4": "available"}, ("n5-n6",)),
    "b_both": ({"n4": "owned", "n5": "owned", "n6": "owned"}, ("n4-n5", "n5-n6")),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def asset(reference, kind, suffix):
    namespace, path = reference.split(":")
    return layout.PACK / "assets" / namespace / kind / f"{path}{suffix}"


def item(key):
    """The texture the client would draw for `arkenmmo:<key>`, found through the pack's own files."""
    definition = read(asset(f"arkenmmo:{key}", "items", ".json"))
    model = read(asset(definition["model"]["model"], "models", ".json"))
    return Image.open(asset(model["textures"]["layer0"], "textures", ".png")).convert("RGBA")


def skill_item(theme, skill, state):
    return item(f"gui/skill/{theme.class_id}/{skill}/{state}")


def tree_items(theme, branch, view_name, states, edges, reset_state="ready"):
    """slot -> texture, as the plugin would fill the chest."""
    view = treestone.VIEWS[view_name]
    items = {}
    for slot, (kind, node_id) in view["nodes"].items():
        if kind == "core":
            items[slot] = skill_item(theme, theme.core, "owned")
        else:
            skill = theme.branches[branch][int(node_id[1]) - 1]
            items[slot] = skill_item(theme, skill, states.get(node_id, "locked"))
    for edge in edges:
        for slot in treestone.EDGES[view_name][edge]:
            items[slot] = item(f"gui/skill/{theme.class_id}/link/{view['links'][slot]}")
    suffix = {"ready": "", "confirm": "_confirm", "unavailable": "_unavailable"}[reset_state]
    items[49] = item(f"gui/button/reset{suffix}")
    return items


def loadout_items(theme):
    """A part-filled loadout: three combos set, one pool stone picked."""
    items = {}
    actives = [skills[i] for skills in theme.branches.values() for i in (0, 3, 5)]
    owned = {actives[0], actives[3], actives[4], actives[6]}
    for slot, skill in zip(treestone.LOADOUT_POOL_SLOTS, actives):
        state = "confirm" if skill == actives[4] else "owned" if skill in owned else "locked"
        items[slot] = skill_item(theme, skill, state)
    items[treestone.LOADOUT_CORE_SLOT] = skill_item(theme, theme.core, "owned")
    equipped = zip(treestone.LOADOUT_COMBO_SLOTS, (theme.core, actives[0], actives[3]))
    items.update({slot: skill_item(theme, skill, "owned") for slot, skill in equipped
                  if skill != theme.core})
    items[treestone.LOADOUT_COMBO_SLOTS[0]] = skill_item(theme, theme.core, "owned")
    return items


def menu(title_key, items, scale, screen=None):
    title = preview.title_strings()[title_key]
    image = preview.compose(title, scale, screen=screen, items=False)
    view = preview.Screen(scale, screen)
    for slot, texture in items.items():
        x0, y0, _, _ = layout.cell(slot % 9, slot // 9)
        image.alpha_composite(texture.resize((16 * scale, 16 * scale), NEAREST), view.px(x0 + 1, y0 + 1))
    for (column, row), kind in preview.SAMPLE_ITEMS.items():
        x0, y0, _, _ = layout.player_cell(column, row)
        image.alpha_composite(preview._sample_item(kind).resize((16 * scale, 16 * scale), NEAREST),
                              view.px(x0 + 1, y0 + 1))
    return image


def check(name, image):
    known = {c for ramp in PALETTE.values() for c in ramp}
    colours = image.getcolors(1 << 16)
    strays = [c for _, c in colours if c[3] == 255 and c[:3] not in known]
    # alpha 1 is the invisible advance pixel pack.save_background places
    partial = sum(n for n, c in colours if 1 < c[3] < 255)
    if strays or partial:
        raise ValueError(f"{name}: {len(strays)} colours outside the palette, {partial} partial-alpha px")


def check_pack():
    textures = sorted((layout.ASSETS / "textures" / "font" / "gui").glob("*.png"))
    textures = [p for p in textures if p.name.startswith(("tree_", "loadout_"))]
    for path in textures:
        check(path.name, Image.open(path).convert("RGBA"))
    keys = [p.relative_to(layout.ASSETS / "items").with_suffix("").as_posix()
            for folder in ("gui/skill", "gui/button")
            for p in sorted((layout.ASSETS / "items" / folder).rglob("*.json"))]
    for key in keys:
        check(key, item(key))
    titles = {k: v for k, v in preview.title_strings().items() if k.startswith(("tree_", "loadout_"))}
    for name, title in titles.items():
        leak = preview.compose(title, 2, leak=True, items=False)
        if any(c == preview.LEAK for _, c in leak.getcolors(1 << 20)):
            raise ValueError(f"{name}: the vanilla panel shows through")
    print(f"checked {len(textures)} background tiles, {len(keys)} items and {len(titles)} titles: "
          "palette, alpha, references and panel cover are fine")


def icon_table(theme, scale):
    """All 19 skills of a class in every state that exists, as large as on screen at `scale`."""
    size, step, name_w, row_h = 16 * scale, 16 * scale + 8, 128, max(16 * scale + 10, 36)
    groups = [(theme.core, None)] + [(skill, branch) for branch, skills in theme.branches.items()
                                     for skill in skills]
    column_w = name_w + step * len(STATES) + 16
    sheet = Image.new("RGBA", (column_w * 2, row_h * 10 + 24), SHEET)
    draw = ImageDraw.Draw(sheet)
    for i, state in enumerate(STATES):
        for column in range(2):
            draw.text((column * column_w + name_w + i * step, 6), state[:5], fill=INK)
    for index, (skill, branch) in enumerate(groups):
        column, row = divmod(index, 10)
        x, y = column * column_w, 24 + row * row_h
        draw.text((x + 6, y + size // 2 - 10), skill, fill=INK)
        draw.text((x + 6, y + size // 2 + 2), branch or "core", fill=(150, 146, 140, 255))
        for i, state in enumerate(STATES):
            if branch is None and state not in ("owned", "confirm"):
                continue
            texture = skill_item(theme, skill, state).resize((size, size), NEAREST)
            sheet.alpha_composite(texture, (x + name_w + i * step, y))
    return sheet


def side_by_side(images, gap=10):
    sheet = Image.new("RGBA", (sum(i.width for i in images) + gap * (len(images) + 1),
                               max(i.height for i in images) + gap * 2), SHEET)
    x = gap
    for image in images:
        sheet.alpha_composite(image, (x, gap))
        x += image.width + gap
    return sheet


def stack(images):
    sheet = Image.new("RGBA", (max(i.width for i in images), sum(i.height for i in images)), SHEET)
    y = 0
    for image in images:
        sheet.alpha_composite(image, (0, y))
        y += image.height
    return sheet


def class_previews(theme):
    folder = OUT / theme.class_id
    folder.mkdir(parents=True, exist_ok=True)
    sample = list(theme.branches)[1]
    shown = None
    for branch in theme.branches:
        states, edges, reset_state = UPPER["all_states"]
        upper = (f"tree_{theme.class_id}_{branch}_a", tree_items(theme, branch, "a", states, edges, reset_state))
        lower_states, lower_edges = LOWER["b_left"]
        lower = (f"tree_{theme.class_id}_{branch}_b_left",
                 tree_items(theme, branch, "b", lower_states, lower_edges))
        side_by_side([menu(*upper, 3), menu(*lower, 3)]).save(folder / f"{branch}_upper_lower_gui3.png")
        for label, (key, items) in (("upper", upper), ("lower", lower)):
            for scale, size in ((2, (854, 480)), (3, (1280, 720))):
                menu(key, items, scale, size).save(folder / f"{branch}_{label}_{size[0]}x{size[1]}_gui{scale}.png")
        if branch == sample:
            shown = upper
    loadout = menu(f"loadout_{theme.class_id}", loadout_items(theme), 3)
    loadout.save(folder / "loadout_gui3.png")
    menu(f"loadout_{theme.class_id}", loadout_items(theme), 3, (1280, 720)).save(
        folder / "loadout_1280x720_gui3.png")
    # one sheet per class: a page at GUI scale 3 beside all 19 icons at the same scale
    side_by_side([menu(*shown, 3), icon_table(theme, 3)]).save(OUT / f"overview_{theme.class_id}_gui3.png")
    side_by_side([menu(*shown, 2), icon_table(theme, 2)]).save(OUT / f"overview_{theme.class_id}_gui2.png")
    table = icon_table(theme, 3)
    table.resize((table.width * 2, table.height * 2), NEAREST).save(folder / "icons_x2.png")
    table.convert("L").save(folder / "icons_gui3_greyscale.png")


def path_previews():
    """Every lower background variant and the three upper examples, to judge the off-page paths."""
    theme, branch = THEMES["warrior"], "berserker"
    uppers = [menu(f"tree_warrior_{branch}_a", tree_items(theme, branch, "a", *example), 2)
              for example in UPPER.values()]
    lowers = [menu(f"tree_warrior_{branch}_{name}", tree_items(theme, branch, "b", states, edges), 2)
              for name, (states, edges) in LOWER.items()]
    stack([side_by_side(uppers), side_by_side(lowers)]).save(OUT / "paths_upper_and_lower_gui2.png")
    states, edges, reset_state = UPPER["all_states"]
    pair = [menu(f"tree_warrior_{branch}_a", tree_items(theme, branch, "a", states, edges, reset_state), 3),
            menu(f"tree_warrior_{branch}_b_left", tree_items(theme, branch, "b", *LOWER["b_left"]), 3)]
    side_by_side(pair).save(OUT / "paths_pair_gui3.png")
    menu(f"tree_warrior_{branch}_a",
         tree_items(theme, branch, "a", UPPER["full"][0], UPPER["full"][1], "confirm"), 3).save(
        OUT / "reset_confirm_gui3.png")


def title_previews():
    """All 12 archetype titles: whole upper pages at GUI scale 2, and the header of both views, where
    the lower view's incoming paths run close under the lettering."""
    pages, headers = [], []
    for theme in THEMES.values():
        row = []
        for branch in theme.branches:
            states, edges, reset_state = UPPER["all_states"]
            upper = menu(f"tree_{theme.class_id}_{branch}_a",
                         tree_items(theme, branch, "a", states, edges, reset_state), 2)
            lower = menu(f"tree_{theme.class_id}_{branch}_b_both",
                         tree_items(theme, branch, "b", *LOWER["b_both"]), 2)
            row.append(upper)
            # the top 40 GUI px of the menu, inside the compositor's 12 px margin
            band = (24, 24, 24 + layout.PANEL_W * 2, 24 + 40 * 2)
            headers.append(side_by_side([upper.crop(band), lower.crop(band)]))
        pages.append(side_by_side(row))
    stack(pages).save(OUT / "titles_all_12_gui2.png")
    half = len(headers) // 2
    side_by_side([stack(headers[:half]), stack(headers[half:])]).save(OUT / "titles_headers_both_views_gui2.png")
    print("titles: " + ", ".join(ARCHETYPE_NAMES.values()))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    check_pack()
    for theme in THEMES.values():
        class_previews(theme)
    path_previews()
    title_previews()
    print(f"skill menu previews in {OUT}")


if __name__ == "__main__":
    main()
