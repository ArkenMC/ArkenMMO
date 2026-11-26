package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.text.Messages;
import java.time.Duration;
import java.util.Optional;
import java.util.Set;
import org.bukkit.entity.Player;

/** Players' stored skills and every allowed change to them. Main thread only. */
public final class SkillBook {

    static final Duration RESET_COOLDOWN = Duration.ofSeconds(60);

    private final SkillStorage storage;
    private final SkillSettings settings;
    private final Messages messages;

    public SkillBook(SkillStorage storage, SkillSettings settings, Messages messages) {
        this.storage = storage;
        this.settings = settings;
        this.messages = messages;
    }

    public int level() {
        return settings.testLevel();
    }

    public int points() {
        return settings.testPoints();
    }

    public int freePoints(ClassTree tree, ClassSkills skills) {
        return points() - TreeRules.spent(tree, skills.owned());
    }

    /**
     * The player's skills for this tree. A saved tree that the rules no longer allow (renamed skills,
     * a lower level or fewer points) is emptied and saved, and the player is told.
     */
    public ClassSkills get(Player player, ClassTree tree) {
        Optional<ClassSkills> stored = storage.load(player, tree.playerClass());
        if (stored.isEmpty()) {
            return ClassSkills.starting(tree);
        }
        ClassSkills skills = stored.get();
        if (!TreeRules.isValid(tree, skills.owned(), level(), points())) {
            ClassSkills emptied = skills.withOwned(tree, Set.of(), skills.resetReadyAt());
            storage.save(player, tree.playerClass(), emptied);
            messages.send(player, "skills.chat.tree-invalid");
            return emptied;
        }
        // Also drops combo slot entries that aren't owned actives
        return skills.with(skills.loadout().retain(id -> tree.find(id)
                .filter(skill -> skill.active() && TreeRules.owns(tree, skills.owned(), skill))
                .isPresent()));
    }

    public Set<TreeRules.Gate> missing(ClassTree tree, ClassSkills skills, Skill skill) {
        return TreeRules.missing(tree, skills.owned(), skill, level(), points());
    }

    public boolean canBuy(ClassTree tree, ClassSkills skills, Skill skill) {
        return TreeRules.canBuy(tree, skills.owned(), skill, level(), points());
    }

    public boolean buy(Player player, ClassTree tree, Skill skill) {
        ClassSkills skills = get(player, tree);
        if (!canBuy(tree, skills, skill)) {
            return false;
        }
        storage.save(player, tree.playerClass(), skills.with(skill));
        return true;
    }

    public boolean canRefund(ClassTree tree, ClassSkills skills, Skill skill) {
        return TreeRules.canRemove(tree, skills.owned(), skill, level(), points());
    }

    /** The skill to undo first when {@code skill} can't be undone because others depend on it. */
    public Optional<Skill> blocking(ClassTree tree, ClassSkills skills, Skill skill) {
        return TreeRules.blocking(tree, skills.owned(), skill, level(), points());
    }

    /** Takes back one skill; whether it was bought recently enough is the caller's business. */
    public boolean refund(Player player, ClassTree tree, Skill skill) {
        ClassSkills skills = get(player, tree);
        if (!canRefund(tree, skills, skill)) {
            return false;
        }
        storage.save(player, tree.playerClass(), skills.without(tree, skill));
        return true;
    }

    /** Whole seconds until the tree may be reset again, rounded up; 0 when it may. */
    public long resetWaitSeconds(ClassSkills skills) {
        long millis = skills.resetReadyAt() - System.currentTimeMillis();
        // Capped in case the server clock was turned back
        return Math.clamp((millis + 999) / 1000, 0, RESET_COOLDOWN.toSeconds());
    }

    public boolean canReset(ClassSkills skills) {
        return !skills.owned().isEmpty() && resetWaitSeconds(skills) == 0;
    }

    public boolean reset(Player player, ClassTree tree) {
        ClassSkills skills = get(player, tree);
        if (!canReset(skills)) {
            return false;
        }
        long readyAt = System.currentTimeMillis() + RESET_COOLDOWN.toMillis();
        storage.save(player, tree.playerClass(), skills.withOwned(tree, Set.of(), readyAt));
        return true;
    }

    public void saveLoadout(Player player, ClassTree tree, Loadout loadout) {
        storage.save(player, tree.playerClass(), get(player, tree).with(loadout));
    }
}
