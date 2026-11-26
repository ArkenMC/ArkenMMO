package dev.casperrs.arkenMMO.warrior;

import dev.casperrs.arkenMMO.casting.SkillAction;
import dev.casperrs.arkenMMO.casting.SkillFeedback;
import dev.casperrs.arkenMMO.combat.SkillDamage;
import dev.casperrs.arkenMMO.combat.SkillTargets;
import dev.casperrs.arkenMMO.skill.SkillValues;
import java.util.Optional;
import org.bukkit.entity.Player;

/** Hits every enemy in a cone ahead. */
public final class Cleave implements SkillAction {

    private final SkillValues values;
    private final SkillDamage damage;
    private final SkillFeedback feedback;

    public Cleave(SkillValues values, SkillDamage damage, SkillFeedback feedback) {
        this.values = values;
        this.damage = damage;
        this.feedback = feedback;
    }

    @Override
    public Optional<Runnable> prepare(Player caster) {
        return Optional.of(() -> {
            feedback.play("skill_warrior_cleave", caster.getLocation());
            damage.deal(caster,
                    SkillTargets.cone(caster, values.number("warrior.cleave.range"),
                            values.number("warrior.cleave.angle")),
                    values.number("warrior.cleave.damage"));
        });
    }
}
