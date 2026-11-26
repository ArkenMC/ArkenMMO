package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.Optional;
import org.bukkit.entity.Player;

/** Opens the skill tree of a player's class. Main thread only. */
public final class SkillMenus {

    private final ClassStorage classes;
    private final Messages messages;
    private final TreeScreen tree;

    public SkillMenus(SkillBook book, SkillValues values, ClassStorage classes, Messages messages) {
        this.classes = classes;
        this.messages = messages;
        SkillContext context = new SkillContext(book, new SkillItems(messages, values), messages, classes);
        LoadoutScreen loadout = new LoadoutScreen(context, this::showTree);
        this.tree = new TreeScreen(context, loadout::open);
    }

    /** Opens the tree of the player's class; players without a class are told. */
    public void request(Player player) {
        Optional<PlayerClass> current = classes.get(player);
        if (current.isEmpty()) {
            messages.send(player, "skills.chat.no-class");
            return;
        }
        showTree(player, new SkillSession(SkillCatalog.of(current.get())));
    }

    private void showTree(Player player, SkillSession session) {
        tree.open(player, session);
    }
}
