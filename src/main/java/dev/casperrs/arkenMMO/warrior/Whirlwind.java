package dev.casperrs.arkenMMO.warrior;

import dev.casperrs.arkenMMO.casting.SkillAction;
import dev.casperrs.arkenMMO.casting.SkillFeedback;
import dev.casperrs.arkenMMO.combat.OngoingAction;
import dev.casperrs.arkenMMO.combat.OngoingActions;
import dev.casperrs.arkenMMO.combat.SkillDamage;
import dev.casperrs.arkenMMO.combat.SkillTargets;
import dev.casperrs.arkenMMO.skill.SkillValues;
import java.util.Optional;
import org.bukkit.entity.Player;

/** Several pulses around the caster, spread over the spin: the first at once, the rest at even steps. */
public final class Whirlwind implements SkillAction {

    private final SkillValues values;
    private final SkillDamage damage;
    private final SkillFeedback feedback;
    private final OngoingActions ongoing;

    public Whirlwind(SkillValues values, SkillDamage damage, SkillFeedback feedback, OngoingActions ongoing) {
        this.values = values;
        this.damage = damage;
        this.feedback = feedback;
        this.ongoing = ongoing;
    }

    @Override
    public Optional<Runnable> prepare(Player caster) {
        return Optional.of(() -> {
            int count = (int) Math.max(1, values.number("warrior.whirlwind.count"));
            int interval = (int) Math.max(1,
                    Math.round(values.number("warrior.whirlwind.duration") * 20 / count));
            // Registered before the first pulse, so that a death during it also ends the spin
            if (count > 1) {
                ongoing.start(caster, new Spin(count - 1, interval));
            }
            pulse(caster);
        });
    }

    private void pulse(Player caster) {
        feedback.play("skill_warrior_whirlwind", caster.getLocation());
        damage.deal(caster,
                SkillTargets.within(caster, caster.getLocation(), values.number("warrior.whirlwind.radius")),
                values.number("warrior.whirlwind.damage"));
    }

    private final class Spin implements OngoingAction {

        private final int interval;
        private int pulsesLeft;
        private int age;

        private Spin(int pulsesLeft, int interval) {
            this.pulsesLeft = pulsesLeft;
            this.interval = interval;
        }

        @Override
        public boolean tick(Player owner) {
            if (++age % interval != 0) {
                return true;
            }
            pulse(owner);
            return --pulsesLeft > 0;
        }
    }
}
