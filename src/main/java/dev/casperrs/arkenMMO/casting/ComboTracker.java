package dev.casperrs.arkenMMO.casting;

import java.util.ArrayList;
import java.util.List;
import org.jetbrains.annotations.Nullable;

/** One player's 3-click combo. One mouse press can raise several server events, so each tick gives one click at most. */
final class ComboTracker {

    static final int LENGTH = 3;
    static final long TIMEOUT_MILLIS = 1000;
    // A held right button repeats every 4 ticks (200 ms); the rest is slack for uneven packet arrival.
    static final long HELD_REPEAT_MILLIS = 250;

    enum Status {
        PROGRESS,
        COMPLETED,
        /** Not the opening click, and no combo is running. */
        NOT_STARTED,
        /** The tick already gave a click, or was claimed by {@link #ignoreTick}. */
        SAME_TICK,
        HELD_REPEAT
    }

    /** {@code clicks} is filled for PROGRESS and COMPLETED; {@code slot} is 1-4 for COMPLETED, else 0. */
    record Result(Status status, List<Click> clicks, int slot) {

        private static Result of(Status status) {
            return new Result(status, List.of(), 0);
        }
    }

    private final List<Click> clicks = new ArrayList<>(LENGTH);
    private long usedTick = Long.MIN_VALUE;
    private long comboMillis;
    private @Nullable Click lastPress;
    private long lastPressMillis;

    /** Claims the tick for something that isn't a combo click, such as opening a door or dropping an item. */
    void ignoreTick(long tick) {
        usedTick = tick;
    }

    /** A mirrored combo (Archer) opens with a left click, any other with a right click. */
    Result click(Click click, boolean mirrored, long tick, long nowMillis) {
        if (tick == usedTick) {
            return Result.of(Status.SAME_TICK);
        }
        usedTick = tick;

        boolean heldRepeat = click == Click.RIGHT && lastPress == Click.RIGHT
                && nowMillis - lastPressMillis <= HELD_REPEAT_MILLIS;
        lastPress = click;
        lastPressMillis = nowMillis;
        if (heldRepeat) {
            return Result.of(Status.HELD_REPEAT);
        }

        if (!clicks.isEmpty() && nowMillis - comboMillis > TIMEOUT_MILLIS) {
            clicks.clear();
        }
        Click opener = mirrored ? Click.LEFT : Click.RIGHT;
        boolean counts = !clicks.isEmpty() || click == opener;
        if (!counts) {
            return Result.of(Status.NOT_STARTED);
        }

        clicks.add(click);
        comboMillis = nowMillis;
        if (clicks.size() < LENGTH) {
            return new Result(Status.PROGRESS, List.copyOf(clicks), 0);
        }
        Result completed = new Result(Status.COMPLETED, List.copyOf(clicks), slotOf(opener));
        clicks.clear();
        return completed;
    }

    /** Forgets the running combo, keeping the tick claim. */
    void reset() {
        clicks.clear();
        lastPress = null;
    }

    // With O the opening button and X the other one: 1 = O-X-O, 2 = O-O-O, 3 = O-X-X, 4 = O-O-X.
    private int slotOf(Click opener) {
        boolean secondOpens = clicks.get(1) == opener;
        boolean thirdOpens = clicks.get(2) == opener;
        if (secondOpens) {
            return thirdOpens ? 2 : 4;
        }
        return thirdOpens ? 1 : 3;
    }
}
