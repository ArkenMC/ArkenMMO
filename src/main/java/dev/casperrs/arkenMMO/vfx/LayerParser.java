package dev.casperrs.arkenMMO.vfx;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.Particle;
import org.bukkit.block.data.BlockData;
import org.jspecify.annotations.Nullable;

/** Reads one layer of effects.yml (format at the top of that file). */
final class LayerParser {

    private static final String GROUND = "ground";
    private static final String GROUND_FALLBACK = "minecraft:coarse_dirt";

    private LayerParser() {
    }

    /** Throws IllegalArgumentException with a readable reason for any bad value. */
    static ParticleLayer parse(Map<?, ?> values) {
        LayerSettings settings = new LayerSettings(values);
        String type = settings.requiredText("type");
        if (!type.equals("particle")) {
            throw new IllegalArgumentException("unknown layer type '" + type + "'");
        }
        Particle particle = particle(settings.requiredText("particle"));
        Class<?> dataType = particle.getDataType();
        BlockData groundFallback = null;
        Object data = null;
        if (dataType == BlockData.class) {
            String block = settings.requiredText("block");
            if (block.equals(GROUND)) {
                groundFallback = Bukkit.createBlockData(GROUND_FALLBACK);
            } else {
                data = Bukkit.createBlockData(block);
            }
        } else {
            data = data(particle, dataType, settings);
        }
        double speed = settings.number("speed", 0, 0, 4);
        double jitter = settings.number("jitter", 0, 0, 2);
        List<Shapes.Point> points = points(settings);
        settings.rejectUnread();
        return new ParticleLayer(particle, data, groundFallback, speed, jitter, points);
    }

    private static Particle particle(String name) {
        try {
            return Particle.valueOf(name.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("unknown particle '" + name + "'", e);
        }
    }

    private static @Nullable Object data(Particle particle, Class<?> type, LayerSettings settings) {
        if (type == Void.class) {
            return null;
        }
        if (type == Particle.DustOptions.class) {
            return new Particle.DustOptions(color(settings, "color"), size(settings));
        }
        if (type == Particle.DustTransition.class) {
            return new Particle.DustTransition(
                    color(settings, "color"), color(settings, "to-color"), size(settings));
        }
        if (type == Color.class) {
            return color(settings, "color");
        }
        throw new IllegalArgumentException("particle '" + particle.name().toLowerCase(Locale.ROOT)
                + "' needs data this engine doesn't support");
    }

    private static Color color(LayerSettings settings, String key) {
        String hex = settings.requiredText(key);
        if (!hex.matches("#[0-9a-f]{6}")) {
            throw new IllegalArgumentException("'" + key + "' must be \"#rrggbb\", not " + hex);
        }
        return Color.fromRGB(Integer.parseInt(hex.substring(1), 16));
    }

    private static float size(LayerSettings settings) {
        return (float) settings.number("size", 1, 0.1, 4);
    }

    private static List<Shapes.Point> points(LayerSettings settings) {
        String shape = settings.requiredText("shape");
        Shapes.Timing timing = new Shapes.Timing(
                settings.whole("points", 1, 1, 500),
                settings.whole("delay-ticks", 0, 0, 100),
                settings.whole("duration-ticks", 1, 1, 100));
        Shapes.Movement movement = new Shapes.Movement(
                motion(settings.text("motion", "none")), settings.number("lift", 0, -4, 4));
        return switch (shape) {
            case "arc" -> arc(settings, timing, movement);
            case "line" -> Shapes.line(settings.vector("from"), settings.vector("to"), timing, movement);
            default -> throw new IllegalArgumentException("unknown shape '" + shape + "'");
        };
    }

    private static List<Shapes.Point> arc(LayerSettings settings, Shapes.Timing timing, Shapes.Movement movement) {
        double radius = settings.number("radius", 1, 0, 16);
        double y = settings.number("y", 0, -4, 8);
        return Shapes.arc(
                settings.number("start-angle", 0, -720, 720),
                settings.number("sweep", 360, -720, 720),
                radius, settings.number("end-radius", radius, 0, 16),
                y, settings.number("end-y", y, -4, 8),
                timing, movement);
    }

    private static Shapes.Motion motion(String name) {
        try {
            return Shapes.Motion.valueOf(name.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("unknown motion '" + name + "'", e);
        }
    }
}
