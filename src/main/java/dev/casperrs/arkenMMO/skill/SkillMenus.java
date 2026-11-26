package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.pack.ResourcePackService;
import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.Optional;
import org.bukkit.entity.Player;

/** Opens the skill tree of a player's class. Main thread only. */
public final class SkillMenus {

    private final ClassStorage classes;
    private final ResourcePackService resourcePack;
    private final Messages messages;
    private final TreeScreen tree;

    public SkillMenus(SkillBook book, SkillValues values, ClassStorage classes, ResourcePackService resourcePack,
                      Messages messages) {
        this.classes = classes;
        this.resourcePack = resourcePack;
        this.messages = messages;
        SkillContext context = new SkillContext(book, new SkillItems(messages, values), messages, classes);
        LoadoutScreen loadout = new LoadoutScreen(context, this::showTree);
        this.tree = new TreeScreen(context, loadout::open);
    }

    /** Opens the tree now or once the player's resource pack has loaded; players without a class are told. */
    public void request(Player player) {
        if (classes.get(player).isEmpty()) {
            messages.send(player, "skills.chat.no-class");
            return;
        }
        boolean opened = resourcePack.whenReady(player, () -> {
            Optional<PlayerClass> current = classes.get(player);
            current.ifPresent(playerClass ->
                    showTree(player, new SkillSession(SkillCatalog.of(playerClass))));
        });
        if (!opened) {
            messages.send(player, "skills.chat.waiting-for-pack");
        }
    }

    private void showTree(Player player, SkillSession session) {
        tree.open(player, session);
    }
}
