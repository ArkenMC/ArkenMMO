package dev.casperrs.arkenMMO.vfx;

import java.util.ArrayList;
import java.util.List;

/**
 * Shape maths without Bukkit types (design/vfx-scripts runs it for the previews).
 * Local frame in blocks: right, up, forward. Angles in degrees, 0 = forward, positive = to the right.
 */
public final class Shapes {

    /** OUTWARD points away from the vertical axis; SPIN follows the direction an arc is drawn in. */
    public enum Motion { NONE, OUTWARD, UP, SPIN }

    public record Vec(double right, double up, double forward) {}

    /** {@code velocity} is a direction for the particle, zero when it doesn't move; {@code tick} counts from the start. */
    public record Point(Vec position, Vec velocity, int tick) {}

    /** Points appear in order, spread over {@code duration} ticks (1 = all at once) after {@code delay} ticks. */
    public record Timing(int points, int delay, int duration) {

        int tickOf(int index) {
            return delay + index * duration / points;
        }
    }

    /** {@code lift} is the upward part added to a moving particle's direction. */
    public record Movement(Motion motion, double lift) {}

    private static final Vec STILL = new Vec(0, 0, 0);

    private Shapes() {
    }

    /** A flat, tilted or spiralling arc; a sweep of 360 or more is a ring without a doubled end point. */
    public static List<Point> arc(double startAngle, double sweep, double startRadius, double endRadius,
                                  double startY, double endY, Timing timing, Movement movement) {
        boolean closed = Math.abs(sweep) >= 360;
        List<Point> points = new ArrayList<>(timing.points());
        for (int i = 0; i < timing.points(); i++) {
            double t = fraction(i, timing.points(), closed);
            double angle = Math.toRadians(startAngle + sweep * t);
            double radius = lerp(startRadius, endRadius, t);
            double sin = Math.sin(angle);
            double cos = Math.cos(angle);
            Vec position = new Vec(sin * radius, lerp(startY, endY, t), cos * radius);
            double turn = Math.signum(sweep);
            Vec velocity = velocity(movement, new Vec(sin, 0, cos), new Vec(cos * turn, 0, -sin * turn));
            points.add(new Point(position, velocity, timing.tickOf(i)));
        }
        return points;
    }

    /** A straight line including both ends. OUTWARD and SPIN both move along the line. */
    public static List<Point> line(Vec from, Vec to, Timing timing, Movement movement) {
        double right = to.right() - from.right();
        double up = to.up() - from.up();
        double forward = to.forward() - from.forward();
        double length = Math.sqrt(right * right + up * up + forward * forward);
        Vec along = length == 0 ? STILL : new Vec(right / length, up / length, forward / length);
        Vec velocity = velocity(movement, along, along);
        List<Point> points = new ArrayList<>(timing.points());
        for (int i = 0; i < timing.points(); i++) {
            double t = fraction(i, timing.points(), false);
            Vec position = new Vec(from.right() + right * t, from.up() + up * t, from.forward() + forward * t);
            points.add(new Point(position, velocity, timing.tickOf(i)));
        }
        return points;
    }

    /** Turns a local vector into world x, y, z (returned in that order) for a Minecraft yaw. */
    public static double[] toWorld(Vec local, float yaw) {
        double radians = Math.toRadians(yaw);
        double sin = Math.sin(radians);
        double cos = Math.cos(radians);
        return new double[] {
            -cos * local.right() - sin * local.forward(),
            local.up(),
            -sin * local.right() + cos * local.forward()
        };
    }

    private static double fraction(int index, int count, boolean closed) {
        if (closed) {
            return (double) index / count;
        }
        return count == 1 ? 0.5 : (double) index / (count - 1);
    }

    private static Vec velocity(Movement movement, Vec outward, Vec spin) {
        Vec base = switch (movement.motion()) {
            case NONE -> null;
            case OUTWARD -> outward;
            case UP -> new Vec(0, 1, 0);
            case SPIN -> spin;
        };
        return base == null ? STILL : new Vec(base.right(), base.up() + movement.lift(), base.forward());
    }

    private static double lerp(double a, double b, double t) {
        return a + (b - a) * t;
    }
}
