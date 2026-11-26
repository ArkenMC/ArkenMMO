"""MiniMessage templates for every hover text in the skill tree and loadout menus.

The spec (`design/gui-skill-tooltips.md`) and the hover previews are both generated from here.
A template is a list of lines; the first is the item name, the rest is the lore.
Placeholders are `<lower_case>` and never reuse a MiniMessage tag name such as `<reset>`.
"""
import re

from .tooltipskills import SKILLS

# visible characters per line, measured with the sample values filled in
NAME_LIMIT = 28
LORE_LIMIT = 34

# the name colours of the class selection menu (messages.yml)
CLASS_HEX = {"warrior": "#e8b33c", "archer": "#6abf4b", "mage": "#5aa9e6", "captain": "#d9534f"}
CLASS_NAMES = {"warrior": "Warrior", "archer": "Archer", "mage": "Mage", "captain": "Captain"}
ARCHETYPE_HEX = "#dcc291"
MANA_HEX = "#7fc8e8"
# quiet text; vanilla's dark_gray is unreadable on the class tooltip backgrounds
MUTED_HEX = "#8f8a80"
POINT_COSTS = {"n1": 1, "n2": 1, "n3": 1, "n4": 2, "n5": 1, "n6": 2}

ARCHETYPE_TEXT = {
    "guardian": ("Hold the line: shields, shouts", "and endurance."),
    "berserker": ("Charge in and keep swinging.", "Fury feeds the fight."),
    "duelist": ("Precise strikes against one", "worthy foe."),
    "marksman": ("Careful, heavy shots from", "a long way off."),
    "skirmisher": ("Never stand still: speed and", "a rain of arrows."),
    "hunter": ("Fire, frost, tracking and", "a loyal wolf."),
    "pyromancer": ("Burn your foes with flame", "and falling stars."),
    "frostweaver": ("Slow, root and shatter with", "ice."),
    "lifebinder": ("Mend your allies and sear", "your enemies with light."),
    "vanguard": ("Mark the quarry and lead the", "attack."),
    "standard_bearer": ("Plant your colours and fight", "beside your herald."),
    "warchanter": ("Gather Verses, then turn song", "into steel and healing."),
}

# --- shared lines -----------------------------------------------------------------------------
LINES = {
    "archetype": f"<{ARCHETYPE_HEX}><archetype> <{MUTED_HEX}>- <gray><type>",
    "core": f"<{ARCHETYPE_HEX}><class> core skill <{MUTED_HEX}>- <gray>Active",
    "description": "<gray>",
    "mana": f"<{MANA_HEX}>Mana <white><mana></white>  <{MANA_HEX}>Cooldown <white><cooldown>s",
    "cost": "<gray>Point cost: <white><cost>",
    "combo": "<gray>Combo: <white><combo>",
}

# state block under a tree stone
STATES = {
    "locked": ["<red>Locked"],
    "available": ["<yellow>Click to unlock"],
    "confirm": ["<gold>Click again to unlock"],
    "owned": ["<green>Unlocked"],
    "undoable": ["<green>Unlocked just now", "<yellow>Click to undo"],
    "undo_confirm": ["<gold>Click again to undo", "<gray>Points returned: <white><cost>"],
    "undo_refused": ["<green>Unlocked just now", "<red>Undo <white><blocking></white> first"],
    "core": ["<green>Always yours, free"],
}
# one line per unmet gate, under "Locked"
REQUIREMENTS = {
    "one_skill": ["<red>Needs <white><required>"],
    "either_skill": ["<red>Needs one of:", " <white><required_a>", " <white><required_b>"],
    "level": ["<red>Needs class level <white><level>"],
    "points": ["<red>Not enough points <gray>(<free> free)"],
}

# --- everything that is not a skill stone -----------------------------------------------------
BUTTONS = {
    "sealed": ["<gray>Sealed Stone", f"<{ARCHETYPE_HEX}><archetype>", "",
               f"<{MUTED_HEX}>The carving is hidden.", f"<{MUTED_HEX}>Not yet."],
    "tab": ["<colour><archetype>", f"<{MUTED_HEX}>Archetype", "", "<description>", "",
            "<gray>Points spent: <white><spent>", "<yellow>Click to view"],
    "tab_open": ["<colour><archetype>", f"<{MUTED_HEX}>Archetype", "", "<description>", "",
                 "<gray>Points spent: <white><spent>", "<green>You are viewing this"],
    "back": ["<yellow>Back"],
    "back_loadout": ["<yellow>Back to the skill tree"],
    "reset_ready": ["<yellow>Reset skills", "<gray>Points returned: <white><points>",
                    "<gray>Free out of combat.", "", "<yellow>Click to reset"],
    "reset_confirm": ["<gold>Reset your skills?", "<gray>Points returned: <white><points>",
                      "<gray>Next reset in <white><cooldown>s</white> after.", "", "<gold>Click again to reset"],
    "reset_combat": [f"<{MUTED_HEX}>Reset skills", "<red>Leave combat first <gray>(<seconds>s)"],
    "reset_cooldown": [f"<{MUTED_HEX}>Reset skills", "<red>Ready again in <white><seconds>s"],
    "reset_nothing": [f"<{MUTED_HEX}>Reset skills", "<red>Nothing to reset"],
    "scroll_down": ["<yellow>Scroll down", "<gray>Higher tiers of this", "<gray>archetype."],
    "scroll_up": ["<yellow>Scroll up", "<gray>Lower tiers of this", "<gray>archetype."],
    "loadout": ["<yellow>Spell loadout", "<gray>Set your four combo spells.", "", "<yellow>Click to open"],
    "info": ["<yellow><class> skills", "<gray>Class level <white><level></white> of <white><max_level>",
             "<gray>XP <white><xp></white> / <white><xp_next>", "<gray>Free skill points: <white><free>", "",
             f"<{ARCHETYPE_HEX}><archetype_1><gray>: <white><spent_1>",
             f"<{ARCHETYPE_HEX}><archetype_2><gray>: <white><spent_2>",
             f"<{ARCHETYPE_HEX}><archetype_3><gray>: <white><spent_3>"],
    "loadout_info": ["<yellow>How to cast", "<gray>Hold your class weapon and", "<gray>click a three-click pattern.",
                     "<gray>R is right, L is left."],
    "seat_empty": ["<gray>Empty seat", "<gray>Combo: <white><combo>", "", f"<{MUTED_HEX}>Pick a skill below first."],
    "seat_empty_picked": ["<gray>Empty seat", "<gray>Combo: <white><combo>", "",
                          "<yellow>Click to place <white><picked>"],
}
# last lines of a filled loadout seat or a pool entry; the lines above come from the skill
LOADOUT_STATES = {
    "seat": ["<yellow>Click to clear"],
    "seat_picked": ["<yellow>Click to place <white><picked>"],
    "pool_free": ["<yellow>Click to pick"],
    "pool_assigned": ["<green>On combo <white><combo>", "<yellow>Click to pick"],
    "pool_picked": ["<gold>Picked: click a seat"],
    "pool_locked": ["<red>Not unlocked"],
}

_VALUE = re.compile(r"\{(\w+):([\d.]+)\}([%s]?)")
_TAG = re.compile(r"<[^<>]*>")


def _sample(text):
    return _VALUE.sub(lambda m: m.group(2) + m.group(3), text)


def _wrap(text, limit=LORE_LIMIT):
    """Greedy wrap, measured with the sample values in place."""
    lines, current = [], []
    for word in text.split():
        if current and len(_sample(" ".join(current + [word]))) > limit:
            lines.append(" ".join(current))
            current = []
        current.append(word)
    return lines + [" ".join(current)]


def description_lines(skill):
    """The skill's own words as source lines with `{name:sample}` values."""
    return _wrap(" ".join(SKILLS[skill][3]))


def description_template(skill):
    """MiniMessage lore lines; numbers are placeholders shown in white."""
    return [LINES["description"] + _VALUE.sub(
        lambda m: f"<white><{m.group(1)}>{m.group(3)}</white>", line) for line in description_lines(skill)]


def description_plain(skill):
    return _VALUE.sub(lambda m: f"<{m.group(1)}>{m.group(3)}", " ".join(SKILLS[skill][3]))


def samples(skill):
    return {m.group(1): m.group(2) for line in SKILLS[skill][3] for m in _VALUE.finditer(line)}


def skill_name(skill):
    return SKILLS[skill][0]


def is_active(skill):
    return SKILLS[skill][1] is not None


def fill(line, values):
    """Substitutes sample values for placeholders; style tags are left for the renderer."""
    for key, value in values.items():
        line = line.replace(f"<{key}>", str(value))
    return line


def visible(line):
    return _TAG.sub("", line)


def skill_tooltip(theme, skill, archetype, node, state_lines, extra=()):
    """A whole hover text with sample values: name, archetype, description, numbers, state.
    `archetype` is the display name, or None for the core skill; `extra` sits above the state."""
    _, mana, cooldown, _ = SKILLS[skill]
    values = {"class": CLASS_NAMES[theme.class_id], "archetype": archetype or "",
              "type": "Active" if is_active(skill) else "Passive", "mana": mana, "cooldown": cooldown,
              **samples(skill)}
    lines = [f"<{CLASS_HEX[theme.class_id]}>{skill_name(skill)}",
             fill(LINES["archetype" if archetype else "core"], values), ""]
    lines += [fill(line, values) for line in description_template(skill)]
    numbers = []
    if is_active(skill):
        numbers.append(fill(LINES["mana"], values))
    if node and state_lines and state_lines[0] in ("<red>Locked", "<yellow>Click to unlock",
                                                  "<gold>Click again to unlock"):
        numbers.append(fill(LINES["cost"], {"cost": POINT_COSTS[node]}))
    if numbers:
        lines += ["", *numbers]
    return lines + [*extra, "", *state_lines]
