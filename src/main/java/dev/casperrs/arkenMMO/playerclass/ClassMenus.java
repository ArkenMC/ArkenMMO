package dev.casperrs.arkenMMO.playerclass;

import dev.casperrs.arkenMMO.menu.Menu;
import dev.casperrs.arkenMMO.menu.MenuIcons;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Predicate;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.jetbrains.annotations.Nullable;

/**
 * The class pages and confirm screens. Their slots must match the art painted into the titles;
 * the items are invisible and only carry tooltips.
 */
final class ClassMenus {

    private static final String ASSET_NAMESPACE = "arkenmmo";
    private static final Key BLANK_MODEL = Key.key(ASSET_NAMESPACE, "gui/blank");
    private static final int CLASSES_PER_PAGE = 2;

    private final Predicate<Player> mayChoose;
    private final BiConsumer<Player, PlayerClass> onConfirm;

    private final List<Component> pageTitles;
    private final Map<PlayerClass, Component> confirmTitles = new EnumMap<>(PlayerClass.class);
    private final Map<PlayerClass, ItemStack> panelIcons = new EnumMap<>(PlayerClass.class);
    private final Map<PlayerClass, ItemStack> confirmIcons = new EnumMap<>(PlayerClass.class);
    private final ItemStack nextIcon;
    private final ItemStack previousIcon;
    private final ItemStack backIcon;

    /** {@code mayChoose} is asked before any click is acted on and handles a refusal itself. */
    ClassMenus(Messages messages, Predicate<Player> mayChoose, BiConsumer<Player, PlayerClass> onConfirm) {
        this.mayChoose = mayChoose;
        this.onConfirm = onConfirm;
        this.pageTitles = List.of(
                messages.get("menu.titles.class-select-1"),
                messages.get("menu.titles.class-select-2"));
        for (PlayerClass playerClass : PlayerClass.values()) {
            Component name = messages.get("classes." + playerClass.id() + ".name");
            List<Component> panelLore = new ArrayList<>(
                    messages.getList("classes." + playerClass.id() + ".description"));
            panelLore.addAll(messages.getList("menu.panel-footer"));
            panelIcons.put(playerClass, icon(name, panelLore, Key.key(ASSET_NAMESPACE, playerClass.id())));
            confirmTitles.put(playerClass, messages.get("menu.titles.confirm-" + playerClass.id()));
            confirmIcons.put(playerClass, icon(
                    messages.get("menu.confirm.name", Placeholder.component("class", name)),
                    messages.getList("menu.confirm.lore", Placeholder.component("class", name))));
        }
        this.nextIcon = icon(messages.get("menu.next-page"));
        this.previousIcon = icon(messages.get("menu.previous-page"));
        this.backIcon = icon(messages.get("menu.back"));
    }

    void openFirstPage(Player player) {
        openPage(player, 0);
    }

    private void openPage(Player player, int page) {
        PlayerClass[] classes = PlayerClass.values();
        PlayerClass left = classes[page * CLASSES_PER_PAGE];
        PlayerClass right = classes[page * CLASSES_PER_PAGE + 1];
        int otherPage = 1 - page;
        new Menu(pageTitles.get(page))
                .button(0, 3, 0, 5, panelIcons.get(left), guarded(viewer -> openConfirm(viewer, left)))
                .button(5, 8, 0, 5, panelIcons.get(right), guarded(viewer -> openConfirm(viewer, right)))
                .button(4, 4, 4, 5, page == 0 ? nextIcon : previousIcon,
                        guarded(viewer -> openPage(viewer, otherPage)))
                .open(player);
    }

    private void openConfirm(Player player, PlayerClass playerClass) {
        int page = playerClass.ordinal() / CLASSES_PER_PAGE;
        new Menu(confirmTitles.get(playerClass))
                .button(5, 8, 1, 2, confirmIcons.get(playerClass),
                        guarded(viewer -> onConfirm.accept(viewer, playerClass)))
                .button(5, 8, 3, 4, backIcon, guarded(viewer -> openPage(viewer, page)))
                .open(player);
    }

    private Consumer<Player> guarded(Consumer<Player> action) {
        return player -> {
            if (mayChoose.test(player)) {
                action.accept(player);
            }
        };
    }

    private static ItemStack icon(Component name) {
        return icon(name, List.of());
    }

    private static ItemStack icon(Component name, List<Component> lore) {
        return icon(name, lore, null);
    }

    private static ItemStack icon(Component name, List<Component> lore, @Nullable Key tooltipStyle) {
        return MenuIcons.of(BLANK_MODEL, name, lore, tooltipStyle);
    }
}
