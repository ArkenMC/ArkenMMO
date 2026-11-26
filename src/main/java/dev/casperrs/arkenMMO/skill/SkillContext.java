package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.function.Consumer;
import org.bukkit.entity.Player;

/** What both skill screens work with. */
record SkillContext(SkillBook book, SkillItems items, Messages messages, ClassStorage classes) {

    /** Runs a click only while the player may use the menu and still has its class; otherwise it closes. */
    Consumer<Player> guarded(SkillSession session, Consumer<Player> action) {
        return player -> {
            if (!player.hasPermission(SkillsCommand.PERMISSION)) {
                player.closeInventory();
            } else if (classes.get(player).filter(session.tree.playerClass()::equals).isPresent()) {
                action.accept(player);
            } else {
                player.closeInventory();
                messages.send(player, "skills.chat.class-changed");
            }
        };
    }
}
