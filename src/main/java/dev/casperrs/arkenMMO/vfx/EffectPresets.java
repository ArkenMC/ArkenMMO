package dev.casperrs.arkenMMO.vfx;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.logging.Logger;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

/** The presets and limits of {@code effects.yml}; effects it leaves out come from the bundled file. */
record EffectPresets(Map<String, List<ParticleLayer>> byId, int maxActiveEffects) {

    private static final String FILE_NAME = "effects.yml";
    private static final String LIMITS = "limits";

    static EffectPresets load(JavaPlugin plugin) {
        File file = new File(plugin.getDataFolder(), FILE_NAME);
        if (!file.exists()) {
            plugin.saveResource(FILE_NAME, false);
        }
        YamlConfiguration yaml = YamlConfiguration.loadConfiguration(file);
        YamlConfiguration bundled = bundled(plugin);
        int maxParticles = limit(yaml, bundled, "max-particles-per-effect");
        Set<String> ids = new LinkedHashSet<>(bundled.getKeys(false));
        ids.addAll(yaml.getKeys(false));
        ids.remove(LIMITS);
        Map<String, List<ParticleLayer>> presets = new HashMap<>();
        for (String id : ids) {
            YamlConfiguration source = yaml.contains(id) ? yaml : bundled;
            List<ParticleLayer> layers = layers(source.getMapList(id + ".layers"), id, plugin.getLogger());
            if (!layers.isEmpty()) {
                presets.put(id, capped(layers, maxParticles, id, plugin.getLogger()));
            }
        }
        return new EffectPresets(Map.copyOf(presets), limit(yaml, bundled, "max-active-effects"));
    }

    private static YamlConfiguration bundled(JavaPlugin plugin) {
        try (Reader reader = new InputStreamReader(
                Objects.requireNonNull(plugin.getResource(FILE_NAME)), StandardCharsets.UTF_8)) {
            return YamlConfiguration.loadConfiguration(reader);
        } catch (IOException e) {
            throw new UncheckedIOException("Could not read the bundled " + FILE_NAME, e);
        }
    }

    private static int limit(YamlConfiguration yaml, YamlConfiguration bundled, String key) {
        String path = LIMITS + "." + key;
        return Math.max(1, yaml.getInt(path, bundled.getInt(path)));
    }

    private static List<ParticleLayer> layers(List<Map<?, ?>> raw, String id, Logger logger) {
        List<ParticleLayer> layers = new ArrayList<>(raw.size());
        for (int i = 0; i < raw.size(); i++) {
            try {
                layers.add(LayerParser.parse(raw.get(i)));
            } catch (IllegalArgumentException e) {
                logger.warning(FILE_NAME + ": skipped layer " + (i + 1) + " of '" + id + "': " + e.getMessage());
            }
        }
        if (layers.isEmpty()) {
            logger.warning(FILE_NAME + ": effect '" + id + "' has no usable layers");
        }
        return List.copyOf(layers);
    }

    /** Thins every layer evenly when the effect has more particles than allowed. */
    private static List<ParticleLayer> capped(List<ParticleLayer> layers, int max, String id, Logger logger) {
        int total = layers.stream().mapToInt(layer -> layer.points().size()).sum();
        if (total <= max) {
            return layers;
        }
        logger.warning(FILE_NAME + ": effect '" + id + "' has " + total + " particles; thinned to " + max);
        List<ParticleLayer> thinned = new ArrayList<>(layers.size());
        long seen = 0;
        for (ParticleLayer layer : layers) {
            List<Shapes.Point> kept = new ArrayList<>();
            for (Shapes.Point point : layer.points()) {
                if ((seen + 1) * max / total > seen * max / total) {
                    kept.add(point);
                }
                seen++;
            }
            thinned.add(layer.withPoints(List.copyOf(kept)));
        }
        return List.copyOf(thinned);
    }
}
