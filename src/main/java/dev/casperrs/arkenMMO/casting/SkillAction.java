package dev.casperrs.arkenMMO.casting;

import java.util.Optional;
import org.bukkit.entity.Player;

/** What one castable skill does. */
public interface SkillAction {

    /**
     * Checks that the skill can be used now, changing nothing. Running the result performs it; empty means
     * there is no target, and the cast then costs nothing.
     */
    Optional<Runnable> prepare(Player caster);
}
