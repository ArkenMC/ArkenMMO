package dev.casperrs.arkenMMO.combat;

import org.bukkit.entity.Player;

/** A skill that keeps going after the cast: a channel, a delayed hit or a leap. */
public interface OngoingAction {

    /** Runs once a tick, starting the tick after the cast. {@code false} ends the action. */
    boolean tick(Player owner);

    default boolean preventsFallDamage() {
        return false;
    }

    /** Called when the action is ended early: quit, death, world change or plugin disable. */
    default void cancel(Player owner) {
    }
}
