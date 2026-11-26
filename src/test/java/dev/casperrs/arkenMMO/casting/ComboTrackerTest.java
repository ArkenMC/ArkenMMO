package dev.casperrs.arkenMMO.casting;

import static dev.casperrs.arkenMMO.casting.Click.LEFT;
import static dev.casperrs.arkenMMO.casting.Click.RIGHT;
import static dev.casperrs.arkenMMO.casting.ComboTracker.Status.COMPLETED;
import static dev.casperrs.arkenMMO.casting.ComboTracker.Status.HELD_REPEAT;
import static dev.casperrs.arkenMMO.casting.ComboTracker.Status.NOT_STARTED;
import static dev.casperrs.arkenMMO.casting.ComboTracker.Status.PROGRESS;
import static dev.casperrs.arkenMMO.casting.ComboTracker.Status.SAME_TICK;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class ComboTrackerTest {

    private final ComboTracker tracker = new ComboTracker();

    /** A click at a real time, on the tick that time falls in. */
    private ComboTracker.Result at(long millis, Click click) {
        return tracker.click(click, false, millis / 50, millis);
    }

    private ComboTracker.Result mirroredAt(long millis, Click click) {
        return tracker.click(click, true, millis / 50, millis);
    }

    @Test
    void completesTheFourSlots() {
        assertSlot(1, 0, false, RIGHT, LEFT, RIGHT);
        assertSlot(2, 5000, false, RIGHT, RIGHT, RIGHT);
        assertSlot(3, 10000, false, RIGHT, LEFT, LEFT);
        assertSlot(4, 15000, false, RIGHT, RIGHT, LEFT);
    }

    @Test
    void mirrorsTheSlotsForArcher() {
        assertSlot(1, 0, true, LEFT, RIGHT, LEFT);
        assertSlot(2, 5000, true, LEFT, LEFT, LEFT);
        assertSlot(3, 10000, true, LEFT, RIGHT, RIGHT);
        assertSlot(4, 15000, true, LEFT, LEFT, RIGHT);
    }

    private void assertSlot(int slot, long start, boolean mirrored, Click... clicks) {
        ComboTracker.Result result = null;
        for (int i = 0; i < clicks.length; i++) {
            long millis = start + i * 400L;
            result = tracker.click(clicks[i], mirrored, millis / 50, millis);
        }
        assertEquals(COMPLETED, result.status());
        assertEquals(slot, result.slot());
        assertEquals(List.of(clicks), result.clicks());
    }

    @Test
    void onlyTheOpeningClickStartsACombo() {
        assertEquals(NOT_STARTED, at(0, LEFT).status());
        assertEquals(NOT_STARTED, mirroredAt(400, RIGHT).status());
        assertEquals(List.of(RIGHT), at(800, RIGHT).clicks());
    }

    @Test
    void allowsExactlyOneSecondBetweenClicks() {
        at(0, RIGHT);
        at(1000, LEFT);
        assertEquals(COMPLETED, at(2000, RIGHT).status());
    }

    @Test
    void startsOverAfterMoreThanOneSecond() {
        at(0, RIGHT);
        assertEquals(NOT_STARTED, at(1001, LEFT).status());
        assertEquals(List.of(RIGHT), at(1500, RIGHT).clicks());
        assertEquals(List.of(RIGHT), at(2600, RIGHT).clicks());
    }

    @Test
    void takesOneClickPerTick() {
        assertEquals(PROGRESS, tracker.click(RIGHT, false, 1, 0).status());
        assertEquals(SAME_TICK, tracker.click(LEFT, false, 1, 10).status());
        assertEquals(List.of(RIGHT, LEFT), tracker.click(LEFT, false, 9, 400).clicks());
    }

    @Test
    void ignoredTickDropsTheClickAndKeepsTheCombo() {
        at(0, RIGHT);
        tracker.ignoreTick(8);
        assertEquals(SAME_TICK, at(400, LEFT).status());
        assertEquals(List.of(RIGHT, RIGHT), at(800, RIGHT).clicks());
    }

    @Test
    void heldRightButtonCountsOnce() {
        assertEquals(PROGRESS, at(0, RIGHT).status());
        for (long millis = 200; millis <= 2000; millis += 200) {
            assertEquals(HELD_REPEAT, at(millis, RIGHT).status());
        }
        assertEquals(PROGRESS, at(2400, RIGHT).status());
    }

    @Test
    void aLeftClickBetweenTwoRightClicksIsNotAHold() {
        at(0, RIGHT);
        at(100, LEFT);
        assertEquals(COMPLETED, at(200, RIGHT).status());
    }

    @Test
    void fastLeftClicksAllCount() {
        mirroredAt(0, LEFT);
        mirroredAt(100, LEFT);
        assertEquals(2, mirroredAt(200, LEFT).slot());
    }

    @Test
    void resetForgetsTheCombo() {
        at(0, RIGHT);
        tracker.reset();
        assertEquals(NOT_STARTED, at(400, LEFT).status());
    }
}
