package dev.casperrs.arkenMMO.vfx;

import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/** One layer's raw values. Reading records the keys, so misspelt ones can be reported. */
final class LayerSettings {

    private final Map<?, ?> values;
    private final Set<Object> read = new HashSet<>();

    LayerSettings(Map<?, ?> values) {
        this.values = values;
    }

    String text(String key, String fallback) {
        Object value = value(key);
        return value == null ? fallback : value.toString().trim().toLowerCase(Locale.ROOT);
    }

    String requiredText(String key) {
        String text = text(key, null);
        if (text == null) {
            throw new IllegalArgumentException("'" + key + "' is missing");
        }
        return text;
    }

    double number(String key, double fallback, double min, double max) {
        Object value = value(key);
        return value == null ? fallback : checked(key, value, min, max);
    }

    int whole(String key, int fallback, int min, int max) {
        double number = number(key, fallback, min, max);
        if (number != Math.rint(number)) {
            throw new IllegalArgumentException("'" + key + "' must be a whole number");
        }
        return (int) number;
    }

    Shapes.Vec vector(String key) {
        if (!(value(key) instanceof List<?> list) || list.size() != 3) {
            throw new IllegalArgumentException("'" + key + "' must be [right, up, forward]");
        }
        return new Shapes.Vec(
                checked(key, list.get(0), -16, 16),
                checked(key, list.get(1), -16, 16),
                checked(key, list.get(2), -16, 16));
    }

    void rejectUnread() {
        for (Object key : values.keySet()) {
            if (!read.contains(key)) {
                throw new IllegalArgumentException("'" + key + "' is not used by this layer");
            }
        }
    }

    private Object value(String key) {
        read.add(key);
        return values.get(key);
    }

    private static double checked(String key, Object value, double min, double max) {
        if (value instanceof Number number && number.doubleValue() >= min && number.doubleValue() <= max) {
            return number.doubleValue();
        }
        throw new IllegalArgumentException(
                "'" + key + "' must be a number from " + min + " to " + max + ", not " + value);
    }
}
