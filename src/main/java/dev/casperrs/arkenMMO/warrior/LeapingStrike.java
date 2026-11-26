package dev.casperrs.arkenMMO.warrior;

import dev.casperrs.arkenMMO.casting.SkillAction;
import dev.casperrs.arkenMMO.casting.SkillFeedback;
import dev.casperrs.arkenMMO.combat.OngoingAction;
import dev.casperrs.arkenMMO.combat.OngoingActions;
import dev.casperrs.arkenMMO.combat.SkillDamage;
import dev.casperrs.arkenMMO.combat.SkillTargets;
import dev.casperrs.arkenMMO.skill.SkillValues;
import java.util.Optional;
import org.bukkit.FluidCollisionMode;
import org.bukkit.Location;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.util.BoundingBox;
import org.bukkit.util.RayTraceResult;

/** Leaps toward the spot looked at, hits around the landing and prevents the leap's fall damage. */
public final class LeapingStrike implements SkillAction {

    private static final double LIFT = 0.6;
    // How far a launch carries per unit of horizontal speed on level ground: the first tick, then 14 ticks
    // that start at the first tick's drag (ground 0.546, air 0.91) and lose 9% each
    private static final double AIR_DRAG = 0.91;
    private static final double GROUND_DRAG = 0.546;
    private static final double LATER_TICKS_REACH = (1 - Math.pow(AIR_DRAG, 14)) / (1 - AIR_DRAG);

    private final SkillValues values;
    private final SkillDamage damage;
    private final SkillFeedback feedback;
    private final OngoingActions ongoing;

    public LeapingStrike(SkillValues values, SkillDamage damage, SkillFeedback feedback, OngoingActions ongoing) {
        this.values = values;
        this.damage = damage;
        this.feedback = feedback;
        this.ongoing = ongoing;
    }

    @Override
    public Optional<Runnable> prepare(Player caster) {
        return Optional.of(() -> {
            feedback.play("skill_warrior_leaping_strike", caster.getLocation());
            double drag = onGround(caster) ? GROUND_DRAG : AIR_DRAG;
            double speed = distance(caster) / (1 + drag * LATER_TICKS_REACH);
            caster.setVelocity(SkillTargets.heading(caster.getLocation()).multiply(speed).setY(LIFT));
            ongoing.start(caster, new Flight());
        });
    }

    /** Horizontal blocks to cover: up to the block looked at, at most the skill's range. */
    private double distance(Player caster) {
        double range = Math.max(0, values.number("warrior.leaping_strike.range"));
        Location eyes = caster.getEyeLocation();
        // Longer than the range, because the ray to the ground ahead is slanted
        RayTraceResult hit = eyes.getWorld().rayTraceBlocks(
                eyes, eyes.getDirection(), range * 2, FluidCollisionMode.NEVER, true);
        if (hit == null) {
            return range;
        }
        double x = hit.getHitPosition().getX() - eyes.getX();
        double z = hit.getHitPosition().getZ() - eyes.getZ();
        return Math.min(range, Math.hypot(x, z));
    }

    // Player#isOnGround is deprecated because the client reports it, so look for a block under the feet
    private static boolean onGround(Entity entity) {
        BoundingBox body = entity.getBoundingBox();
        return entity.getWorld().hasCollisionsIn(new BoundingBox(body.getMinX(), body.getMinY() - 0.1,
                body.getMinZ(), body.getMaxX(), body.getMinY() - 0.001, body.getMaxZ()));
    }

    private void land(Player caster) {
        caster.setFallDistance(0);
        feedback.play("skill_warrior_leaping_strike_impact", caster.getLocation());
        damage.deal(caster,
                SkillTargets.within(caster, caster.getLocation(),
                        values.number("warrior.leaping_strike.radius")),
                values.number("warrior.leaping_strike.damage"));
    }

    private final class Flight implements OngoingAction {

        // The ground check would still see the take-off block during the first ticks
        private static final int MIN_AIR_TICKS = 5;
        private static final int MAX_TICKS = 200;
        // The client may report the landing, and with it the fall, a little after the server sees ground
        private static final int GRACE_TICKS = 10;

        private int age;
        private int landedAt = -1;

        @Override
        public boolean tick(Player owner) {
            age++;
            if (landedAt >= 0) {
                owner.setFallDistance(0);
                return age - landedAt < GRACE_TICKS;
            }
            // From here on the player moves in a way that has no landing
            if (owner.isGliding() || owner.isFlying() || owner.isInsideVehicle() || owner.isClimbing()) {
                return false;
            }
            if (age >= MIN_AIR_TICKS && (owner.isInWater() || onGround(owner))) {
                landedAt = age;
                land(owner);
                return true;
            }
            return age < MAX_TICKS;
        }

        @Override
        public boolean preventsFallDamage() {
            return true;
        }

        // The fall distance is saved with the player, so quitting mid-air must not keep it
        @Override
        public void cancel(Player owner) {
            owner.setFallDistance(0);
        }
    }
}
