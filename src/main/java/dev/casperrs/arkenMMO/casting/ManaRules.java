package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.skill.SkillValues;

/**
 * The {@code mana} section of {@code skill-values.yml}. Regeneration is per second; the repeat values are
 * shares of a skill's base cost (0.25 = 25% more).
 */
public record ManaRules(double max, double regen, double calmRegen, long calmAfterMillis,
                        long repeatWindowMillis, double repeatStep, double repeatMax) {

    public static ManaRules read(SkillValues values) {
        return new ManaRules(
                values.number("mana.max"),
                values.number("mana.regen"),
                values.number("mana.calm_regen"),
                Math.round(values.number("mana.calm_after") * 1000),
                Math.round(values.number("mana.repeat_window") * 1000),
                values.number("mana.repeat_step") / 100,
                values.number("mana.repeat_max") / 100);
    }
}
