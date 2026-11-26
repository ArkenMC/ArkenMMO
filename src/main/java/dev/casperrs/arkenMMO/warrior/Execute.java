package dev.casperrs.arkenMMO.warrior;

import dev.casperrs.arkenMMO.casting.SkillAction;
import dev.casperrs.arkenMMO.casting.SkillFeedback;
import dev.casperrs.arkenMMO.combat.SkillDamage;
import dev.casperrs.arkenMMO.combat.SkillTargets;
import dev.casperrs.arkenMMO.skill.SkillValues;
import java.util.Objects;
import java.util.Optional;
import org.bukkit.Location;
import org.bukkit.attribute.Attribute;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;

/** A heavy hit on the enemy aimed at, much heavier when it is low on health. */
public final class Execute implements SkillAction {

    private final SkillValues values;
    private final SkillDamage damage;
    private final SkillFeedback feedback;

    public Execute(SkillValues values, SkillDamage damage, SkillFeedback feedback) {
        this.values = values;
        this.damage = damage;
        this.feedback = feedback;
    }

    @Override
    public Optional<Runnable> prepare(Player caster) {
        return SkillTargets.aimed(caster, values.number("warrior.execute.range"))
                .map(target -> () -> strike(caster, target));
    }

    private void strike(Player caster, LivingEntity target) {
        double maxHealth = Objects.requireNonNull(target.getAttribute(Attribute.MAX_HEALTH)).getValue();
        boolean low = target.getHealth() < maxHealth * values.number("warrior.execute.threshold") / 100;
        // Before the damage, while the target is still where it is hit
        Location feet = target.getLocation();
        feet.setYaw(caster.getYaw());
        feedback.play(low ? "skill_warrior_execute_low" : "skill_warrior_execute", feet);
        damage.deal(caster, target,
                values.number(low ? "warrior.execute.finisher" : "warrior.execute.damage"));
    }
}
