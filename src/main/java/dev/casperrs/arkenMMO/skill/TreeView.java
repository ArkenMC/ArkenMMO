package dev.casperrs.arkenMMO.skill;

import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

/** The two halves of a tree page and their slots, which must match the art painted into the titles. */
enum TreeView {
    UPPER(Map.of(SkillNode.N1, 4, SkillNode.N2, 20, SkillNode.N3, 24,
            SkillNode.N4, 38, SkillNode.N5, 40, SkillNode.N6, 42),
            List.of(new Link(SkillNode.N1, SkillNode.N2, new Piece(2, "corner_es"), new Piece(3, "h"),
                            new Piece(11, "v")),
                    new Link(SkillNode.N1, SkillNode.N3, new Piece(5, "h"), new Piece(6, "corner_sw"),
                            new Piece(15, "v")),
                    new Link(SkillNode.N2, SkillNode.N4, new Piece(29, "v")),
                    new Link(SkillNode.N3, SkillNode.N6, new Piece(33, "v")),
                    new Link(SkillNode.N4, SkillNode.N5, new Piece(39, "h")),
                    new Link(SkillNode.N5, SkillNode.N6, new Piece(41, "h"))),
            List.of()),
    LOWER(Map.of(SkillNode.N4, 2, SkillNode.N5, 4, SkillNode.N6, 6),
            List.of(new Link(SkillNode.N4, SkillNode.N5, new Piece(3, "h")),
                    new Link(SkillNode.N5, SkillNode.N6, new Piece(5, "h"))),
            // Both keystones and the ultimate
            List.of(20, 24, 40));

    /** One connector item. */
    record Piece(int slot, String shape) {
    }

    /** A connection, lit once both ends are owned. */
    record Link(SkillNode from, SkillNode to, List<Piece> pieces) {

        Link(SkillNode from, SkillNode to, Piece... pieces) {
            this(from, to, List.of(pieces));
        }
    }

    private final Map<SkillNode, Integer> nodeSlots;
    private final List<Link> links;
    private final List<Integer> sealedSlots;

    TreeView(Map<SkillNode, Integer> nodeSlots, List<Link> links, List<Integer> sealedSlots) {
        this.nodeSlots = nodeSlots;
        this.links = links;
        this.sealedSlots = sealedSlots;
    }

    Map<SkillNode, Integer> nodeSlots() {
        return nodeSlots;
    }

    List<Link> links() {
        return links;
    }

    List<Integer> sealedSlots() {
        return sealedSlots;
    }

    /**
     * The end of the title key. The lower view has no slot above its first row, so the paths coming
     * from the upper view are painted into the title, lit when both their ends are owned.
     */
    String titleSuffix(Predicate<SkillNode> owned) {
        if (this == UPPER) {
            return "a";
        }
        boolean left = owned.test(SkillNode.N2) && owned.test(SkillNode.N4);
        boolean right = owned.test(SkillNode.N3) && owned.test(SkillNode.N6);
        if (left && right) {
            return "b_both";
        }
        if (left) {
            return "b_left";
        }
        return right ? "b_right" : "b";
    }
}
