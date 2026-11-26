package dev.casperrs.arkenMMO.menu;

import java.util.function.Consumer;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.jetbrains.annotations.Nullable;

/** A six-row chest menu: read-only slots, some of which run an action when clicked. Open menus can be changed. */
public final class Menu implements InventoryHolder {

    private static final int COLUMNS = 9;
    private static final int ROWS = 6;

    private final Inventory inventory;
    private final Consumer<Player>[] actions;
    private @Nullable Consumer<Player> otherClick;

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
                button(row * COLUMNS + column, icon, action);
            }
        }
        return this;
    }

    /** A one-slot button; with a {@code null} icon the empty slot is the button. */
    public Menu button(int slot, @Nullable ItemStack icon, Consumer<Player> action) {
        inventory.setItem(slot, icon);
        actions[slot] = action;
        return this;
    }

    /** Shows an item that is not a button. */
    public Menu item(int slot, ItemStack icon) {
        inventory.setItem(slot, icon);
        actions[slot] = null;
        return this;
    }

    public Menu clear(int slot) {
        inventory.setItem(slot, null);
        actions[slot] = null;
        return this;
    }

    /** Runs for a click that hits no button, also in the player's own inventory or outside the window. */
    public Menu onOtherClick(Consumer<Player> action) {
        otherClick = action;
        return this;
    }

    public void open(Player player) {
        player.openInventory(inventory);
    }

    /** The action for a raw slot of the view, or {@code null} for anything that does nothing. */
    @Nullable Consumer<Player> actionAt(int rawSlot) {
        Consumer<Player> action = rawSlot >= 0 && rawSlot < actions.length ? actions[rawSlot] : null;
        return action != null ? action : otherClick;
    }

    boolean isViewedBy(Player player) {
        return player.getOpenInventory().getTopInventory().getHolder(false) == this;
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
