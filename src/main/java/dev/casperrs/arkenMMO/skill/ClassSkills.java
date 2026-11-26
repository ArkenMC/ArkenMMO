package dev.casperrs.arkenMMO.skill;

import java.util.HashSet;
import java.util.Set;

/**
 * What a player has stored for one class: bought skill IDs, the combo slots and the time
 * (epoch milliseconds, 0 for never reset) from which the tree may be reset again.
 */
public record ClassSkills(Set<String> owned, Loadout loadout, long resetReadyAt) {

    public ClassSkills {
        owned = Set.copyOf(owned);
    }

    public static ClassSkills starting(ClassTree tree) {
        return new ClassSkills(Set.of(), Loadout.starting(tree.core().id()), 0);
    }

    /** A new active takes the first free combo slot. */
    public ClassSkills with(Skill skill) {
        Set<String> changed = new HashSet<>(owned);
        changed.add(skill.id());
        return new ClassSkills(changed, skill.active() ? loadout.fill(skill.id()) : loadout, resetReadyAt);
    }

    public ClassSkills without(ClassTree tree, Skill skill) {
        Set<String> changed = new HashSet<>(owned);
        changed.remove(skill.id());
        return withOwned(tree, changed, resetReadyAt);
    }

    /** Skills that are no longer owned leave their combo slots. */
    public ClassSkills withOwned(ClassTree tree, Set<String> changed, long readyAt) {
        return new ClassSkills(changed,
                loadout.retain(id -> id.equals(tree.core().id()) || changed.contains(id)), readyAt);
    }

    public ClassSkills with(Loadout changed) {
        return new ClassSkills(owned, changed, resetReadyAt);
    }
}
