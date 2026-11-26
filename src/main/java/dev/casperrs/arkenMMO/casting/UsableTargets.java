package dev.casperrs.arkenMMO.casting;

import java.util.List;
import java.util.Set;
import org.bukkit.Material;
import org.bukkit.Tag;
import org.bukkit.block.Block;
import org.bukkit.entity.AbstractVillager;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Enemy;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Hanging;
import org.bukkit.entity.Interaction;
import org.bukkit.entity.Tameable;
import org.bukkit.entity.Vehicle;
import org.bukkit.inventory.InventoryHolder;

/**
 * Blocks and entities that do something when right-clicked with a weapon, so that click isn't part of a combo.
 * The API has no current "is this usable" query ({@code Material#isInteractable} is deprecated).
 */
final class UsableTargets {

    private static final List<Tag<Material>> BLOCK_TAGS = List.of(
            Tag.DOORS, Tag.TRAPDOORS, Tag.FENCE_GATES, Tag.BUTTONS, Tag.BEDS, Tag.ALL_SIGNS, Tag.ANVIL,
            Tag.CANDLE_CAKES);

    // Blocks with their own inventory are found through InventoryHolder instead.
    private static final Set<Material> BLOCKS = Set.of(
            Material.ENDER_CHEST, Material.CRAFTING_TABLE, Material.ENCHANTING_TABLE, Material.SMITHING_TABLE,
            Material.CARTOGRAPHY_TABLE, Material.GRINDSTONE, Material.LOOM, Material.STONECUTTER,
            Material.BEACON, Material.LEVER, Material.BELL, Material.NOTE_BLOCK, Material.REPEATER,
            Material.COMPARATOR, Material.DAYLIGHT_DETECTOR, Material.CAKE, Material.RESPAWN_ANCHOR,
            Material.DRAGON_EGG);

    private UsableTargets() {
    }

    static boolean isUsable(Block block) {
        Material type = block.getType();
        return BLOCKS.contains(type)
                || BLOCK_TAGS.stream().anyMatch(tag -> tag.isTagged(type))
                || block.getState(false) instanceof InventoryHolder;
    }

    static boolean isUsable(Entity entity) {
        // First, because some enemies (piglins, pillagers) have an inventory.
        if (entity instanceof Enemy) {
            return false;
        }
        return entity instanceof AbstractVillager
                || entity instanceof InventoryHolder
                || entity instanceof Vehicle
                || entity instanceof Hanging
                || entity instanceof ArmorStand
                || entity instanceof Tameable
                || entity instanceof Interaction;
    }
}
