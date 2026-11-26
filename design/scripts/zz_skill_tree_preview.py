"""Skill tree A1 previews only, written to target/previews/skills/. Writes nothing into the pack."""
from PIL import Image

from pixelkit import layout, preview, treenodes, treestone
from pixelkit.palette import PALETTE, col

NEAREST = Image.Resampling.NEAREST
OUT = layout.ROOT / "target" / "previews" / "skills"
SCREENS = {2: (854, 480), 3: (1280, 720), 4: (1920, 1080)}

SKILLS = {"core": "cleave", "n1": "leaping_strike", "n2": "bloodthirst", "n3": "fury",
          "n4": "whirlwind", "n5": "relentless", "n6": "execute"}
KINDS = {"cleave": "core", "leaping_strike": "active", "bloodthirst": "passive", "fury": "passive",
         "whirlwind": "active", "relentless": "passive", "execute": "active"}

# page examples: node states, the edges whose two ends are owned, and the reset state
EXAMPLES = {
    "all_states": ("a", {"n1": "owned", "n2": "owned", "n3": "available", "n4": "confirm",
                         "n5": "locked", "n6": "locked"}, ("n1-n2",), "ready"),
    "fresh": ("a", {"n1": "available", "n2": "locked", "n3": "locked", "n4": "locked",
                    "n5": "locked", "n6": "locked"}, (), "unavailable"),
    "full": ("a", {n: "owned" for n in ("n1", "n2", "n3", "n4", "n5", "n6")},
             tuple(treestone.EDGES_A), "ready"),
    "reset_confirm": ("a", {"n1": "owned", "n2": "owned", "n3": "owned", "n4": "owned",
                            "n5": "owned", "n6": "available"},
                      ("n1-n2", "n1-n3", "n2-n4", "n4-n5"), "confirm"),
    "lower_view": ("b", {"n4": "owned", "n5": "owned", "n6": "available"}, (), "ready"),
}


def items_for(example):
    """slot -> 32x32 item texture, exactly what the plugin would put in the chest."""
    view_name, states, edges, reset_state = EXAMPLES[example]
    view = treestone.VIEWS[view_name]
    items = {}
    for slot, (kind, node_id) in view["nodes"].items():
        state = "owned" if kind == "core" else states[node_id]
        items[slot] = treenodes.node(SKILLS[node_id], kind, state)
    lit = {slot for edge in edges for slot in treestone.EDGES_A[edge]}
    if view_name == "b":
        lit = {3}
    for slot in lit:
        items[slot] = treenodes.link(view["links"][slot])
    items[49] = treenodes.reset(reset_state)
    return view_name, items


def flat(master, items):
    """The page at art resolution with its items in place."""
    out = master.copy()
    for slot, item in items.items():
        out.alpha_composite(item, treestone.item_origin(slot))
    return out


def screen(master, items, scale, size=None):
    """The chest as the client shows it: vanilla panel, title art, 16x16 GUI items, label."""
    view = preview.Screen(scale, size)
    preview._vanilla_panel(view, preview.VANILLA_GREY)
    view.stamp(master, 0, 0, master.width // layout.DENSITY, master.height // layout.DENSITY)
    preview._label(view)
    for slot, item in items.items():
        x0, y0, _, _ = layout.cell(slot % 9, slot // 9)
        view.stamp(item, x0 + 1, y0 + 1, 16, 16)
    for (column, row), kind in preview.SAMPLE_ITEMS.items():
        x0, y0, _, _ = layout.player_cell(column, row)
        view.stamp(preview._sample_item(kind), x0 + 1, y0 + 1, 16, 16)
    return view.image


def scaled(image, factor):
    return image.resize((image.width * factor, image.height * factor), NEAREST)


def check(name, image):
    known = {c for ramp in PALETTE.values() for c in ramp}
    colours = image.convert("RGBA").getcolors(1 << 16)
    strays = [c for _, c in colours if c[3] and c[:3] not in known]
    partial = sum(n for n, c in colours if 0 < c[3] < 255)
    if strays or partial:
        raise ValueError(f"{name}: {len(strays)} colours outside the palette, {partial} partial-alpha px")
    return len([c for _, c in colours if c[3]])


def pages():
    for example in EXAMPLES:
        view_name, items = items_for(example)
        master = treestone.page("berserker", view_name)
        print(f"{example}: {check(example, master)} background colours")
        for slot, item in items.items():
            check(f"{example} slot {slot}", item)
        art = flat(master, items)
        art.save(OUT / f"page_{example}_art.png")
        scaled(art, 3).save(OUT / f"page_{example}_art_x3.png")
        for scale, size in SCREENS.items():
            screen(master, items, scale, size).save(OUT / f"page_{example}_{size[0]}x{size[1]}_gui{scale}.png")
        if example in ("all_states", "lower_view"):
            screen(master, {}, 3).save(OUT / f"page_{example}_background_only_gui3.png")
            screen(master, items, 3).convert("L").save(OUT / f"page_{example}_greyscale_gui3.png")


def _plate(width, height):
    return Image.new("RGBA", (width, height), col("ember_stone", 1))


def icon_sheet():
    """Every sample icon (rows) in every state (columns), at art size."""
    pad, cell_size = 4, 40
    rows = list(SKILLS.values())
    sheet = _plate(len(treenodes.STATES) * cell_size + pad * 2, len(rows) * cell_size + pad * 2)
    for y, name in enumerate(rows):
        for x, state in enumerate(treenodes.STATES):
            sheet.alpha_composite(treenodes.node(name, KINDS[name], state),
                                  (pad + x * cell_size + 4, pad + y * cell_size + 4))
    return sheet


def silhouettes():
    from pixelkit.treeicons import ICONS
    names = list(ICONS)
    sheet = Image.new("RGBA", (len(names) * 32, 32), (222, 218, 208, 255))
    for i, name in enumerate(names):
        black = Image.new("RGBA", (24, 24), (0, 0, 0, 255))
        sheet.paste(black, (i * 32 + 4, 4), Image.fromarray((ICONS[name] * 255).astype("uint8"), "L"))
    return sheet


def parts_sheet():
    """The three reset states and the four connector pieces, each over dark stone."""
    parts = [treenodes.reset(s) for s in ("ready", "confirm", "unavailable")]
    parts += [treenodes.link(k) for k in ("h", "v", "corner_es", "corner_sw")]
    sheet = _plate(len(parts) * 40 + 8, 40)
    for i, part in enumerate(parts):
        sheet.alpha_composite(part, (i * 40 + 8, 4))
    return sheet


def real_size(sheet, scale, name):
    """A sheet exactly as large as it appears on screen at a GUI scale (2 art px per GUI px)."""
    size = (sheet.width * scale // 2, sheet.height * scale // 2)
    sheet.resize(size, NEAREST).save(OUT / f"{name}_gui{scale}.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages()
    icons = icon_sheet()
    scaled(icons, 8).save(OUT / "icons_states_x8.png")
    scaled(icons.convert("L"), 8).save(OUT / "icons_states_greyscale_x8.png")
    for scale in (2, 3, 4):
        real_size(icons, scale, "icons_states")
    real_size(icons.convert("L"), 3, "icons_states_greyscale")
    scaled(silhouettes(), 6).save(OUT / "icons_silhouettes_x6.png")
    scaled(parts_sheet(), 8).save(OUT / "reset_and_links_x8.png")
    real_size(parts_sheet(), 3, "reset_and_links")
    print(f"skill tree previews in {OUT}")


if __name__ == "__main__":
    main()
