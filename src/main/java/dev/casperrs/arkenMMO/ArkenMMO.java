package dev.casperrs.arkenMMO;

import dev.casperrs.arkenMMO.menu.MenuListener;
import dev.casperrs.arkenMMO.playerclass.ClassCommand;
import dev.casperrs.arkenMMO.playerclass.ClassSelection;
import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.text.Messages;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import org.bukkit.plugin.java.JavaPlugin;

public final class ArkenMMO extends JavaPlugin {

    @Override
    public void onEnable() {
        Messages messages = Messages.load(this);
        ClassSelection selection = new ClassSelection(new ClassStorage(this), messages);

        getServer().getPluginManager().registerEvents(new MenuListener(this), this);

        ClassCommand classCommand = new ClassCommand(selection, messages);
        getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS, event ->
                event.registrar().register(classCommand.node(), "Choose your class"));
    }

    @Override
    public void onDisable() {
        MenuListener.closeAll();
    }
}
