package dev.casperrs.arkenMMO.skill;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.function.Predicate;

/** The skills on the combo slots, as IDs; {@link #EMPTY} marks a free slot. A skill sits on one slot at most. */
public record Loadout(List<String> seats) {

    public static final int SIZE = 4;
    public static final String EMPTY = "";

    /** Extra entries are dropped, missing ones are free, and a repeated skill keeps its first slot. */
    public Loadout {
        List<String> cleaned = new ArrayList<>(Collections.nCopies(SIZE, EMPTY));
        for (int seat = 0; seat < Math.min(SIZE, seats.size()); seat++) {
            if (!cleaned.contains(seats.get(seat))) {
                cleaned.set(seat, seats.get(seat));
            }
        }
        seats = List.copyOf(cleaned);
    }

    /** A new tree: the core skill on the first slot. */
    public static Loadout starting(String coreId) {
        return new Loadout(List.of(coreId));
    }

    public Optional<String> at(int seat) {
        return Optional.of(seats.get(seat)).filter(id -> !id.equals(EMPTY));
    }

    /** If the skill already has a slot, the two slots swap. */
    public Loadout assign(int seat, String skillId) {
        List<String> changed = new ArrayList<>(seats);
        int previous = changed.indexOf(skillId);
        if (previous >= 0) {
            changed.set(previous, changed.get(seat));
        }
        changed.set(seat, skillId);
        return new Loadout(changed);
    }

    public Loadout clear(int seat) {
        List<String> changed = new ArrayList<>(seats);
        changed.set(seat, EMPTY);
        return new Loadout(changed);
    }

    /** Puts a new skill on the first free slot, if there is one and it has no slot yet. */
    public Loadout fill(String skillId) {
        int free = seats.indexOf(EMPTY);
        return free < 0 || seats.contains(skillId) ? this : assign(free, skillId);
    }

    public Loadout retain(Predicate<String> keep) {
        return new Loadout(seats.stream().map(id -> id.equals(EMPTY) || keep.test(id) ? id : EMPTY).toList());
    }
}
