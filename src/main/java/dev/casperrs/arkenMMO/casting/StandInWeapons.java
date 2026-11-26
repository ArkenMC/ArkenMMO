package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import org.bukkit.GameMode;
import org.bukkit.Material;
import org.bukkit.entity.Player;

/** Temporary: until class weapons exist, a Warrior's iron sword counts. No other class can cast yet. */
final class StandInWeapons {

    private StandInWeapons() {
    }

    /** Whether the player can fight and holds their class weapon in the main hand. */
    static boolean isWielding(Player player, ClassStorage classes) {
        // The item first: it is much cheaper to read than the stored class
        return player.getInventory().getItemInMainHand().getType() == Material.IRON_SWORD
                && player.getGameMode() != GameMode.SPECTATOR
                && classes.get(player).filter(PlayerClass.WARRIOR::equals).isPresent();
    }
}
