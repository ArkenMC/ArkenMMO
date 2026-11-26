package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.ArrayList;
import java.util.List;

/** Every class's skills. The keys are fixed: they are stored with players and name resource pack art. */
public final class SkillCatalog {

    private static final ClassTree WARRIOR = tree(PlayerClass.WARRIOR, "cleave",
            archetype(PlayerClass.WARRIOR, "guardian",
                    "shield_bash", "iron_hide", "stalwart", "challenging_shout", "second_wind", "bulwark"),
            archetype(PlayerClass.WARRIOR, "berserker",
                    "leaping_strike", "bloodthirst", "fury", "whirlwind", "relentless", "execute"),
            archetype(PlayerClass.WARRIOR, "duelist",
                    "lunge", "footwork", "focus", "riposte", "opportunist", "hamstring"));

    private static final ClassTree ARCHER = tree(PlayerClass.ARCHER, "vault",
            archetype(PlayerClass.ARCHER, "marksman",
                    "power_shot", "eagle_eye", "steady_aim", "piercing_shot", "weak_spot", "hunters_mark"),
            archetype(PlayerClass.ARCHER, "skirmisher",
                    "volley", "fleet_foot", "momentum", "rapid_fire", "light_step", "tumble"),
            archetype(PlayerClass.ARCHER, "hunter",
                    "flame_arrow", "tracker", "survivalist", "wolf_companion", "barbed_heads", "frost_arrow"));

    private static final ClassTree MAGE = tree(PlayerClass.MAGE, "blink",
            archetype(PlayerClass.MAGE, "pyromancer",
                    "fireball", "kindling", "inner_heat", "flame_wave", "ash_siphon", "meteor"),
            archetype(PlayerClass.MAGE, "frostweaver",
                    "ice_lance", "chill_touch", "frost_armor", "frost_nova", "shatter", "blizzard"),
            archetype(PlayerClass.MAGE, "lifebinder",
                    "mending_light", "gentle_soul", "radiance", "sanctuary", "smite", "sunburst"));

    private static final ClassTree CAPTAIN = tree(PlayerClass.CAPTAIN, "rallying_strike",
            archetype(PlayerClass.CAPTAIN, "vanguard",
                    "quarry_mark", "hardened_resolve", "lead_from_the_front", "press_the_attack",
                    "gallant_example", "scattering_shout"),
            archetype(PlayerClass.CAPTAIN, "standard_bearer",
                    "plant_standard", "tall_colours", "close_ranks", "call_herald", "steadfast_company",
                    "sworn_bond"),
            archetype(PlayerClass.CAPTAIN, "warchanter",
                    "war_ballad", "stirring_melody", "long_refrain", "anthem_of_courage", "clear_voice", "coda"));

    private SkillCatalog() {
    }

    public static ClassTree of(PlayerClass playerClass) {
        return switch (playerClass) {
            case WARRIOR -> WARRIOR;
            case ARCHER -> ARCHER;
            case MAGE -> MAGE;
            case CAPTAIN -> CAPTAIN;
        };
    }

    private static ClassTree tree(PlayerClass playerClass, String core, ClassTree.Archetype... archetypes) {
        return new ClassTree(playerClass, new Skill(playerClass, core, null, null), List.of(archetypes));
    }

    private static ClassTree.Archetype archetype(PlayerClass playerClass, String key, String... skillKeys) {
        SkillNode[] nodes = SkillNode.values();
        if (skillKeys.length != nodes.length) {
            throw new IllegalArgumentException(key + " needs " + nodes.length + " skills");
        }
        List<Skill> skills = new ArrayList<>(nodes.length);
        for (SkillNode node : nodes) {
            skills.add(new Skill(playerClass, skillKeys[node.ordinal()], key, node));
        }
        return new ClassTree.Archetype(key, List.copyOf(skills));
    }
}
