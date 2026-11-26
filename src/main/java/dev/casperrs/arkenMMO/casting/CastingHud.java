package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.plugin.Plugin;
import org.bukkit.scheduler.BukkitTask;
import org.jetbrains.annotations.Nullable;

/**
 * The action bar of players holding their class weapon: mana, and for a moment the combo or why a cast
 * failed. One shared task redraws it and stops when nobody is shown anything. Main thread only.
 */
public final class CastingHud {

    private static final long PERIOD_TICKS = 10;

    /** {@code until} is on the {@link Casters#now()} clock. */
    private record Line(Component text, long until) {
    }

    private final Plugin plugin;
    private final ClassStorage classes;
    private final Casters casters;
    private final Messages messages;
    private final Set<UUID> watched = new HashSet<>();
    private final Map<UUID, Line> lines = new HashMap<>();
    // One per whole mana value, so most redraws don't parse anything
    private final Map<Integer, Component> manaTexts = new HashMap<>();
    private @Nullable BukkitTask task;

    public CastingHud(Plugin plugin, ClassStorage classes, Casters casters, Messages messages) {
        this.plugin = plugin;
        this.classes = classes;
        this.casters = casters;
        this.messages = messages;
    }

    /** Shows the bar from the next redraw on, for as long as the player holds their class weapon. */
    void watch(Player player) {
        watched.add(player.getUniqueId());
        if (task == null) {
            task = Bukkit.getScheduler().runTaskTimer(plugin, this::redraw, 1, PERIOD_TICKS);
        }
    }

    void show(Player player, Component line, long millis) {
        lines.put(player.getUniqueId(), new Line(line, Casters.now() + millis));
        watch(player);
        draw(player);
    }

    void clear(Player player) {
        lines.remove(player.getUniqueId());
    }

    void forget(Player player) {
        clear(player);
        watched.remove(player.getUniqueId());
    }

    private void redraw() {
        watched.removeIf(playerId -> {
            Player player = Bukkit.getPlayer(playerId);
            if (player == null || !StandInWeapons.isWielding(player, classes)) {
                lines.remove(playerId);
                return true;
            }
            draw(player);
            return false;
        });
        if (watched.isEmpty() && task != null) {
            task.cancel();
            task = null;
        }
    }

    private void draw(Player player) {
        long now = Casters.now();
        Component mana = manaTexts.computeIfAbsent((int) casters.of(player).mana(now), value ->
                messages.get("casting.mana",
                        Placeholder.unparsed("mana", Integer.toString(value)),
                        Placeholder.unparsed("max", Integer.toString(casters.maxMana()))));
        Line line = lines.get(player.getUniqueId());
        player.sendActionBar(line == null || now >= line.until() ? mana : messages.get("casting.bar",
                Placeholder.component("line", line.text()), Placeholder.component("mana_text", mana)));
    }
}
