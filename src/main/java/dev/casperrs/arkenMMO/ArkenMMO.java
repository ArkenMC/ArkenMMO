package dev.casperrs.arkenMMO;

import dev.casperrs.arkenMMO.casting.Casters;
import dev.casperrs.arkenMMO.casting.CastingHud;
import dev.casperrs.arkenMMO.casting.CastingListener;
import dev.casperrs.arkenMMO.casting.CombatListener;
import dev.casperrs.arkenMMO.casting.ComboInput;
import dev.casperrs.arkenMMO.casting.ManaRules;
import dev.casperrs.arkenMMO.casting.SkillAction;
import dev.casperrs.arkenMMO.casting.SkillCaster;
import dev.casperrs.arkenMMO.casting.SkillFeedback;
import dev.casperrs.arkenMMO.combat.OngoingActions;
import dev.casperrs.arkenMMO.combat.OngoingListener;
import dev.casperrs.arkenMMO.combat.SkillDamage;
import dev.casperrs.arkenMMO.sound.SoundService;
import dev.casperrs.arkenMMO.warrior.Cleave;
import dev.casperrs.arkenMMO.warrior.Execute;
import dev.casperrs.arkenMMO.warrior.LeapingStrike;
import dev.casperrs.arkenMMO.warrior.Whirlwind;
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
import dev.casperrs.arkenMMO.vfx.Effects;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import java.util.Map;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.Nullable;

public final class ArkenMMO extends JavaPlugin {

    private @Nullable OngoingActions ongoing;
    private @Nullable Effects effects;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        Messages messages = Messages.load(this);
        ResourcePackService resourcePack = new ResourcePackService(
                messages, ResourcePackSettings.read(getConfig(), getLogger()).orElse(null));
        ClassStorage classes = new ClassStorage(this);
        ClassSelection selection = new ClassSelection(classes, resourcePack, messages);
        SkillBook skills = new SkillBook(new SkillStorage(this), SkillSettings.read(getConfig()), messages);
        SkillValues skillValues = SkillValues.load(this);
        SkillMenus skillMenus = new SkillMenus(skills, skillValues, classes, resourcePack, messages);

        PluginManager plugins = getServer().getPluginManager();
        plugins.registerEvents(resourcePack, this);
        plugins.registerEvents(new MenuListener(this), this);
        startCasting(classes, skills, skillValues, messages);

        ClassCommand classCommand = new ClassCommand(selection, messages);
        SkillsCommand skillsCommand = new SkillsCommand(skillMenus, messages);
        getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS, event -> {
            event.registrar().register(classCommand.node(), "Choose your class");
            event.registrar().register(skillsCommand.node(), "Open your skill tree");
        });
    }

    @Override
    public void onDisable() {
        if (ongoing != null) {
            ongoing.cancelAll();
        }
        if (effects != null) {
            effects.shutdown();
        }
        MenuListener.closeAll();
    }

    private void startCasting(ClassStorage classes, SkillBook skills, SkillValues values, Messages messages) {
        SoundService sounds = SoundService.load(this);
        effects = Effects.load(this);
        SkillFeedback feedback = new SkillFeedback(sounds, effects);
        ongoing = new OngoingActions(this);
        SkillDamage damage = new SkillDamage(() -> values.number("power.base")
                + values.number("power.per_level") * (skills.level() - 1));
        Map<String, SkillAction> actions = Map.of(
                "warrior.cleave", new Cleave(values, damage, feedback),
                "warrior.leaping_strike", new LeapingStrike(values, damage, feedback, ongoing),
                "warrior.whirlwind", new Whirlwind(values, damage, feedback, ongoing),
                "warrior.execute", new Execute(values, damage, feedback));

        Casters casters = new Casters(ManaRules.read(values));
        CastingHud hud = new CastingHud(this, classes, casters, messages);
        SkillCaster caster = new SkillCaster(skills, values, casters, hud, sounds, messages, actions);
        ComboInput combos = new ComboInput(this, classes, messages, hud, sounds, caster,
                getConfig().getBoolean("debug.casting", false) ? getLogger() : null);

        PluginManager plugins = getServer().getPluginManager();
        plugins.registerEvents(new CastingListener(combos, hud), this);
        plugins.registerEvents(new CombatListener(casters), this);
        plugins.registerEvents(new OngoingListener(ongoing), this);
    }
}
