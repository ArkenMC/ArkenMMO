package dev.casperrs.arkenMMO.sound;

import java.util.Locale;
import java.util.function.Consumer;
import net.kyori.adventure.key.Key;
import org.bukkit.SoundCategory;
import org.bukkit.configuration.ConfigurationSection;
import org.jetbrains.annotations.Nullable;

/** One event of {@code sounds.yml}; {@code key} is the sound that gets played. */
record SoundDef(String key, float volume, float pitchMin, float pitchMax, SoundCategory source) {

    /**
     * The entry's {@code fallback} only replaces a blank or invalid {@code key}: the server can't know whether
     * a client has a custom sound. Throws {@link IllegalArgumentException} if neither can be used.
     */
    static SoundDef read(ConfigurationSection entry, Consumer<String> warn) {
        float pitchMin = pitch(entry.getDouble("pitch-min", 1));
        return new SoundDef(playedKey(entry, warn),
                (float) Math.max(0, entry.getDouble("volume", 1)),
                pitchMin, Math.max(pitchMin, pitch(entry.getDouble("pitch-max", 1))),
                category(entry.getString("source", "master"), warn));
    }

    private static String playedKey(ConfigurationSection entry, Consumer<String> warn) {
        String key = entry.getString("key", "");
        if (isKey(key)) {
            return key;
        }
        String fallback = entry.getString("fallback");
        if (!isKey(fallback)) {
            throw new IllegalArgumentException("neither its key nor its fallback is a sound key");
        }
        if (!key.isBlank()) {
            warn.accept("'" + key + "' is not a sound key, so the fallback is played");
        }
        return fallback;
    }

    private static boolean isKey(@Nullable String key) {
        return key != null && !key.isBlank() && !key.endsWith(":") && Key.parseable(key);
    }

    private static float pitch(double value) {
        return (float) Math.clamp(value, 0.5, 2);
    }

    // sounds.yml may use the singular names of Adventure's sources
    private static SoundCategory category(String name, Consumer<String> warn) {
        String upper = name.toUpperCase(Locale.ROOT);
        String wanted = switch (upper) {
            case "RECORD", "BLOCK", "PLAYER" -> upper + "S";
            default -> upper;
        };
        for (SoundCategory category : SoundCategory.values()) {
            if (category.name().equals(wanted)) {
                return category;
            }
        }
        warn.accept("unknown source '" + name + "', so master is used");
        return SoundCategory.MASTER;
    }
}
