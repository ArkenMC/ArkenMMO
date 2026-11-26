package dev.casperrs.arkenMMO.skill;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.Arrays;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class TreeRulesTest {

    private static final int LEVEL = 30;
    private static final int POINTS = 18;

    private final ClassTree tree = SkillCatalog.of(PlayerClass.WARRIOR);
    private final ClassTree.Archetype guardian = tree.archetypes().getFirst();

    private Skill skill(SkillNode node) {
        return guardian.at(node);
    }

    private Set<String> owned(SkillNode... nodes) {
        return Arrays.stream(nodes).map(node -> skill(node).id()).collect(Collectors.toSet());
    }

    private Set<TreeRules.Gate> missing(Set<String> owned, SkillNode node) {
        return TreeRules.missing(tree, owned, skill(node), LEVEL, POINTS);
    }

    private boolean canBuy(Set<String> owned, SkillNode node) {
        return TreeRules.canBuy(tree, owned, skill(node), LEVEL, POINTS);
    }

    @Test
    void onlyTheEntryNodeIsOpenAtTheStart() {
        for (SkillNode node : SkillNode.values()) {
            assertEquals(node == SkillNode.N1 ? Set.of() : Set.of(TreeRules.Gate.CONNECTION),
                    missing(Set.of(), node), node.name());
        }
        assertFalse(TreeRules.canBuy(tree, Set.of(), tree.core(), LEVEL, POINTS));
        assertFalse(canBuy(owned(SkillNode.N1), SkillNode.N1));
    }

    @Test
    void anyOneLinkOpensANodeAndTheBridgeWorksBothWays() {
        assertFalse(canBuy(owned(SkillNode.N1, SkillNode.N3), SkillNode.N4));
        assertFalse(canBuy(owned(SkillNode.N1, SkillNode.N3), SkillNode.N5));
        assertTrue(canBuy(owned(SkillNode.N1, SkillNode.N2), SkillNode.N4));
        assertTrue(canBuy(owned(SkillNode.N1, SkillNode.N3, SkillNode.N6, SkillNode.N5), SkillNode.N4));
    }

    @Test
    void linksStayInsideOneArchetype() {
        Skill otherN2 = tree.archetypes().get(1).at(SkillNode.N2);
        assertFalse(TreeRules.canBuy(tree, owned(SkillNode.N1), otherN2, LEVEL, POINTS));
    }

    @Test
    void everyUnmetGateIsNamedAndPointsCountAcrossArchetypes() {
        Set<String> owned = owned(SkillNode.N1, SkillNode.N2);
        assertEquals(Set.of(TreeRules.Gate.LEVEL), TreeRules.missing(tree, owned, skill(SkillNode.N4), 7, POINTS));
        assertEquals(Set.of(), TreeRules.missing(tree, owned, skill(SkillNode.N4), 8, 4));
        assertEquals(Set.of(TreeRules.Gate.POINTS), TreeRules.missing(tree, owned, skill(SkillNode.N4), 8, 3));
        assertEquals(Set.of(TreeRules.Gate.values()),
                TreeRules.missing(tree, Set.of(), skill(SkillNode.N6), 1, 0));
        Skill otherEntry = tree.archetypes().get(2).at(SkillNode.N1);
        assertFalse(TreeRules.canBuy(tree, owned, otherEntry, LEVEL, 2));
    }

    @Test
    void linkedNodesCannotHoldEachOtherUp() {
        assertFalse(TreeRules.isValid(tree, owned(SkillNode.N1, SkillNode.N4, SkillNode.N5), LEVEL, POINTS));
        assertFalse(TreeRules.isValid(tree,
                owned(SkillNode.N1, SkillNode.N4, SkillNode.N5, SkillNode.N6), LEVEL, POINTS));
    }

    @Test
    void savedTreesThatNoLongerFitAreInvalid() {
        Set<String> full = owned(SkillNode.values());
        assertTrue(TreeRules.isValid(tree, full, LEVEL, 8));
        assertFalse(TreeRules.isValid(tree, full, LEVEL, 7));
        assertFalse(TreeRules.isValid(tree, full, 7, POINTS));
        assertFalse(TreeRules.isValid(tree, Set.of("warrior.removed_skill"), LEVEL, POINTS));
        assertFalse(TreeRules.isValid(tree, Set.of(tree.core().id()), LEVEL, POINTS));
        assertFalse(TreeRules.isValid(SkillCatalog.of(PlayerClass.MAGE), full, LEVEL, POINTS));
    }

    @Test
    void undoOnlyWhileEveryOtherSkillStaysConnected() {
        Set<String> line = owned(SkillNode.N1, SkillNode.N2, SkillNode.N4, SkillNode.N5);
        assertFalse(canRemove(line, SkillNode.N1));
        assertFalse(canRemove(line, SkillNode.N2));
        assertFalse(canRemove(line, SkillNode.N4));
        assertTrue(canRemove(line, SkillNode.N5));
        assertFalse(canRemove(line, SkillNode.N3));

        // With the other side owned too, n4 is still reached over n6 and n5
        Set<String> full = owned(SkillNode.values());
        assertTrue(canRemove(full, SkillNode.N2));
        assertTrue(canRemove(full, SkillNode.N3));
        assertTrue(canRemove(full, SkillNode.N5));
        assertFalse(canRemove(full, SkillNode.N1));
    }

    @Test
    void aRefusedUndoNamesASkillThatCanBeUndoneFirst() {
        Set<String> line = owned(SkillNode.N1, SkillNode.N2, SkillNode.N4, SkillNode.N5);
        for (SkillNode node : new SkillNode[] {SkillNode.N1, SkillNode.N2, SkillNode.N4}) {
            assertEquals(Optional.of(skill(SkillNode.N5)),
                    TreeRules.blocking(tree, line, skill(node), LEVEL, POINTS), node.name());
        }
        assertEquals(Optional.empty(), TreeRules.blocking(tree, line, skill(SkillNode.N5), LEVEL, POINTS));
    }

    private boolean canRemove(Set<String> owned, SkillNode node) {
        return TreeRules.canRemove(tree, owned, skill(node), LEVEL, POINTS);
    }
}
