package dev.casperrs.arkenMMO.sound;

import java.util.Locale;
import org.bukkit.SoundCategory;
import org.bukkit.configuration.ConfigurationSection;
import org.jetbrains.annotations.Nullable;

/** One event of {@code sounds.yml}. {@code fallback} is for players without the resource pack. */
record SoundDef(String key, @Nullable String fallback, float volume, float pitchMin, float pitchMax,
                SoundCategory source) {

    /** Throws {@link IllegalArgumentException} without a key or with an unknown source. */
    static SoundDef read(ConfigurationSection entry) {
        String key = entry.getString("key");
        if (key == null || key.isBlank()) {
            throw new IllegalArgumentException("it has no key");
        }
        float pitchMin = pitch(entry.getDouble("pitch-min", 1));
        return new SoundDef(key, entry.getString("fallback"),
                (float) Math.max(0, entry.getDouble("volume", 1)),
                pitchMin, Math.max(pitchMin, pitch(entry.getDouble("pitch-max", 1))),
                category(entry.getString("source", "master")));
    }

    /** The key this player can hear, or {@code null} if there is none. */
    @Nullable String keyFor(boolean packLoaded) {
        return packLoaded || !key.contains(":") || key.startsWith("minecraft:") ? key : fallback;
    }

    private static float pitch(double value) {
        return (float) Math.clamp(value, 0.5, 2);
    }

    // sounds.yml may use the singular names of Adventure's sources
    private static SoundCategory category(String name) {
        String upper = name.toUpperCase(Locale.ROOT);
        return SoundCategory.valueOf(switch (upper) {
            case "RECORD", "BLOCK", "PLAYER" -> upper + "S";
            default -> upper;
        });
    }
}
