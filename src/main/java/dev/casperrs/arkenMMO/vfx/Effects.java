package dev.casperrs.arkenMMO.vfx;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;
import org.jspecify.annotations.Nullable;

/** Plays the effects of {@code effects.yml} by ID. Main thread only. */
public final class Effects {

    private final JavaPlugin plugin;
    private final List<Playback> active = new ArrayList<>();
    private final Set<String> reportedUnknown = new HashSet<>();
    private EffectPresets presets;
    private @Nullable BukkitTask ticker;
    private boolean closed;

    private Effects(JavaPlugin plugin, EffectPresets presets) {
        this.plugin = plugin;
        this.presets = presets;
    }

    /** Saves the default {@code effects.yml} if it is missing and loads it. */
    public static Effects load(JavaPlugin plugin) {
        return new Effects(plugin, EffectPresets.load(plugin));
    }

    /**
     * Plays an effect at the location, turned by its yaw (pitch is ignored). With a {@code viewer}
     * only that player sees it; with {@code null} every player nearby does. Unknown IDs are logged once.
     */
    public void play(String effectId, Location location, @Nullable Player viewer) {
        if (closed) {
            return;
        }
        List<ParticleLayer> layers = presets.byId().get(effectId);
        if (layers == null) {
            if (reportedUnknown.add(effectId)) {
                plugin.getLogger().warning("Unknown effect '" + effectId + "'");
            }
            return;
        }
        Playback playback = new Playback(layers, location, viewer);
        if (!playback.step()) {
            return;
        }
        if (active.size() >= presets.maxActiveEffects()) {
            // Over the cap the effect keeps its shape but loses its animation
            playback.finish();
            return;
        }
        active.add(playback);
        if (ticker == null) {
            ticker = plugin.getServer().getScheduler().runTaskTimer(plugin, this::tick, 1, 1);
        }
    }

    /** Reads {@code effects.yml} again and stops the running effects. */
    public void reload() {
        stop();
        reportedUnknown.clear();
        presets = EffectPresets.load(plugin);
    }

    /** Stops the running effects; later calls to {@link #play} do nothing. */
    public void shutdown() {
        closed = true;
        stop();
    }

    private void tick() {
        active.removeIf(playback -> !playback.step());
        if (active.isEmpty()) {
            stop();
        }
    }

    private void stop() {
        active.clear();
        if (ticker != null) {
            ticker.cancel();
            ticker = null;
        }
    }
}
