package dev.casperrs.arkenMMO.playerclass;

import java.util.Locale;
import java.util.Optional;

/** The playable classes, in menu order. The {@link #id()} is what gets stored and names assets and config keys. */
public enum PlayerClass {
    WARRIOR,
    ARCHER,
    MAGE,
    CAPTAIN;

    private final String id = name().toLowerCase(Locale.ROOT);

    public String id() {
        return id;
    }

    public static Optional<PlayerClass> byId(String id) {
        for (PlayerClass playerClass : values()) {
            if (playerClass.id.equals(id)) {
                return Optional.of(playerClass);
            }
        }
        return Optional.empty();
    }
}
