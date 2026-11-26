package dev.casperrs.arkenMMO.casting;

import java.util.HashMap;
import java.util.Map;
import org.jetbrains.annotations.Nullable;

/** One player's mana, cooldowns and repeat costs. Times are milliseconds on one monotonic clock. */
final class CasterState {

    /** {@code repeats} counts the quick recasts that led to this cast. */
    private record Cast(long at, long readyAt, int repeats) {
    }

    private final ManaRules rules;
    private final Map<String, Cast> lastCasts = new HashMap<>();
    private double mana;
    private long updatedAt;
    private long calmAt;

    CasterState(ManaRules rules, long now) {
        this.rules = rules;
        this.mana = rules.max();
        this.updatedAt = now;
        this.calmAt = now;
    }

    /** Regeneration is worked out when asked, so nothing has to tick. */
    double mana(long now) {
        long elapsed = Math.max(0, now - updatedAt);
        long fighting = Math.clamp(calmAt - updatedAt, 0, elapsed);
        mana = Math.min(rules.max(),
                mana + (fighting * rules.regen() + (elapsed - fighting) * rules.calmRegen()) / 1000);
        updatedAt += elapsed;
        return mana;
    }

    void fight(long now) {
        mana(now);
        calmAt = now + rules.calmAfterMillis();
    }

    long cooldownLeft(String skillId, long now) {
        Cast last = lastCasts.get(skillId);
        return last == null ? 0 : Math.max(0, last.readyAt() - now);
    }

    /** What the skill costs now, with the surcharge for recasting it quickly. */
    double cost(String skillId, double baseCost, long now) {
        int repeats = repeats(lastCasts.get(skillId), now);
        return baseCost * (1 + Math.min(rules.repeatMax(), repeats * rules.repeatStep()));
    }

    void cast(String skillId, double cost, long cooldownMillis, long now) {
        mana = Math.max(0, mana(now) - cost);
        lastCasts.put(skillId, new Cast(now, now + cooldownMillis, repeats(lastCasts.get(skillId), now)));
    }

    private int repeats(@Nullable Cast last, long now) {
        return last != null && now - last.at() <= rules.repeatWindowMillis() ? last.repeats() + 1 : 0;
    }
}
