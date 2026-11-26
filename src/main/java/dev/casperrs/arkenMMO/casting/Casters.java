package dev.casperrs.arkenMMO.casting;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import org.bukkit.entity.Player;

/**
 * Every player's {@link CasterState}. Kept until the server restarts, so relogging doesn't refill mana or
 * clear cooldowns. Main thread only.
 */
public final class Casters {

    private final ManaRules rules;
    private final Map<UUID, CasterState> states = new HashMap<>();

    public Casters(ManaRules rules) {
        this.rules = rules;
    }

    CasterState of(Player player) {
        return states.computeIfAbsent(player.getUniqueId(), id -> new CasterState(rules, now()));
    }

    int maxMana() {
        return (int) rules.max();
    }

    /** The clock for {@link CasterState}. */
    static long now() {
        return System.nanoTime() / 1_000_000;
    }
}
