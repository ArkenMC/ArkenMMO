package dev.casperrs.arkenMMO;

import dev.casperrs.arkenMMO.casting.CastingListener;
import dev.casperrs.arkenMMO.casting.ComboInput;
import dev.casperrs.arkenMMO.menu.MenuListener;
import dev.casperrs.arkenMMO.pack.ResourcePackService;
import dev.casperrs.arkenMMO.pack.ResourcePackSettings;
import dev.casperrs.arkenMMO.playerclass.ClassCommand;
import dev.casperrs.arkenMMO.playerclass.ClassSelection;
import dev.casperrs.arkenMMO.playerclass.ClassStorage;
import dev.casperrs.arkenMMO.skill.SkillBook;
import dev.casperrs.arkenMMO.skill.SkillMenus;
import dev.casperrs.arkenMMO.skill.SkillSettings;
import dev.casperrs.arkenMMO.skill.SkillStorage;
import dev.casperrs.arkenMMO.skill.SkillValues;
import dev.casperrs.arkenMMO.skill.SkillsCommand;
import dev.casperrs.arkenMMO.text.Messages;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;

public final class ArkenMMO extends JavaPlugin {

    @Override
    public void onEnable() {
        saveDefaultConfig();
        Messages messages = Messages.load(this);
        ResourcePackService resourcePack = new ResourcePackService(
                messages, ResourcePackSettings.read(getConfig(), getLogger()).orElse(null));
        ClassStorage classes = new ClassStorage(this);
        ClassSelection selection = new ClassSelection(classes, resourcePack, messages);
        SkillBook skills = new SkillBook(new SkillStorage(this), SkillSettings.read(getConfig()), messages);
        SkillMenus skillMenus = new SkillMenus(
                skills, SkillValues.load(this), classes, resourcePack, messages);
        ComboInput combos = new ComboInput(
                classes, messages, getConfig().getBoolean("debug.casting", false) ? getLogger() : null);

        PluginManager plugins = getServer().getPluginManager();
        plugins.registerEvents(resourcePack, this);
        plugins.registerEvents(new MenuListener(this), this);
        plugins.registerEvents(new CastingListener(combos), this);

        ClassCommand classCommand = new ClassCommand(selection, messages);
        SkillsCommand skillsCommand = new SkillsCommand(skillMenus, messages);
        getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS, event -> {
            event.registrar().register(classCommand.node(), "Choose your class");
            event.registrar().register(skillsCommand.node(), "Open your skill tree");
        });
    }

    @Override
    public void onDisable() {
        MenuListener.closeAll();
    }
}
