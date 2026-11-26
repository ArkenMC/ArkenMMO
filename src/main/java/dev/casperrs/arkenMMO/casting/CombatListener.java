package dev.casperrs.arkenMMO.casting;

import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.entity.Projectile;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;

/** Dealing or taking damage puts a player in combat, which slows mana regeneration. */
public final class CombatListener implements Listener {

    private final Casters casters;

    public CombatListener(Casters casters) {
        this.casters = casters;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onDamage(EntityDamageByEntityEvent event) {
        Entity victim = event.getEntity();
        if (!(victim instanceof LivingEntity) || victim instanceof ArmorStand) {
            return;
        }
        fight(victim);
        Entity damager = event.getDamager();
        if (damager instanceof Projectile projectile && projectile.getShooter() instanceof Entity shooter) {
            damager = shooter;
        }
        fight(damager);
    }

    private void fight(Entity entity) {
        if (entity instanceof Player player) {
            casters.of(player).fight(Casters.now());
        }
    }
}
