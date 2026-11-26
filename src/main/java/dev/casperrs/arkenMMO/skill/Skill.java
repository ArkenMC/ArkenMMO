package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import org.jetbrains.annotations.Nullable;

/**
 * One skill. {@code key} is its ID without the class prefix and names its art and text.
 * The core skill is always owned and has neither an {@code archetype} nor a {@code node}.
 */
public record Skill(PlayerClass playerClass, String key, @Nullable String archetype, @Nullable SkillNode node) {

    /** The stored ID, such as {@code warrior.shield_bash}. */
    public String id() {
        return playerClass.id() + "." + key;
    }

    public boolean isCore() {
        return node == null;
    }

    public boolean active() {
        return node == null || node.active();
    }
}
