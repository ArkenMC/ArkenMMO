package dev.casperrs.arkenMMO.combat;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.plugin.Plugin;
import org.bukkit.scheduler.BukkitTask;
import org.jetbrains.annotations.Nullable;

/** Runs every ongoing skill from one task, which only exists while there is one. Main thread only. */
public final class OngoingActions {

    // Compared by identity: each start is its own entry
    private static final class Entry {

        private final UUID owner;
        private final OngoingAction action;

        private Entry(UUID owner, OngoingAction action) {
            this.owner = owner;
            this.action = action;
        }
    }

    private final Plugin plugin;
    private final List<Entry> entries = new ArrayList<>();
    private @Nullable BukkitTask task;

    public OngoingActions(Plugin plugin) {
        this.plugin = plugin;
    }

    public void start(Player owner, OngoingAction action) {
        entries.add(new Entry(owner.getUniqueId(), action));
        if (task == null) {
            task = Bukkit.getScheduler().runTaskTimer(plugin, this::tick, 1, 1);
        }
    }

    public boolean preventsFallDamage(Player player) {
        return entries.stream().anyMatch(entry ->
                entry.owner.equals(player.getUniqueId()) && entry.action.preventsFallDamage());
    }

    public void cancel(Player owner) {
        for (Entry entry : List.copyOf(entries)) {
            if (entry.owner.equals(owner.getUniqueId()) && entries.remove(entry)) {
                entry.action.cancel(owner);
            }
        }
        stopIfIdle();
    }

    public void cancelAll() {
        for (Entry entry : List.copyOf(entries)) {
            Player owner = Bukkit.getPlayer(entry.owner);
            if (entries.remove(entry) && owner != null) {
                entry.action.cancel(owner);
            }
        }
        stopIfIdle();
    }

    private void tick() {
        // A copy, because an action's damage can kill its owner, which cancels entries during the loop
        for (Entry entry : List.copyOf(entries)) {
            if (!entries.contains(entry)) {
                continue;
            }
            Player owner = Bukkit.getPlayer(entry.owner);
            if (owner == null || owner.isDead() || !entry.action.tick(owner)) {
                entries.remove(entry);
            }
        }
        stopIfIdle();
    }

    private void stopIfIdle() {
        if (entries.isEmpty() && task != null) {
            task.cancel();
            task = null;
        }
    }
}
