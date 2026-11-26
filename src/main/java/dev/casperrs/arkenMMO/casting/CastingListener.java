package dev.casperrs.arkenMMO.casting;

import io.papermc.paper.event.player.PlayerArmSwingEvent;
import io.papermc.paper.event.player.PrePlayerAttackEntityEvent;
import org.bukkit.block.Block;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.entity.EntityShootBowEvent;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.player.PlayerDropItemEvent;
import org.bukkit.event.player.PlayerInteractEntityEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.event.player.PlayerItemHeldEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.inventory.EquipmentSlot;

/**
 * Turns server events into combo clicks. It only watches: vanilla behaviour stays, except that combo arrows
 * don't fly. The click events don't skip cancelled ones, because air clicks arrive already cancelled.
 */
public final class CastingListener implements Listener {

    private final ComboInput input;

    public CastingListener(ComboInput input) {
        this.input = input;
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onInteract(PlayerInteractEvent event) {
        if (event.getHand() != EquipmentSlot.HAND) {
            return;
        }
        Player player = event.getPlayer();
        Action action = event.getAction();
        if (action.isLeftClick()) {
            input.click(player, Click.LEFT, action.name());
        } else if (action.isRightClick()) {
            Block block = event.getClickedBlock();
            if (block != null && usesBlock(player, block)) {
                input.ignore(player, "used " + block.getType());
            } else {
                input.click(player, Click.RIGHT, action.name());
            }
        }
    }

    // Covers hits on entities, which raise no LEFT_CLICK interact event.
    @EventHandler(priority = EventPriority.MONITOR)
    public void onAttack(PrePlayerAttackEntityEvent event) {
        input.click(event.getPlayer(), Click.LEFT, "ATTACK " + event.getAttacked().getType());
    }

    // Not a click: the left clicks it could report already arrive above. Logged to diagnose phantom clicks.
    @EventHandler(priority = EventPriority.MONITOR)
    public void onArmSwing(PlayerArmSwingEvent event) {
        input.debug(event.getPlayer(), () -> "ARM_SWING " + event.getHand() + " (not counted)");
    }

    // Also receives PlayerInteractAtEntityEvent, which shares this handler list.
    @EventHandler(priority = EventPriority.MONITOR)
    public void onInteractEntity(PlayerInteractEntityEvent event) {
        if (event.getHand() != EquipmentSlot.HAND) {
            return;
        }
        Entity target = event.getRightClicked();
        if (UsableTargets.isUsable(target)) {
            input.ignore(event.getPlayer(), "used " + target.getType());
        } else {
            input.click(event.getPlayer(), Click.RIGHT, "INTERACT_ENTITY " + target.getType());
        }
    }

    // A client may swing after dropping, which the server reports as a left click in the air.
    @EventHandler(priority = EventPriority.MONITOR)
    public void onDrop(PlayerDropItemEvent event) {
        input.ignore(event.getPlayer(), "dropped an item");
    }

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onShoot(EntityShootBowEvent event) {
        if (event.getEntity() instanceof Player player && input.swallowsShot(player)) {
            event.setCancelled(true);
            input.debug(player, () -> "arrow cancelled: its draw was a combo click");
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onItemHeld(PlayerItemHeldEvent event) {
        input.reset(event.getPlayer());
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onDeath(PlayerDeathEvent event) {
        input.reset(event.getPlayer());
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent event) {
        input.forget(event.getPlayer());
    }

    // Vanilla skips the block's own action while sneaking with an item, and a combo weapon is in hand then.
    private static boolean usesBlock(Player player, Block block) {
        return !player.isSneaking() && UsableTargets.isUsable(block);
    }
}
