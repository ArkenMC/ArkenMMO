package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.sound.SoundService;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.function.Supplier;
import java.util.logging.Logger;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.Nullable;

/**
 * Feeds clicks into each player's combo and casts completed ones. A left click is held for a tick, because
 * the swing of a dropped item can reach the server before the drop does. Main thread only.
 */
public final class ComboInput {

    private static final List<String> POSITIONS = List.of("first", "second", "third");

    // Compared by identity, so that a click's delayed task can't take a later one
    private static final class Press {

        private final String source;
        private final int tick;
        private final long millis;

        private Press(String source, int tick, long millis) {
            this.source = source;
            this.tick = tick;
            this.millis = millis;
        }
    }

    private final Plugin plugin;
    private final ClassStorage classes;
    private final Messages messages;
    private final CastingHud hud;
    private final SoundService sounds;
    private final SkillCaster caster;
    private final @Nullable Logger debugLog;
    private final Map<UUID, ComboTracker> trackers = new HashMap<>();
    private final Map<UUID, Press> waitingLefts = new HashMap<>();

    /** A {@code null} logger turns click debugging off. */
    public ComboInput(Plugin plugin, ClassStorage classes, Messages messages, CastingHud hud, SoundService sounds,
                      SkillCaster caster, @Nullable Logger debugLog) {
        this.plugin = plugin;
        this.classes = classes;
        this.messages = messages;
        this.hud = hud;
        this.sounds = sounds;
        this.caster = caster;
        this.debugLog = debugLog;
    }

    void click(Player player, Click click, String source) {
        // Anything that arrives now shows that the waiting left click didn't come with a drop
        flush(player);
        if (!StandInWeapons.isWielding(player, classes)) {
            reset(player);
            debug(player, () -> source + " " + click + " -> no class weapon");
            return;
        }
        Press press = new Press(source, Bukkit.getCurrentTick(), System.nanoTime() / 1_000_000);
        if (click == Click.RIGHT) {
            count(player, click, press);
            return;
        }
        waitingLefts.put(player.getUniqueId(), press);
        Bukkit.getScheduler().runTask(plugin, () -> {
            if (waitingLefts.get(player.getUniqueId()) == press) {
                flush(player);
            }
        });
    }

    /** A drop: neither its swing nor anything else in this tick is a click. */
    void drop(Player player) {
        Press swing = waitingLefts.remove(player.getUniqueId());
        if (swing != null) {
            debug(player, () -> swing.source + " LEFT -> discarded, it came with a drop");
        }
        claimTick(player, "dropped an item");
    }

    /** Something else used this tick's click, such as a door. */
    void ignore(Player player, String reason) {
        flush(player);
        claimTick(player, reason);
    }

    void reset(Player player) {
        waitingLefts.remove(player.getUniqueId());
        ComboTracker tracker = trackers.get(player.getUniqueId());
        if (tracker != null) {
            tracker.reset();
        }
        hud.clear(player);
    }

    void forget(Player player) {
        waitingLefts.remove(player.getUniqueId());
        trackers.remove(player.getUniqueId());
        hud.forget(player);
    }

    void debug(Player player, Supplier<String> line) {
        if (debugLog != null) {
            debugLog.info("[casting] " + player.getName() + " tick " + Bukkit.getCurrentTick() + ": " + line.get());
        }
    }

    private void flush(Player player) {
        Press press = waitingLefts.remove(player.getUniqueId());
        if (press != null && player.isOnline() && StandInWeapons.isWielding(player, classes)) {
            count(player, Click.LEFT, press);
        }
    }

    private void claimTick(Player player, String reason) {
        tracker(player).ignoreTick(Bukkit.getCurrentTick());
        debug(player, () -> "ignoring this tick: " + reason);
    }

    private void count(Player player, Click click, Press press) {
        PlayerClass playerClass = classes.get(player).orElseThrow();
        ComboTracker.Result result = tracker(player).click(
                click, playerClass == PlayerClass.ARCHER, press.tick, press.millis);
        debug(player, () -> press.source + " " + click + " from tick " + press.tick + " -> "
                + result.status().name().toLowerCase(Locale.ROOT));
        switch (result.status()) {
            case PROGRESS -> {
                playClick(player, click);
                hud.show(player, messages.get("casting.progress", clicks(result)), ComboTracker.TIMEOUT_MILLIS);
            }
            case COMPLETED -> {
                playClick(player, click);
                caster.cast(player, playerClass, result.slot(), clicks(result));
            }
            case NOT_STARTED, SAME_TICK, HELD_REPEAT -> {
            }
        }
    }

    private void playClick(Player player, Click click) {
        sounds.playTo(player, "combo_click_" + click.name().toLowerCase(Locale.ROOT));
    }

    private ComboTracker tracker(Player player) {
        return trackers.computeIfAbsent(player.getUniqueId(), id -> new ComboTracker());
    }

    private TagResolver clicks(ComboTracker.Result result) {
        TagResolver.Builder resolvers = TagResolver.builder();
        for (int i = 0; i < ComboTracker.LENGTH; i++) {
            String name = i < result.clicks().size()
                    ? result.clicks().get(i).name().toLowerCase(Locale.ROOT)
                    : "pending";
            Component text = messages.get("casting.clicks." + name);
            resolvers.resolver(Placeholder.component(POSITIONS.get(i), text));
        }
        return resolvers.build();
    }
}
