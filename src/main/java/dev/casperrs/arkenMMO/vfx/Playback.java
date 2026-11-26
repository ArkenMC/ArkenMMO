package dev.casperrs.arkenMMO.vfx;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.Player;
import org.jspecify.annotations.Nullable;

/** One running effect: world positions are worked out per particle as its tick comes. */
final class Playback {

    private final List<ParticleLayer> layers;
    private final List<@Nullable Object> data;
    private final Location origin;
    private final @Nullable Player viewer;
    private final int lastTick;
    private int tick;

    Playback(List<ParticleLayer> layers, Location location, @Nullable Player viewer) {
        this.layers = layers;
        this.origin = location.clone();
        this.viewer = viewer;
        // Read once, so a delayed particle keeps the ground the effect started on
        this.data = new ArrayList<>(layers.size());
        int last = 0;
        for (ParticleLayer layer : layers) {
            data.add(layer.dataAt(origin));
            for (Shapes.Point point : layer.points()) {
                last = Math.max(last, point.tick());
            }
        }
        this.lastTick = last;
    }

    /** Shows the next tick's particles; false once there is nothing left to show. */
    boolean step() {
        if (!canShow()) {
            return false;
        }
        spawn(tick, tick);
        return ++tick <= lastTick;
    }

    /** Shows everything left at once. */
    void finish() {
        if (canShow()) {
            spawn(tick, lastTick);
        }
    }

    private boolean canShow() {
        return origin.isWorldLoaded() && (viewer == null || viewer.isOnline());
    }

    private void spawn(int from, int to) {
        for (int i = 0; i < layers.size(); i++) {
            ParticleLayer layer = layers.get(i);
            for (Shapes.Point point : layer.points()) {
                if (point.tick() >= from && point.tick() <= to) {
                    spawn(layer, data.get(i), point);
                }
            }
        }
    }

    private void spawn(ParticleLayer layer, @Nullable Object particleData, Shapes.Point point) {
        double[] at = Shapes.toWorld(point.position(), origin.getYaw());
        double x = origin.getX() + at[0];
        double y = origin.getY() + at[1];
        double z = origin.getZ() + at[2];
        if (layer.jitter() > 0) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            x += random.nextDouble(-layer.jitter(), layer.jitter());
            y += random.nextDouble(-layer.jitter(), layer.jitter());
            z += random.nextDouble(-layer.jitter(), layer.jitter());
        }
        Shapes.Vec velocity = point.velocity();
        boolean moving = layer.speed() > 0
                && (velocity.right() != 0 || velocity.up() != 0 || velocity.forward() != 0);
        // With count 0 the client reads the offsets as a direction and "extra" as the speed
        int count = moving ? 0 : 1;
        double[] direction = moving ? Shapes.toWorld(velocity, origin.getYaw()) : new double[3];
        double extra = moving ? layer.speed() : 0;
        if (viewer != null) {
            viewer.spawnParticle(layer.particle(), x, y, z, count,
                    direction[0], direction[1], direction[2], extra, particleData);
        } else {
            World world = origin.getWorld();
            world.spawnParticle(layer.particle(), x, y, z, count,
                    direction[0], direction[1], direction[2], extra, particleData);
        }
    }
}
