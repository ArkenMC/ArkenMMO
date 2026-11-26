package dev.casperrs.arkenMMO.skill;

import org.bukkit.configuration.file.FileConfiguration;

/** The level and skill points every player has until levelling exists. */
public record SkillSettings(int testLevel, int testPoints) {

    static final int MAX_LEVEL = 30;

    public static SkillSettings read(FileConfiguration config) {
        return new SkillSettings(
                Math.clamp(config.getInt("skills.test-level"), 1, MAX_LEVEL),
                Math.max(0, config.getInt("skills.test-points")));
    }
}
