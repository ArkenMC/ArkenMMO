"""Skill tree data: the classes, their branches and skills, and each class's colours."""
from dataclasses import dataclass

from .palette import col

STATES = ("locked", "available", "confirm", "owned")
NODE_IDS = ("n1", "n2", "n3", "n4", "n5", "n6")
# every branch shares one shape: n1, n4 and n6 are actives
NODE_KINDS = {"n1": "active", "n2": "passive", "n3": "passive", "n4": "active", "n5": "passive",
              "n6": "active"}


@dataclass(frozen=True)
class Theme:
    class_id: str
    # five stone steps, dark to light
    stone: tuple
    # owned glow, dark to light: plate, three halo and ring steps, rune fill, rune core
    glow: tuple
    gem: str
    # the "click again" corner brackets and the core stone's bars: dark, mid, light
    mark: tuple
    core: str
    # branch id -> skill ids n1..n6, in the brief's tab order
    branches: dict
    combos: tuple

    def s(self, step):
        return col(*self.stone[step])

    def g(self, step):
        return col(*self.glow[step])

    def skill_kinds(self):
        """skill id -> stone shape, core first."""
        kinds = {self.core: "core"}
        for skills in self.branches.values():
            kinds.update({skill: NODE_KINDS[node] for node, skill in zip(NODE_IDS, skills)})
        return kinds


def _steps(ramp, *steps):
    return tuple((ramp, step) for step in steps)


GOLD_MARK = _steps("gold", 2, 4, 5)
# the Captain glows gold, so "click again" turns ivory there to stay distinct from owned
IVORY_MARK = _steps("ivory", 1, 3, 4)
COMBOS = ("RLR", "RRR", "RLL", "RRL")
MIRRORED_COMBOS = ("LRL", "LLL", "LRR", "LLR")

THEMES = {theme.class_id: theme for theme in (
    Theme("warrior", _steps("ember_stone", 0, 1, 2, 3, 4), _steps("crimson", 0, 1, 2, 3, 4, 5), "crimson",
          GOLD_MARK, "cleave", {
              "guardian": ("shield_bash", "iron_hide", "stalwart", "challenging_shout", "second_wind", "bulwark"),
              "berserker": ("leaping_strike", "bloodthirst", "fury", "whirlwind", "relentless", "execute"),
              "duelist": ("lunge", "footwork", "focus", "riposte", "opportunist", "hamstring"),
          }, COMBOS),
    Theme("archer", _steps("dusk_forest", 0, 1, 2, 3, 4), _steps("forest", 0, 1, 2, 3, 4, 5), "forest",
          GOLD_MARK, "vault", {
              "marksman": ("power_shot", "eagle_eye", "steady_aim", "piercing_shot", "weak_spot",
                           "hunters_mark"),
              "skirmisher": ("volley", "fleet_foot", "momentum", "rapid_fire", "light_step", "tumble"),
              "hunter": ("flame_arrow", "tracker", "survivalist", "wolf_companion", "barbed_heads",
                         "frost_arrow"),
          }, MIRRORED_COMBOS),
    Theme("mage", _steps("night_teal", 1, 2, 3, 4, 5), _steps("violet", 0, 1, 2, 3, 4, 5), "violet",
          GOLD_MARK, "blink", {
              "pyromancer": ("fireball", "kindling", "inner_heat", "flame_wave", "ash_siphon", "meteor"),
              "frostweaver": ("ice_lance", "chill_touch", "frost_armor", "frost_nova", "shatter", "blizzard"),
              "lifebinder": ("mending_light", "gentle_soul", "radiance", "sanctuary", "smite", "sunburst"),
          }, COMBOS),
    Theme("captain", _steps("dawn_stone", 0, 1, 2, 3, 4), (("leather", 0),) + _steps("gold", 0, 1, 2, 3, 4),
          "navy", IVORY_MARK, "rallying_strike", {
              "vanguard": ("quarry_mark", "hardened_resolve", "lead_from_the_front", "press_the_attack",
                           "gallant_example", "scattering_shout"),
              "standard_bearer": ("plant_standard", "tall_colours", "close_ranks", "call_herald",
                                  "steadfast_company", "sworn_bond"),
              "warchanter": ("war_ballad", "stirring_melody", "long_refrain", "anthem_of_courage",
                             "clear_voice", "coda"),
          }, COMBOS),
)}
