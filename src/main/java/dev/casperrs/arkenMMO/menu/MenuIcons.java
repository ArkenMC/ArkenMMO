package dev.casperrs.arkenMMO.menu;

import io.papermc.paper.datacomponent.DataComponentTypes;
import io.papermc.paper.datacomponent.item.ItemLore;
import io.papermc.paper.datacomponent.item.TooltipDisplay;
import java.util.List;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.TextDecoration;
import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;
import org.jetbrains.annotations.Nullable;

/** Items that only exist to be shown in a {@link Menu}. */
public final class MenuIcons {

    private MenuIcons() {
    }

    /** {@code tooltipStyle} {@code null} keeps the vanilla tooltip. */
    public static ItemStack of(Key model, Component name, List<Component> lore, @Nullable Key tooltipStyle) {
        ItemStack icon = base(model);
        icon.setData(DataComponentTypes.ITEM_NAME, name);
        if (!lore.isEmpty()) {
            // The client shows lore in italics unless told otherwise
            icon.setData(DataComponentTypes.LORE, ItemLore.lore(lore.stream()
                    .map(line -> line.decorationIfAbsent(TextDecoration.ITALIC, TextDecoration.State.FALSE))
                    .toList()));
        }
        if (tooltipStyle != null) {
            icon.setData(DataComponentTypes.TOOLTIP_STYLE, tooltipStyle);
        }
        return icon;
    }

    /** A picture without any tooltip. */
    public static ItemStack decoration(Key model) {
        ItemStack icon = base(model);
        icon.setData(DataComponentTypes.TOOLTIP_DISPLAY,
                TooltipDisplay.tooltipDisplay().hideTooltip(true).build());
        return icon;
    }

    private static ItemStack base(Key model) {
        ItemStack icon = ItemStack.of(Material.PAPER);
        icon.setData(DataComponentTypes.ITEM_MODEL, model);
        return icon;
    }
}
