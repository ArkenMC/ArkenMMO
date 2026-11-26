package dev.casperrs.arkenMMO.skill;

import java.util.List;

/**
 * The buyable places of an archetype; every archetype has this shape. Keystones and the ultimate are
 * sealed in this release, so they aren't listed. None of these needs points spent in the archetype.
 */
public enum SkillNode {
    N1(1, 1, true),
    N2(1, 1, false),
    N3(1, 1, false),
    N4(2, 8, true),
    N5(1, 8, false),
    N6(2, 8, true);

    private final int cost;
    private final int requiredLevel;
    private final boolean active;

    SkillNode(int cost, int requiredLevel, boolean active) {
        this.cost = cost;
        this.requiredLevel = requiredLevel;
        this.active = active;
    }

    public int cost() {
        return cost;
    }

    public int requiredLevel() {
        return requiredLevel;
    }

    public boolean active() {
        return active;
    }

    /** Owning any one of these allows buying this node; empty for the entry node. */
    public List<SkillNode> links() {
        return switch (this) {
            case N1 -> List.of();
            case N2, N3 -> List.of(N1);
            case N4 -> List.of(N2, N5);
            case N5 -> List.of(N4, N6);
            case N6 -> List.of(N3, N5);
        };
    }
}
