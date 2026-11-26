package dev.casperrs.arkenMMO.menu;

import java.util.function.Consumer;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.jetbrains.annotations.Nullable;

/** A six-row chest menu: read-only slots, some of which run an action when clicked. */
public final class Menu implements InventoryHolder {

    private static final int COLUMNS = 9;
    private static final int ROWS = 6;

    private final Inventory inventory;
    private final Consumer<Player>[] actions;

    @SuppressWarnings("unchecked")
    public Menu(Component title) {
        this.inventory = Bukkit.createInventory(this, COLUMNS * ROWS, title);
        this.actions = (Consumer<Player>[]) new Consumer<?>[COLUMNS * ROWS];
    }

    /** Fills a rectangle of slots (zero-based, bounds inclusive) so that it acts as one button. */
    public Menu button(int firstColumn, int lastColumn, int firstRow, int lastRow,
                       ItemStack icon, Consumer<Player> action) {
        for (int row = firstRow; row <= lastRow; row++) {
            for (int column = firstColumn; column <= lastColumn; column++) {
                int slot = row * COLUMNS + column;
                inventory.setItem(slot, icon);
                actions[slot] = action;
            }
        }
        return this;
    }

    public void open(Player player) {
        player.openInventory(inventory);
    }

    /** The action for a raw slot of the view, or {@code null} for anything that does nothing. */
    @Nullable Consumer<Player> actionAt(int rawSlot) {
        return rawSlot >= 0 && rawSlot < actions.length ? actions[rawSlot] : null;
    }

    boolean isViewedBy(Player player) {
        return player.getOpenInventory().getTopInventory().getHolder(false) == this;
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
