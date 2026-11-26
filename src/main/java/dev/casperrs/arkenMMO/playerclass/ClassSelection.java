package dev.casperrs.arkenMMO.playerclass;

import dev.casperrs.arkenMMO.text.Messages;
import java.util.Optional;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.entity.Player;

/** The rules of choosing a class: only a player without one may pick. Main thread only. */
public final class ClassSelection {

    private final ClassStorage storage;
    private final Messages messages;
    private final ClassMenus menus;

    public ClassSelection(ClassStorage storage, Messages messages) {
        this.storage = storage;
        this.messages = messages;
        this.menus = new ClassMenus(messages, this::checkEligible, this::choose);
    }

    /**
     * Opens the selection menu. Returns the player's class if they already have one; then nothing happens.
     * ItemsAdder applies the resource pack before join and kicks players without it, so the art is loaded.
     */
    public Optional<PlayerClass> request(Player player) {
        Optional<PlayerClass> current = storage.get(player);
        if (current.isEmpty()) {
            menus.openFirstPage(player);
        }
        return current;
    }

    /** Removes the player's class and returns it; empty if they had none. */
    public Optional<PlayerClass> reset(Player player) {
        Optional<PlayerClass> current = storage.get(player);
        if (current.isPresent()) {
            storage.clear(player);
        }
        return current;
    }

    /** The {@code <class>} placeholder, filled with the configured class name. */
    public TagResolver classPlaceholder(PlayerClass playerClass) {
        return Placeholder.component("class", messages.get("classes." + playerClass.id() + ".name"));
    }

    private boolean checkEligible(Player player) {
        Optional<PlayerClass> current = storage.get(player);
        current.ifPresent(playerClass -> {
            player.closeInventory();
            messages.send(player, "class.current", classPlaceholder(playerClass));
        });
        return current.isEmpty();
    }

    private void choose(Player player, PlayerClass playerClass) {
        storage.set(player, playerClass);
        player.closeInventory();
        messages.send(player, "class.chosen", classPlaceholder(playerClass));
    }
}
