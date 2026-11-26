package dev.casperrs.arkenMMO.menu;

import java.util.function.Consumer;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.InventoryView;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.Nullable;

/** Locks every item while a {@link Menu} is open and runs its button actions. */
public final class MenuListener implements Listener {

    private final Plugin plugin;

    public MenuListener(Plugin plugin) {
        this.plugin = plugin;
    }

    /** Needed on disable: without this listener the menu items could be taken out. */
    public static void closeAll() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            if (menuOf(player.getOpenInventory()) != null) {
                player.closeInventory();
            }
        }
    }

    // HIGHEST so that no earlier handler can un-cancel
    @EventHandler(priority = EventPriority.HIGHEST)
    public void onClick(InventoryClickEvent event) {
        Menu menu = menuOf(event.getView());
        if (menu == null) {
            return;
        }
        event.setCancelled(true);
        if (!isPlainClick(event.getClick()) || !(event.getWhoClicked() instanceof Player player)) {
            return;
        }
        Consumer<Player> action = menu.actionAt(event.getRawSlot());
        if (action == null) {
            return;
        }
        // Inventories must not be opened or closed inside the click event. The view check also drops
        // further clicks from the same tick once the first one has changed the screen.
        Bukkit.getScheduler().runTask(plugin, () -> {
            if (player.isOnline() && menu.isViewedBy(player)) {
                action.accept(player);
            }
        });
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onDrag(InventoryDragEvent event) {
        if (menuOf(event.getView()) != null) {
            event.setCancelled(true);
        }
    }

    private static @Nullable Menu menuOf(InventoryView view) {
        return view.getTopInventory().getHolder(false) instanceof Menu menu ? menu : null;
    }

    private static boolean isPlainClick(ClickType click) {
        return switch (click) {
            case LEFT, RIGHT, SHIFT_LEFT, SHIFT_RIGHT -> true;
            default -> false;
        };
    }
}
