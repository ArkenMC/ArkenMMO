"""Writes the hover text spec and renders hover previews with the pack's class tooltip frames.

It reads the pack that gui_skill_tree.py built. The text is drawn with Pillow's built-in bitmap font as a
stand-in for the vanilla font, so widths in game differ a little.
"""
import re

from PIL import Image, ImageDraw, ImageFont

import zz_skill_tree_preview as menus
from pixelkit import layout, preview, tooltiptext as text
from pixelkit.treetheme import ARCHETYPE_NAMES, NODE_IDS, THEMES

NEAREST = Image.Resampling.NEAREST
OUT = menus.OUT / "tooltips"
SPEC = layout.ROOT / "design" / "gui-skill-tooltips.md"
FONT = ImageFont.load_default_imagefont()
# vanilla's named chat colours
NAMED = {"gray": "#aaaaaa", "dark_gray": "#555555", "white": "#ffffff", "yellow": "#ffff55",
         "gold": "#ffaa00", "red": "#ff5555", "green": "#55ff55"}
TOKEN = re.compile(r"(</?[#\w]+>)")


def spans(line):
    """(text, colour) runs of one MiniMessage line; only colour tags are used in these templates."""
    stack = ["#ffffff"]
    for part in TOKEN.split(line):
        if TOKEN.fullmatch(part):
            name = part.strip("</>")
            if name not in NAMED and not name.startswith("#"):
                raise ValueError(f"unfilled placeholder or unknown tag {part!r} in {line!r}")
            if part.startswith("</"):
                stack.pop()
            else:
                stack.append(NAMED.get(name, name))
        elif part:
            yield part, stack[-1]


def _rgb(code):
    return tuple(int(code[i:i + 2], 16) for i in (1, 3, 5))


def box(style, lines):
    """One hover box in GUI px: the class sprites around the text, as the client lays them out."""
    for index, line in enumerate(lines):
        limit = text.NAME_LIMIT if index == 0 else text.LORE_LIMIT
        if len(text.visible(line)) > limit:
            raise ValueError(f"line longer than {limit}: {text.visible(line)!r}")
    width = max(int(FONT.getlength(text.visible(line))) for line in lines)
    height = len(lines) * 10 + (2 if len(lines) > 1 else 0)
    out = Image.new("RGBA", (width + 24, height + 24))
    folder = layout.ASSETS / "textures" / "gui" / "sprites" / "tooltip"
    for part in ("background", "frame"):
        path = folder / f"{style}_{part}.png"
        meta = menus.read(path.with_name(path.name + ".mcmeta"))
        sprite = Image.open(path).convert("RGBA")
        out.alpha_composite(preview.nine_slice(sprite, meta["gui"]["scaling"], *out.size))
    draw = ImageDraw.Draw(out)
    draw.fontmode = "1"
    for index, line in enumerate(lines):
        x, y = 12, 12 + index * 10 + (2 if index else 0) - 1
        for run, colour in spans(line):
            shadow = tuple(v // 4 for v in _rgb(colour))
            draw.text((x + 1, y + 1), run, font=FONT, fill=shadow)
            draw.text((x, y), run, font=FONT, fill=_rgb(colour))
            x += int(FONT.getlength(run))
    # drop the sprites' empty margin
    return out.crop(out.getchannel("A").getbbox())


def sheet(boxes, columns, scale, captions=None):
    """Hover boxes in columns, filled top to bottom, each under its caption."""
    items = list(zip(captions or [""] * len(boxes), boxes))
    target = sum(b.height + 16 for _, b in items) / columns
    stacks, current, used = [], [], 0
    for caption, image in items:
        if current and used + (image.height + 16) / 2 > target and len(stacks) < columns - 1:
            stacks.append(current)
            current, used = [], 0
        current.append((caption, image))
        used += image.height + 16
    stacks.append(current)
    widths = [max(max(i.width, len(c) * 6) for c, i in stack) for stack in stacks]
    out = Image.new("RGBA", (sum(widths) + 8 * (len(stacks) + 1),
                             max(sum(i.height + 16 for _, i in stack) for stack in stacks) + 8), menus.SHEET)
    draw = ImageDraw.Draw(out)
    draw.fontmode = "1"
    x = 8
    for stack, width in zip(stacks, widths):
        y = 6
        for caption, image in stack:
            draw.text((x, y), caption, font=FONT, fill=menus.INK)
            out.alpha_composite(image, (x, y + 11))
            y += image.height + 16
        x += width + 8
    return out.resize((out.width * scale, out.height * scale), NEAREST)


def archetypes(theme):
    """(id, display name, skills) per archetype."""
    return [(branch, ARCHETYPE_NAMES[branch], skills) for branch, skills in theme.branches.items()]


def every_skill(theme):
    """(skill, archetype display name or None, node id or None), core first."""
    yield theme.core, None, None
    for _, name, skills in archetypes(theme):
        for node, skill in zip(NODE_IDS, skills):
            yield skill, name, node


def tab_lines(theme, branch, name, template, spent):
    values = {"colour": f"<{text.CLASS_HEX[theme.class_id]}>", "archetype": name, "spent": spent}
    lines = []
    for line in text.BUTTONS[template]:
        if line == "<description>":
            lines += [f"<gray>{part}" for part in text.ARCHETYPE_TEXT[branch]]
        else:
            lines.append(text.fill(line, values))
    return lines


def button_lines(theme, key, **extra):
    values = {"class": text.CLASS_NAMES[theme.class_id], "points": 5, "cooldown": 60, "seconds": 7,
              "level": 12, "max_level": 30, "xp": 340, "xp_next": 900, "free": 4, "combo": "-".join(theme.combos[3]),
              "archetype": archetypes(theme)[1][1]}
    for index, (_, name, _) in enumerate(archetypes(theme), start=1):
        values.update({f"archetype_{index}": name, f"spent_{index}": (0, 5, 0)[index - 1]})
    values.update(extra)
    return [text.fill(line, values) for line in text.BUTTONS[key]]


def state_examples(theme):
    """Every state a tree stone can be hovered in, on the second archetype."""
    branch, name, skills = archetypes(theme)[1]
    n = dict(zip(NODE_IDS, skills))

    def stone(node, state, requirements=(), **values):
        lines = list(text.STATES[state])
        for key, filled in requirements:
            lines += [text.fill(line, filled) for line in text.REQUIREMENTS[key]]
        return text.skill_tooltip(theme, n[node], name, node, [text.fill(line, values) for line in lines])

    return [
        ("locked: gates unmet", stone("n4", "locked", [
            ("either_skill", {"required_a": text.skill_name(n["n2"]), "required_b": text.skill_name(n["n5"])}),
            ("level", {"level": 8})])),
        ("locked: one skill, no points", stone("n2", "locked", [
            ("one_skill", {"required": text.skill_name(n["n1"])}), ("points", {"free": 0})])),
        ("available", stone("n3", "available")),
        ("confirm", stone("n6", "confirm")),
        ("owned", stone("n1", "owned")),
        ("owned, undoable", stone("n2", "undoable")),
        ("undo: confirm", stone("n2", "undo_confirm", cost=1)),
        ("undo: refused", stone("n1", "undo_refused", blocking=text.skill_name(n["n2"]))),
        ("core skill", text.skill_tooltip(theme, theme.core, None, None, text.STATES["core"])),
        ("sealed stone", button_lines(theme, "sealed")),
    ]


def other_examples(theme):
    """Footer buttons and loadout entries."""
    (first, first_name, first_skills), (second, second_name, second_skills) = archetypes(theme)[:2]
    combo, picked = "-".join(theme.combos[1]), text.skill_name(second_skills[3])
    state = {key: [text.fill(line, {"combo": combo, "picked": picked}) for line in lines]
             for key, lines in text.LOADOUT_STATES.items()}
    combo_line = (text.fill(text.LINES["combo"], {"combo": combo}),)

    def entry(key, extra=()):
        return text.skill_tooltip(theme, second_skills[0], second_name, None, state[key], extra)

    examples = [("tab, open", tab_lines(theme, second, second_name, "tab_open", 5)),
                ("tab, other", tab_lines(theme, first, first_name, "tab", 0))]
    for key in ("back", "reset_ready", "reset_confirm", "reset_combat", "reset_cooldown", "reset_nothing",
                "scroll_down", "scroll_up", "loadout", "info", "loadout_info", "back_loadout", "seat_empty"):
        examples.append((key.replace("_", " "), button_lines(theme, key)))
    examples.append(("seat empty, skill picked", button_lines(theme, "seat_empty_picked", picked=picked)))
    examples += [("filled seat", entry("seat", combo_line)),
                 ("filled seat, skill picked", entry("seat_picked", combo_line)),
                 ("pool: free", entry("pool_free")), ("pool: assigned", entry("pool_assigned")),
                 ("pool: picked", entry("pool_picked")), ("pool: locked", entry("pool_locked"))]
    return examples


def hover(title_key, items, slot, style, lines, scale=3, screen=(1280, 720)):
    """A menu with one hover box beside the hovered slot, kept inside the screen like the client does."""
    image = menus.menu(title_key, items, scale, screen)
    view = preview.Screen(scale, screen)
    tip = box(style, lines)
    tip = tip.resize((tip.width * scale, tip.height * scale), NEAREST)
    x0, y0, x1, _ = layout.cell(slot % 9, slot // 9)
    x, y = view.px(x1 - 2, y0 - 4)
    if x + tip.width > screen[0]:
        x = view.px(x0 + 2, y0)[0] - tip.width
    image.alpha_composite(tip, (max(0, x), max(0, min(y, screen[1] - tip.height))))
    return image


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for theme in THEMES.values():
        cid = theme.class_id
        for label, examples, columns in (("states", state_examples(theme), 4),
                                         ("buttons", other_examples(theme), 5)):
            boxes = [box(cid, lines) for _, lines in examples]
            captions = [caption for caption, _ in examples]
            sheet(boxes, columns, 2, captions).save(OUT / f"{cid}_{label}_gui2.png")
        # all 19 skills, so every description is seen once in a real frame
        skills = [(skill, text.skill_tooltip(theme, skill, name, node, text.STATES["core" if node is None else "owned"]))
                  for skill, name, node in every_skill(theme)]
        count += len(skills)
        sheet([box(cid, lines) for _, lines in skills], 5, 2).save(OUT / f"{cid}_all_19_skills_gui2.png")
        branch, name, _ = archetypes(theme)[1]
        states, edges, reset = menus.UPPER["all_states"]
        tree = menus.tree_items(theme, branch, "a", states, edges, reset)
        key = f"tree_{cid}_{branch}_a"
        examples = dict(state_examples(theme))
        hover(key, tree, 38, cid, examples["locked: gates unmet"]).save(OUT / f"{cid}_hover_stone_1280x720_gui3.png")
        hover(key, tree, 47, cid, tab_lines(theme, branch, name, "tab_open", 5)).save(
            OUT / f"{cid}_hover_tab_1280x720_gui3.png")
        others = dict(other_examples(theme))
        hover(f"loadout_{cid}", menus.loadout_items(theme), 28, cid, others["pool: free"]).save(
            OUT / f"{cid}_hover_loadout_1280x720_gui3.png")
    return count


# --- the spec ---------------------------------------------------------------------------------

def yaml_line(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_block(name, entries, indent=0):
    out = ["  " * indent + f"{name}:"]
    for key, value in entries.items():
        pad = "  " * (indent + 1)
        if isinstance(value, dict):
            out += yaml_block(key, value, indent + 1)
        elif isinstance(value, str):
            out.append(f"{pad}{key}: {yaml_line(value)}")
        else:
            out.append(f"{pad}{key}:")
            out += [f"{pad}  - {yaml_line(line)}" for line in value]
    return out


def fenced(lines):
    return "\n".join(["```yaml", *lines, "```"])


def button_yaml():
    return {key: {"name": lines[0], **({"lore": lines[1:]} if len(lines) > 1 else {})}
            for key, lines in text.BUTTONS.items()}


def skill_yaml(theme):
    return {skill: {"name": f"<{text.CLASS_HEX[theme.class_id]}>{text.skill_name(skill)}",
                    "description": text.description_template(skill)}
            for skill, _, _ in every_skill(theme)}


def skill_table():
    rows = ["| Class | Archetype | Skill (`<skill>`) | Type | Mana / cooldown (draft) | Plain description |",
            "|---|---|---|---|---|---|"]
    for theme in THEMES.values():
        for skill, archetype, _ in every_skill(theme):
            _, mana, cooldown, _ = text.SKILLS[skill]
            cost = f"{mana} / {cooldown}s" if mana is not None else "-"
            rows.append(f"| {text.CLASS_NAMES[theme.class_id]} | {archetype or 'Core skill'} | "
                        f"{text.skill_name(skill)} (`{skill}`) | {'Active' if text.is_active(skill) else 'Passive'} | "
                        f"{cost} | {text.description_plain(skill).replace('<', '&lt;')} |")
    return "\n".join(rows)


def sample_table():
    rows = ["| `<skill>` | Draft sample values |", "|---|---|"]
    for theme in THEMES.values():
        for skill, _, _ in every_skill(theme):
            rows.append(f"| `{skill}` | {', '.join(f'{k} {v}' for k, v in text.samples(skill).items())} |")
    return "\n".join(rows)


def write_spec():
    colours = "\n".join(f"| {text.CLASS_NAMES[c]} | `{value}` | `arkenmmo:{c}` |"
                        for c, value in text.CLASS_HEX.items())
    tabs = {branch: {"name": ARCHETYPE_NAMES[branch],
                     "description": [f"<gray>{line}" for line in text.ARCHETYPE_TEXT[branch]]}
            for theme in THEMES.values() for branch in theme.branches}
    skills = "\n\n".join(f"### {text.CLASS_NAMES[t.class_id]}\n{fenced(yaml_block('skills', skill_yaml(t)))}"
                         for t in THEMES.values())
    SPEC.write_text(f"""# Asset: skill menu hover text

Generated by `design/scripts/zz_skill_tooltips.py` from `pixelkit/tooltiptext.py` and `tooltipskills.py`. Change those files, not this one.
**Status:** proposal, waiting for approval. `messages.yml` and Java are not edited. The numbers are placeholders; the draft values are untested.

## Frames and colours
Every item in a class's tree and loadout menus uses that class's existing tooltip style, including footer buttons and sealed stones. No sprites were added or changed. Name colours are the ones the class selection menu already uses in `messages.yml`.

| Class | Name colour | `tooltip_style` |
|---|---|---|
{colours}

Other colours: archetype line `{text.ARCHETYPE_HEX}`, mana line `{text.MANA_HEX}`, descriptions `gray` with numbers in `white`, quiet text `{text.MUTED_HEX}` (not `dark_gray`, which is unreadable on these backgrounds), `red` for blocked, `yellow` for a click, `gold` for "click again", `green` for owned.

Lit connector pieces hide their tooltip. The dark (unusable) scroll arrow and plain ledge slots get **no item**, so nothing shows on hover.

## Rules
- Build items as the class menu does: name as `ITEM_NAME`, lines as `LORE` with italic off.
- Line limits, with values filled in: name {text.NAME_LIMIT} visible characters, lore {text.LORE_LIMIT}. Vanilla does not wrap item lore, so keep the line breaks. A value much longer than its draft sample can break the limit.
- Fill placeholders with trusted values only (`Placeholder.parsed` for config names, `unparsed` for anything a player typed). No placeholder reuses a MiniMessage tag name.
- `<colour>` is the class name colour tag. `<archetype>` is always the display name. `<type>` is `Active` or `Passive`.
- Only colour tags are used. Separators are plain ASCII.

## How a skill hover is put together
Used for tree stones, the core skill, loadout seats and pool entries. Skip a line when its condition is false.

1. Name: the skill's `name`.
2. `archetype` line, or `core` line for the core skill. **Every state shows it.**
3. Empty line.
4. The skill's `description` lines. **Every state shows them.**
5. Empty line, then `mana` (actives only) and `cost` (tree stones that are locked, available or confirm). Leave the empty line out if neither applies.
6. Filled loadout seats only: `combo`.
7. Empty line, then the state block: `states` in the tree, `loadout-states` in the loadout menu.
8. A locked stone adds one `requirements` entry per unmet gate under `Locked`.

{fenced(yaml_block("lines", text.LINES) + yaml_block("states", text.STATES)
        + yaml_block("requirements", text.REQUIREMENTS) + yaml_block("loadout-states", text.LOADOUT_STATES))}

| State | When | Stone art |
|---|---|---|
| `locked` | a gate is unmet | `locked` |
| `available` | can be bought now | `available` |
| `confirm` | clicked once | `confirm` |
| `owned` | bought before this opening | `owned` |
| `undoable` | bought during this opening and removable | `owned` |
| `undo_confirm` | clicked once to undo | `confirm` |
| `undo_refused` | bought during this opening, but another skill depends on it | `owned` |
| `core` | the free core skill | `owned` |

## Buttons, sealed stones, tabs and loadout seats
The first line is the name. `<description>` in a tab is that archetype's two `archetypes.<id>.description` lines. A sealed stone names its archetype and nothing about the skill. Which reset entry applies: `reset_ready`, `reset_confirm` after one click, or `reset_combat`, `reset_cooldown`, `reset_nothing` with the unavailable art. `back` has no lore, because what it opens is not decided.

{fenced(yaml_block("buttons", button_yaml()))}

{fenced(yaml_block("archetypes", tabs))}

## Skill descriptions (all 76)
From draft sections 7.1-7.4 of `docs/research/mmo-classes-levelling.md`, reworded for players. "Power" is the draft's P. "Opening" and "Verse" are the Captain mechanics from the draft.

{skill_table()}

### Draft sample values
Only for the previews and as a check against the draft; the real values come from config.

{sample_table()}

## Copy-ready skill entries
{skills}

## Previews
`target/previews/skills/tooltips/`: per class `_states`, `_buttons`, `_all_19_skills` sheets at GUI scale 2 and three in-menu hovers at 1280x720 GUI scale 3.

## Not verified
No 26.3 client. The previews use Pillow's built-in bitmap font in place of the vanilla font, so real widths differ, and the box position beside the cursor is simulated. The longest hovers are about 15 lines; check that they fit the user's screen and GUI scale.
""", encoding="utf-8")


def main():
    count = previews()
    write_spec()
    print(f"hover previews for {count} skills in {OUT}; spec written to {SPEC.relative_to(layout.ROOT)}")


if __name__ == "__main__":
    main()
