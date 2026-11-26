package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;
import java.util.logging.Logger;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.Nullable;

/** Feeds clicks into each player's combo and shows it on the action bar. Main thread only. */
public final class ComboInput {

    private static final List<String> POSITIONS = List.of("first", "second", "third");

    private final ClassStorage classes;
    private final Messages messages;
    private final @Nullable Logger debugLog;
    private final Map<UUID, ComboTracker> trackers = new HashMap<>();

    /** A {@code null} logger turns click debugging off. */
    public ComboInput(ClassStorage classes, Messages messages, @Nullable Logger debugLog) {
        this.classes = classes;
        this.messages = messages;
        this.debugLog = debugLog;
    }

    void click(Player player, Click click, String source) {
        Optional<PlayerClass> wielding = wieldingClass(player);
        if (wielding.isEmpty()) {
            reset(player);
            debug(player, () -> source + " " + click + " -> no class weapon");
            return;
        }
        ComboTracker.Result result = tracker(player).click(
                click, wielding.get() == PlayerClass.ARCHER, Bukkit.getCurrentTick(), System.nanoTime() / 1_000_000);
        debug(player, () -> source + " " + click + " -> " + result.status().name().toLowerCase(Locale.ROOT));
        switch (result.status()) {
            case PROGRESS -> show(player, "casting.progress", result);
            case COMPLETED -> show(player, "casting.completed", result);
            case NOT_STARTED, SAME_TICK, HELD_REPEAT -> {
            }
        }
    }

    void ignore(Player player, String reason) {
        tracker(player).ignoreTick(Bukkit.getCurrentTick());
        debug(player, () -> "ignoring this tick: " + reason);
    }

    /** True if the arrow now being released belongs to a combo click. */
    boolean swallowsShot(Player player) {
        ComboTracker tracker = trackers.get(player.getUniqueId());
        return tracker != null && tracker.drawInCombo()
                && wieldingClass(player).filter(PlayerClass.ARCHER::equals).isPresent();
    }

    void reset(Player player) {
        ComboTracker tracker = trackers.get(player.getUniqueId());
        if (tracker != null) {
            tracker.reset();
        }
    }

    void forget(Player player) {
        trackers.remove(player.getUniqueId());
    }

    void debug(Player player, Supplier<String> line) {
        if (debugLog != null) {
            debugLog.info("[casting] " + player.getName() + " tick " + Bukkit.getCurrentTick() + ": " + line.get());
        }
    }

    /** The player's class, if they hold its weapon in the main hand and can fight. */
    private Optional<PlayerClass> wieldingClass(Player player) {
        if (player.getGameMode() == GameMode.SPECTATOR) {
            return Optional.empty();
        }
        return classes.get(player).filter(playerClass ->
                StandInWeapons.matches(playerClass, player.getInventory().getItemInMainHand().getType()));
    }

    private ComboTracker tracker(Player player) {
        return trackers.computeIfAbsent(player.getUniqueId(), id -> new ComboTracker());
    }

    private void show(Player player, String key, ComboTracker.Result result) {
        TagResolver.Builder resolvers = TagResolver.builder()
                .resolver(Placeholder.unparsed("slot", Integer.toString(result.slot())));
        for (int i = 0; i < ComboTracker.LENGTH; i++) {
            String name = i < result.clicks().size()
                    ? result.clicks().get(i).name().toLowerCase(Locale.ROOT)
                    : "pending";
            Component text = messages.get("casting.clicks." + name);
            resolvers.resolver(Placeholder.component(POSITIONS.get(i), text));
        }
        player.sendActionBar(messages.get(key, resolvers.build()));
    }
}
