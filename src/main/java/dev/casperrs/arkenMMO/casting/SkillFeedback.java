package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.sound.SoundService;
import dev.casperrs.arkenMMO.vfx.Effects;
import org.bukkit.Location;

/** What everyone hears and sees of a skill. A moment's sound event and effect share one ID. */
public record SkillFeedback(SoundService sounds, Effects effects) {

    /** {@code id} is a sound event and effect ID; {@code at} gives the spot and the yaw the effect faces. */
    public void play(String id, Location at) {
        Location level = at.clone();
        level.setPitch(0);
        sounds.playAt(level, id);
        effects.play(id, level, null);
    }
}
