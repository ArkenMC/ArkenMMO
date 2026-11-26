package dev.casperrs.arkenMMO.combat;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.bukkit.FluidCollisionMode;
import org.bukkit.Location;
import org.bukkit.entity.AbstractVillager;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Mannequin;
import org.bukkit.entity.Player;
import org.bukkit.entity.Tameable;
import org.bukkit.util.BoundingBox;
import org.bukkit.util.RayTraceResult;
import org.bukkit.util.Vector;

/** Which entities skills may hit (PvE only) and the shapes they are searched in. */
public final class SkillTargets {

    // Extra thickness of the aiming ray, so a target doesn't need a pixel-exact crosshair
    private static final double AIM_WIDTH = 0.3;
    private static final double CHEST_HEIGHT = 1;
    // A target this close to the middle has no meaningful direction, so a cone always includes it
    private static final double POINT_BLANK = 0.5;

    private SkillTargets() {
    }

    public static boolean isEnemy(Entity entity) {
        return entity instanceof LivingEntity living && living.isValid() && !living.isDead()
                && !(entity instanceof Player)
                && !(entity instanceof ArmorStand)
                && !(entity instanceof Mannequin)
                && !(entity instanceof AbstractVillager)
                && !(entity instanceof Tameable tameable && tameable.isTamed());
    }

    /** Enemies in sight of the caster with any part of them within {@code radius} blocks of {@code feet}. */
    public static List<LivingEntity> within(Player caster, Location feet, double radius) {
        Location center = feet.clone().add(0, CHEST_HEIGHT, 0);
        List<LivingEntity> found = new ArrayList<>();
        for (LivingEntity entity : center.getWorld().getNearbyLivingEntities(center, radius, SkillTargets::isEnemy)) {
            if (distanceSquared(entity.getBoundingBox(), center) <= radius * radius
                    && caster.hasLineOfSight(entity)) {
                found.add(entity);
            }
        }
        return found;
    }

    /** Like {@link #within} around the caster, limited to a horizontal cone of {@code degrees} ahead. */
    public static List<LivingEntity> cone(Player caster, double range, double degrees) {
        Location feet = caster.getLocation();
        Vector facing = heading(feet);
        double minDot = Math.cos(Math.toRadians(Math.clamp(degrees, 0, 360) / 2));
        return within(caster, feet, range).stream().filter(entity -> {
            Vector to = entity.getBoundingBox().getCenter().subtract(feet.toVector()).setY(0);
            double length = to.length();
            return length < POINT_BLANK || facing.dot(to) / length >= minDot;
        }).toList();
    }

    /** The first enemy under the crosshair within {@code range} blocks, not through walls. */
    public static Optional<LivingEntity> aimed(Player caster, double range) {
        Location eyes = caster.getEyeLocation();
        RayTraceResult hit = eyes.getWorld().rayTrace(eyes, eyes.getDirection(), range,
                FluidCollisionMode.NEVER, true, AIM_WIDTH, SkillTargets::isEnemy);
        return Optional.ofNullable(hit)
                .map(RayTraceResult::getHitEntity)
                .map(LivingEntity.class::cast);
    }

    /** The level unit vector the location's yaw points along. */
    public static Vector heading(Location location) {
        double yaw = Math.toRadians(location.getYaw());
        return new Vector(-Math.sin(yaw), 0, Math.cos(yaw));
    }

    private static double distanceSquared(BoundingBox box, Location point) {
        double x = Math.clamp(point.getX(), box.getMinX(), box.getMaxX()) - point.getX();
        double y = Math.clamp(point.getY(), box.getMinY(), box.getMaxY()) - point.getY();
        double z = Math.clamp(point.getZ(), box.getMinZ(), box.getMaxZ()) - point.getZ();
        return x * x + y * y + z * z;
    }
}
