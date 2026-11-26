package dev.casperrs.arkenMMO.combat;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import java.util.function.DoubleSupplier;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;

/**
 * Skill damage, dealt with the player as its source so protection and other plugins treat it as theirs
 * and can cancel it. Main thread only.
 */
public final class SkillDamage {

    private final DoubleSupplier power;
    private final Set<UUID> dealing = new HashSet<>();

    /** {@code power} is what 100% deals, in health points. */
    public SkillDamage(DoubleSupplier power) {
        this.power = power;
    }

    public void deal(Player caster, Collection<LivingEntity> targets, double percent) {
        targets.forEach(target -> deal(caster, target, percent));
    }

    /** Does nothing once the caster is dead, for example from thorns on an earlier target. */
    public void deal(Player caster, LivingEntity target, double percent) {
        double amount = power.getAsDouble() * percent / 100;
        // The set stops a damage listener that leads back here from recursing
        if (amount <= 0 || !caster.isOnline() || caster.isDead() || !SkillTargets.isEnemy(target)
                || !dealing.add(caster.getUniqueId())) {
            return;
        }
        try {
            // Otherwise the half second of immunity after any hit would swallow pulses and combined hits
            target.setNoDamageTicks(0);
            target.damage(amount, caster);
        } finally {
            dealing.remove(caster.getUniqueId());
        }
    }
}
