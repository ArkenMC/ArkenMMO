package dev.casperrs.arkenMMO.skill;

import java.util.EnumSet;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

/**
 * Buying rules. {@code owned} holds the IDs of bought skills; the core skill is always owned and is
 * never part of it. {@code points} is the total a player has, spent or not.
 */
public final class TreeRules {

    /** What can stand in the way of buying a skill. */
    public enum Gate {
        LEVEL, CONNECTION, POINTS
    }

    private TreeRules() {
    }

    public static boolean owns(ClassTree tree, Set<String> owned, Skill skill) {
        return skill.equals(tree.core()) || owned.contains(skill.id());
    }

    /** IDs that aren't bought skills of this tree cost nothing. */
    public static int spent(ClassTree tree, Set<String> owned) {
        return tree.archetypes().stream().mapToInt(archetype -> spent(archetype, owned)).sum();
    }

    public static int spent(ClassTree.Archetype archetype, Set<String> owned) {
        return archetype.skills().stream()
                .filter(skill -> owned.contains(skill.id()))
                .mapToInt(skill -> skill.node().cost())
                .sum();
    }

    /** Every unmet gate of a skill that isn't owned yet. */
    public static Set<Gate> missing(ClassTree tree, Set<String> owned, Skill skill, int level, int points) {
        SkillNode node = skill.node();
        Set<Gate> missing = EnumSet.noneOf(Gate.class);
        if (level < node.requiredLevel()) {
            missing.add(Gate.LEVEL);
        }
        if (!connected(tree.archetypeOf(skill), owned, node)) {
            missing.add(Gate.CONNECTION);
        }
        if (points - spent(tree, owned) < node.cost()) {
            missing.add(Gate.POINTS);
        }
        return missing;
    }

    public static boolean canBuy(ClassTree tree, Set<String> owned, Skill skill, int level, int points) {
        return !owns(tree, owned, skill) && missing(tree, owned, skill, level, points).isEmpty();
    }

    /** Whether these skills could have been bought one after another with this level and these points. */
    public static boolean isValid(ClassTree tree, Set<String> owned, int level, int points) {
        return spent(tree, owned) <= points && reachable(tree, owned, level, points).size() == owned.size();
    }

    public static boolean canRemove(ClassTree tree, Set<String> owned, Skill skill, int level, int points) {
        return owned.contains(skill.id()) && isValid(tree, without(owned, skill), level, points);
    }

    /**
     * For a skill that can't be removed: a skill depending on it that can be removed now. Removing
     * these one at a time frees the skill in the end.
     */
    public static Optional<Skill> blocking(ClassTree tree, Set<String> owned, Skill skill, int level, int points) {
        Set<String> remaining = without(owned, skill);
        Set<String> stillReached = reachable(tree, remaining, level, points);
        return remaining.stream()
                .filter(id -> !stillReached.contains(id))
                .sorted()
                .flatMap(id -> tree.find(id).stream())
                .filter(dependent -> canRemove(tree, owned, dependent, level, points))
                .findFirst();
    }

    private static Set<String> without(Set<String> owned, Skill skill) {
        Set<String> remaining = new HashSet<>(owned);
        remaining.remove(skill.id());
        return remaining;
    }

    // Grown from the entry nodes, so that linked nodes can't hold each other up
    private static Set<String> reachable(ClassTree tree, Set<String> owned, int level, int points) {
        Set<String> reached = new HashSet<>();
        boolean grew = true;
        while (grew) {
            grew = false;
            for (String id : owned) {
                Optional<Skill> skill = tree.find(id).filter(found -> !found.isCore());
                if (skill.isPresent() && !reached.contains(id)
                        && canBuy(tree, reached, skill.get(), level, points)) {
                    reached.add(id);
                    grew = true;
                }
            }
        }
        return reached;
    }

    private static boolean connected(ClassTree.Archetype archetype, Set<String> owned, SkillNode node) {
        return node.links().isEmpty()
                || node.links().stream().anyMatch(link -> owned.contains(archetype.at(link).id()));
    }
}
