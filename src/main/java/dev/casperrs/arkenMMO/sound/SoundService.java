package dev.casperrs.arkenMMO.sound;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Logger;
import org.bukkit.Location;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.Nullable;

/** Plays the events of {@code sounds.yml}; the only place that plays sounds. Main thread only. */
public final class SoundService {

    private static final String FILE_NAME = "sounds.yml";
    // A sound of volume 1 or less carries this many blocks
    private static final double AUDIBLE_RANGE = 16;

    private final Map<String, SoundDef> sounds;
    private final Logger logger;
    private final Set<String> unknown = new HashSet<>();

    private SoundService(Map<String, SoundDef> sounds, Logger logger) {
        this.sounds = Map.copyOf(sounds);
        this.logger = logger;
    }

    /** The server's file wins over the bundled one, event by event. Without either, nothing is played. */
    public static SoundService load(JavaPlugin plugin) {
        Map<String, SoundDef> sounds = new HashMap<>();
        // The bundled file and the server's copy can share a mistake; it is reported once
        Set<String> warnings = new LinkedHashSet<>();
        File file = new File(plugin.getDataFolder(), FILE_NAME);
        try (InputStream bundled = plugin.getResource(FILE_NAME)) {
            if (bundled != null) {
                if (!file.exists()) {
                    plugin.saveResource(FILE_NAME, false);
                }
                try (Reader reader = new InputStreamReader(bundled, StandardCharsets.UTF_8)) {
                    read(YamlConfiguration.loadConfiguration(reader), sounds, warnings);
                }
            }
        } catch (IOException e) {
            throw new UncheckedIOException("Could not read the bundled " + FILE_NAME, e);
        }
        if (file.exists()) {
            read(YamlConfiguration.loadConfiguration(file), sounds, warnings);
        }
        warnings.forEach(plugin.getLogger()::warning);
        if (sounds.isEmpty()) {
            plugin.getLogger().warning("No sounds in " + FILE_NAME + ", so the plugin is silent.");
        }
        return new SoundService(sounds, plugin.getLogger());
    }

    /** Only this player hears it. */
    public void playTo(Player listener, String event) {
        SoundDef sound = find(event);
        if (sound != null) {
            play(listener, listener.getLocation(), sound, pitch(sound));
        }
    }

    /** Everyone near the spot hears it. */
    public void playAt(Location at, String event) {
        SoundDef sound = find(event);
        if (sound == null) {
            return;
        }
        double range = AUDIBLE_RANGE * Math.max(1, sound.volume());
        float pitch = pitch(sound);
        for (Player listener : at.getWorld().getPlayers()) {
            if (listener.getLocation().distanceSquared(at) <= range * range) {
                play(listener, at, sound, pitch);
            }
        }
    }

    private static void read(YamlConfiguration yaml, Map<String, SoundDef> sounds, Set<String> warnings) {
        for (String event : yaml.getKeys(false)) {
            ConfigurationSection entry = yaml.getConfigurationSection(event);
            if (entry == null) {
                continue;
            }
            String where = FILE_NAME + ", sound " + event + ": ";
            try {
                sounds.put(event, SoundDef.read(entry, problem -> warnings.add(where + problem)));
            } catch (IllegalArgumentException e) {
                warnings.add(where + "ignored, " + e.getMessage());
            }
        }
    }

    private @Nullable SoundDef find(String event) {
        SoundDef sound = sounds.get(event);
        // An empty file was already reported at startup
        if (sound == null && !sounds.isEmpty() && unknown.add(event)) {
            logger.warning(FILE_NAME + " has no sound " + event);
        }
        return sound;
    }

    private static void play(Player listener, Location at, SoundDef sound, float pitch) {
        listener.playSound(at, sound.key(), sound.source(), sound.volume(), pitch);
    }

    private static float pitch(SoundDef sound) {
        return sound.pitchMin()
                + ThreadLocalRandom.current().nextFloat() * (sound.pitchMax() - sound.pitchMin());
    }
}
