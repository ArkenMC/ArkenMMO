package dev.casperrs.arkenMMO.playerclass;

import dev.casperrs.arkenMMO.pack.ResourcePackService;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.Optional;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.entity.Player;

/** The rules of choosing a class: only a player without one may pick. Main thread only. */
public final class ClassSelection {

    private final ClassStorage storage;
    private final ResourcePackService resourcePack;
    private final Messages messages;
    private final ClassMenus menus;

    public ClassSelection(ClassStorage storage, ResourcePackService resourcePack, Messages messages) {
        this.storage = storage;
        this.resourcePack = resourcePack;
        this.messages = messages;
        this.menus = new ClassMenus(messages, this::checkEligible, this::choose);
    }

    /**
     * Opens the selection menu, or queues it until the player's resource pack has loaded.
     * Returns the player's class if they already have one; then nothing happens.
     */
    public Optional<PlayerClass> request(Player player) {
        Optional<PlayerClass> current = storage.get(player);
        if (current.isEmpty()) {
            boolean opened = resourcePack.whenReady(player, () -> {
                if (storage.get(player).isEmpty()) {
                    menus.openFirstPage(player);
                }
            });
            if (!opened) {
                messages.send(player, "class.waiting-for-pack");
            }
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
