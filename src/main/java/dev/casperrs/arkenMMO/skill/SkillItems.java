package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.menu.MenuIcons;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import net.kyori.adventure.text.serializer.plain.PlainTextComponentSerializer;
import org.bukkit.inventory.ItemStack;
import org.jetbrains.annotations.Nullable;

/** The skill menus' items: their art from the resource pack and their hover text from the messages. */
final class SkillItems {

    /** How a skill stone is drawn. */
    enum Look {
        LOCKED, AVAILABLE, CONFIRM, OWNED;

        private final String id = name().toLowerCase(Locale.ROOT);
    }

    private static final String ASSET_NAMESPACE = "arkenmmo";
    private static final String BLANK_MODEL = "gui/blank";
    /** A lore template line that stands for several lines. */
    private static final String DESCRIPTION_LINE = "<description>";

    private final Messages messages;
    private final SkillValues values;

    SkillItems(Messages messages, SkillValues values) {
        this.messages = messages;
        this.values = values;
    }

    /** Without the name's own colour, for use inside another line. */
    Component skillName(Skill skill) {
        return plain(messages.get(textKey(skill) + ".name"));
    }

    Component className(PlayerClass playerClass) {
        return plain(messages.get("classes." + playerClass.id() + ".name"));
    }

    Component archetypeName(PlayerClass playerClass, String archetype) {
        return messages.get(archetypeKey(playerClass, archetype) + ".name");
    }

    /**
     * A skill stone's hover. {@code showCost} adds the point cost, {@code combo} (or {@code null}) names
     * the loadout slot it sits on, and {@code status} ends the text.
     */
    ItemStack skill(Skill skill, Look look, boolean showCost, @Nullable String combo, List<Component> status) {
        PlayerClass playerClass = skill.playerClass();
        TagResolver numbers = values.placeholders(skill);

        List<Component> lore = new ArrayList<>();
        if (skill.isCore()) {
            lore.add(messages.get("skills.hover.lines.core",
                    Placeholder.component("class", className(playerClass))));
        } else {
            lore.add(messages.get("skills.hover.lines.archetype",
                    Placeholder.component("archetype", archetypeName(playerClass, skill.archetype())),
                    Placeholder.component("type", messages.get(
                            "skills.hover.type." + (skill.active() ? "active" : "passive")))));
        }
        lore.add(Component.empty());
        lore.addAll(messages.getList(textKey(skill) + ".description", numbers));

        List<Component> costs = new ArrayList<>();
        if (skill.active()) {
            costs.add(messages.get("skills.hover.lines.mana", numbers));
        }
        if (showCost && !skill.isCore()) {
            costs.add(messages.get("skills.hover.lines.cost", number("cost", skill.node().cost())));
        }
        if (combo != null) {
            costs.add(messages.get("skills.hover.lines.combo", Placeholder.unparsed("combo", combo)));
        }
        if (!costs.isEmpty()) {
            lore.add(Component.empty());
            lore.addAll(costs);
        }
        lore.add(Component.empty());
        lore.addAll(status);

        return MenuIcons.of(
                key("gui/skill/" + playerClass.id() + "/" + skill.key() + "/" + look.id),
                messages.get(textKey(skill) + ".name"), lore, tooltipStyle(playerClass));
    }

    /** An item whose text is the {@code name} and {@code lore} below {@code textKey}, drawn with a pack model. */
    ItemStack described(PlayerClass playerClass, String model, String textKey, TagResolver... resolvers) {
        return item(playerClass, model, textKey, messages.getList(textKey + ".lore", resolvers), resolvers);
    }

    /** An invisible item over something painted into the title. */
    ItemStack painted(PlayerClass playerClass, String textKey, TagResolver... resolvers) {
        return described(playerClass, BLANK_MODEL, textKey, resolvers);
    }

    ItemStack tab(PlayerClass playerClass, String archetype, String textKey, int spent) {
        TagResolver[] resolvers = {
                Placeholder.parsed("colour", messages.raw("skills.colours." + playerClass.id())),
                Placeholder.component("archetype", archetypeName(playerClass, archetype)),
                number("spent", spent)};
        List<Component> lore = new ArrayList<>();
        for (String line : messages.rawList(textKey + ".lore")) {
            if (line.equals(DESCRIPTION_LINE)) {
                lore.addAll(messages.getList(archetypeKey(playerClass, archetype) + ".description"));
            } else {
                lore.add(messages.parse(line, resolvers));
            }
        }
        return item(playerClass, BLANK_MODEL, textKey, lore, resolvers);
    }

    ItemStack connector(PlayerClass playerClass, String shape) {
        return MenuIcons.decoration(key("gui/skill/" + playerClass.id() + "/link/" + shape));
    }

    static TagResolver number(String name, long value) {
        return Placeholder.unparsed(name, Long.toString(value));
    }

    private ItemStack item(PlayerClass playerClass, String model, String textKey, List<Component> lore,
                           TagResolver... resolvers) {
        return MenuIcons.of(key(model), messages.get(textKey + ".name", resolvers), lore, tooltipStyle(playerClass));
    }

    private static Component plain(Component component) {
        return Component.text(PlainTextComponentSerializer.plainText().serialize(component));
    }

    private static String textKey(Skill skill) {
        return "skills.list." + skill.playerClass().id() + "." + skill.key();
    }

    private static String archetypeKey(PlayerClass playerClass, String archetype) {
        return "skills.archetypes." + playerClass.id() + "." + archetype;
    }

    private static Key key(String value) {
        return Key.key(ASSET_NAMESPACE, value);
    }

    private static Key tooltipStyle(PlayerClass playerClass) {
        return key(playerClass.id());
    }
}
