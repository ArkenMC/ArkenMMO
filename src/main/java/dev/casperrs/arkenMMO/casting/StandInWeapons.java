package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import org.bukkit.Material;

/** Temporary vanilla items that count as class weapons until the real class weapons exist. */
final class StandInWeapons {

    private StandInWeapons() {
    }

    static boolean matches(PlayerClass playerClass, Material held) {
        return held == switch (playerClass) {
            case WARRIOR -> Material.IRON_SWORD;
            case ARCHER -> Material.BOW;
            case MAGE -> Material.STICK;
            case CAPTAIN -> Material.GOLDEN_SWORD;
        };
    }
}
