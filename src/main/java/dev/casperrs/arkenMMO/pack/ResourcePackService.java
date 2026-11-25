package dev.casperrs.arkenMMO.pack;

import dev.casperrs.arkenMMO.text.Messages;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.kyori.adventure.resource.ResourcePackInfo;
import net.kyori.adventure.resource.ResourcePackRequest;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.player.PlayerResourcePackStatusEvent;
import org.jetbrains.annotations.Nullable;

/**
 * Sends the required resource pack and holds back actions until the client has loaded it.
 * Main thread only. Without settings nothing is sent and every action runs at once.
 */
public final class ResourcePackService implements Listener {

    private final Messages messages;
    private final @Nullable UUID packId;
    private final @Nullable ResourcePackRequest request;

    private final Set<UUID> loading = new HashSet<>();
    private final Set<UUID> loaded = new HashSet<>();
    private final Map<UUID, Runnable> waiting = new HashMap<>();

    public ResourcePackService(Messages messages, @Nullable ResourcePackSettings settings) {
        this.messages = messages;
        if (settings == null) {
            this.packId = null;
            this.request = null;
            return;
        }
        this.packId = settings.id();
        this.request = ResourcePackRequest.resourcePackRequest()
                .packs(ResourcePackInfo.resourcePackInfo(settings.id(), settings.url(), settings.sha1()))
                .required(true)
                .replace(false)
                .prompt(messages.get("resource-pack.prompt"))
                .build();
    }

    /**
     * Runs {@code action} now if no pack is needed or it has loaded, otherwise once it has loaded.
     * A newer waiting action replaces the older one; a failed load or a disconnect drops it.
     * A player whose pack failed earlier gets it sent again. Returns false if the action has to wait.
     */
    public boolean whenReady(Player player, Runnable action) {
        UUID playerId = player.getUniqueId();
        if (request == null || loaded.contains(playerId)) {
            action.run();
            return true;
        }
        waiting.put(playerId, action);
        send(player);
        return false;
    }

    private void send(Player player) {
        if (request != null && loading.add(player.getUniqueId())) {
            player.sendResourcePacks(request);
        }
    }

    // LOWEST so that another plugin's join handler can already request a menu without a second send
    @EventHandler(priority = EventPriority.LOWEST)
    public void onJoin(PlayerJoinEvent event) {
        send(event.getPlayer());
    }

    @EventHandler
    public void onStatus(PlayerResourcePackStatusEvent event) {
        if (!event.getID().equals(packId)) {
            return;
        }
        Player player = event.getPlayer();
        UUID playerId = player.getUniqueId();
        switch (event.getStatus()) {
            case ACCEPTED, DOWNLOADED -> {
                // Still on its way
            }
            case SUCCESSFULLY_LOADED -> {
                loading.remove(playerId);
                loaded.add(playerId);
                Runnable action = waiting.remove(playerId);
                if (action != null) {
                    action.run();
                }
            }
            case DECLINED, FAILED_DOWNLOAD, FAILED_RELOAD, INVALID_URL, DISCARDED -> {
                loading.remove(playerId);
                loaded.remove(playerId);
                if (waiting.remove(playerId) != null) {
                    messages.send(player, "resource-pack.failed");
                }
            }
        }
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent event) {
        UUID playerId = event.getPlayer().getUniqueId();
        loading.remove(playerId);
        loaded.remove(playerId);
        waiting.remove(playerId);
    }
}
