package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.Player;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.Nullable;

/**
 * Skills in the player's persistent data, which the server saves with the player. Main thread only.
 * There is one container per class, so later per-class values (XP, level, rebirths, evolution)
 * can be added beside these without moving anything.
 */
public final class SkillStorage {

    private final Plugin plugin;
    private final NamespacedKey rootKey;
    private final NamespacedKey ownedKey;
    private final NamespacedKey loadoutKey;
    private final NamespacedKey resetReadyKey;

    public SkillStorage(Plugin plugin) {
        this.plugin = plugin;
        this.rootKey = new NamespacedKey(plugin, "skills");
        this.ownedKey = new NamespacedKey(plugin, "owned");
        this.loadoutKey = new NamespacedKey(plugin, "loadout");
        this.resetReadyKey = new NamespacedKey(plugin, "reset_ready_at");
    }

    /** Empty if nothing was ever stored for this class. The content is not checked against any rules. */
    public Optional<ClassSkills> load(Player player, PlayerClass playerClass) {
        PersistentDataContainer root = child(player.getPersistentDataContainer(), rootKey);
        PersistentDataContainer stored = root == null ? null : child(root, classKey(playerClass));
        if (stored == null) {
            return Optional.empty();
        }
        return Optional.of(new ClassSkills(
                new HashSet<>(stored.getOrDefault(ownedKey, PersistentDataType.LIST.strings(), List.of())),
                new Loadout(stored.getOrDefault(loadoutKey, PersistentDataType.LIST.strings(), List.of())),
                stored.getOrDefault(resetReadyKey, PersistentDataType.LONG, 0L)));
    }

    public void save(Player player, PlayerClass playerClass, ClassSkills skills) {
        PersistentDataContainer data = player.getPersistentDataContainer();
        PersistentDataContainer root = childOrNew(data, rootKey, data);
        PersistentDataContainer stored = childOrNew(root, classKey(playerClass), data);
        stored.set(ownedKey, PersistentDataType.LIST.strings(), skills.owned().stream().sorted().toList());
        stored.set(loadoutKey, PersistentDataType.LIST.strings(), skills.loadout().seats());
        stored.set(resetReadyKey, PersistentDataType.LONG, skills.resetReadyAt());
        // A nested container has to be written back to its parent
        root.set(classKey(playerClass), PersistentDataType.TAG_CONTAINER, stored);
        data.set(rootKey, PersistentDataType.TAG_CONTAINER, root);
    }

    private NamespacedKey classKey(PlayerClass playerClass) {
        return new NamespacedKey(plugin, playerClass.id());
    }

    private static @Nullable PersistentDataContainer child(PersistentDataContainer parent, NamespacedKey key) {
        return parent.get(key, PersistentDataType.TAG_CONTAINER);
    }

    private static PersistentDataContainer childOrNew(
            PersistentDataContainer parent, NamespacedKey key, PersistentDataContainer context) {
        PersistentDataContainer existing = child(parent, key);
        return existing != null ? existing : context.getAdapterContext().newPersistentDataContainer();
    }
}
