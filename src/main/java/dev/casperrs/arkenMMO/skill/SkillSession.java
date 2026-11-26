package dev.casperrs.arkenMMO.skill;

import java.util.HashSet;
import java.util.Set;
import org.jetbrains.annotations.Nullable;

/**
 * One opening of the skill menus, shared by all their pages. Only the pages' buttons hold it, so it
 * ends when the player closes the menu.
 */
final class SkillSession {

    final ClassTree tree;
    /** IDs bought during this opening; only these can be undone. */
    final Set<String> boughtNow = new HashSet<>();
    int archetype;
    TreeView view = TreeView.UPPER;
    /** Clicked once; a second click buys it or, if it is owned, undoes it. */
    @Nullable Skill confirming;
    boolean confirmingReset;
    /** Picked in the loadout menu, to be put on a combo slot. */
    @Nullable Skill picked;

    SkillSession(ClassTree tree) {
        this.tree = tree;
    }

    ClassTree.Archetype archetype() {
        return tree.archetypes().get(archetype);
    }

    boolean hasSelection() {
        return confirming != null || confirmingReset || picked != null;
    }

    void clearSelection() {
        confirming = null;
        confirmingReset = false;
        picked = null;
    }
}
