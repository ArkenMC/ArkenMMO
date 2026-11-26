package dev.casperrs.arkenMMO.vfx;

import java.util.List;
import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.block.Block;
import org.bukkit.block.data.BlockData;
import org.jspecify.annotations.Nullable;

/**
 * A loaded layer with its points computed in advance.
 * {@code groundFallback} is set when the particle shows the block under the effect's location.
 */
record ParticleLayer(Particle particle, @Nullable Object data, @Nullable BlockData groundFallback,
                     double speed, double jitter, List<Shapes.Point> points) {

    ParticleLayer withPoints(List<Shapes.Point> kept) {
        return new ParticleLayer(particle, data, groundFallback, speed, jitter, kept);
    }

    /** The particle data for one playback. */
    @Nullable Object dataAt(Location origin) {
        if (groundFallback == null) {
            return data;
        }
        if (!origin.isChunkLoaded()) {
            return groundFallback;
        }
        Block below = origin.clone().subtract(0, 0.1, 0).getBlock();
        return below.getType().isSolid() ? below.getBlockData() : groundFallback;
    }
}
