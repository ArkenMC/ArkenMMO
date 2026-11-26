package dev.casperrs.arkenMMO.casting;

import org.bukkit.Location;

/** Where skills' visual effects are played. Everyone sees them. */
@FunctionalInterface
public interface SkillEffects {

    void play(String effectId, Location location);
}
