package dev.casperrs.arkenMMO.skill;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.tree.LiteralCommandNode;
import dev.casperrs.arkenMMO.text.Messages;
import io.papermc.paper.command.brigadier.CommandSourceStack;
import io.papermc.paper.command.brigadier.Commands;
import org.bukkit.entity.Player;

/** {@code /skills} */
public final class SkillsCommand {

    static final String PERMISSION = "arkenmmo.skills";

    private final SkillMenus menus;
    private final Messages messages;

    public SkillsCommand(SkillMenus menus, Messages messages) {
        this.menus = menus;
        this.messages = messages;
    }

    public LiteralCommandNode<CommandSourceStack> node() {
        return Commands.literal("skills")
                .requires(source -> source.getSender().hasPermission(PERMISSION))
                .executes(context -> {
                    if (context.getSource().getExecutor() instanceof Player player) {
                        menus.request(player);
                    } else {
                        messages.send(context.getSource().getSender(), "skills.chat.players-only");
                    }
                    return Command.SINGLE_SUCCESS;
                })
                .build();
    }
}
