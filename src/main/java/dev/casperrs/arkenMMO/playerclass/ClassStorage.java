package dev.casperrs.arkenMMO.playerclass;

import java.util.Optional;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.Player;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.Plugin;

/**
 * Each player's chosen class, kept in the player's persistent data, which the server saves with the player.
 * Main thread only. Only the choice is stored here, so later per-class data can be keyed by class ID.
 */
public final class ClassStorage {

    private final NamespacedKey classKey;

    public ClassStorage(Plugin plugin) {
        this.classKey = new NamespacedKey(plugin, "class");
    }

    public Optional<PlayerClass> get(Player player) {
        String id = player.getPersistentDataContainer().get(classKey, PersistentDataType.STRING);
        return id == null ? Optional.empty() : PlayerClass.byId(id);
    }

    public void set(Player player, PlayerClass playerClass) {
        player.getPersistentDataContainer().set(classKey, PersistentDataType.STRING, playerClass.id());
    }

    public void clear(Player player) {
        player.getPersistentDataContainer().remove(classKey);
    }
}
