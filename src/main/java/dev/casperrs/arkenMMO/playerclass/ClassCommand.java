package dev.casperrs.arkenMMO.playerclass;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import com.mojang.brigadier.tree.LiteralCommandNode;
import dev.casperrs.arkenMMO.text.Messages;
import io.papermc.paper.command.brigadier.CommandSourceStack;
import io.papermc.paper.command.brigadier.Commands;
import io.papermc.paper.command.brigadier.argument.ArgumentTypes;
import io.papermc.paper.command.brigadier.argument.resolvers.selector.PlayerSelectorArgumentResolver;
import java.util.function.BiConsumer;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

/** {@code /class}, {@code /class select <player>} and {@code /class reset <player>}. */
public final class ClassCommand {

    private static final String SELECT_PERMISSION = "arkenmmo.class.select";
    private static final String RESET_PERMISSION = "arkenmmo.class.reset";
    private static final String PLAYER = "player";

    private final ClassSelection selection;
    private final Messages messages;

    public ClassCommand(ClassSelection selection, Messages messages) {
        this.selection = selection;
        this.messages = messages;
    }

    public LiteralCommandNode<CommandSourceStack> node() {
        return Commands.literal("class")
                .executes(this::openOwn)
                .then(onTarget("select", SELECT_PERMISSION, this::select))
                .then(onTarget("reset", RESET_PERMISSION, this::reset))
                .build();
    }

    private static LiteralArgumentBuilder<CommandSourceStack> onTarget(
            String name, String permission, BiConsumer<CommandSender, Player> handler) {
        return Commands.literal(name)
                .requires(source -> source.getSender().hasPermission(permission))
                .then(Commands.argument(PLAYER, ArgumentTypes.player())
                        .executes(context -> {
                            handler.accept(context.getSource().getSender(), targetOf(context));
                            return Command.SINGLE_SUCCESS;
                        }));
    }

    private static Player targetOf(CommandContext<CommandSourceStack> context) throws CommandSyntaxException {
        return context.getArgument(PLAYER, PlayerSelectorArgumentResolver.class)
                .resolve(context.getSource())
                .getFirst();
    }

    private int openOwn(CommandContext<CommandSourceStack> context) {
        if (context.getSource().getExecutor() instanceof Player player) {
            selection.request(player).ifPresent(current ->
                    messages.send(player, "class.current", selection.classPlaceholder(current)));
        } else {
            messages.send(context.getSource().getSender(), "command.players-only");
        }
        return Command.SINGLE_SUCCESS;
    }

    private void select(CommandSender sender, Player target) {
        TagResolver player = Placeholder.unparsed(PLAYER, target.getName());
        selection.request(target).ifPresentOrElse(
                current -> messages.send(sender, "command.select.has-class",
                        player, selection.classPlaceholder(current)),
                () -> messages.send(sender, "command.select.requested", player));
    }

    private void reset(CommandSender sender, Player target) {
        TagResolver player = Placeholder.unparsed(PLAYER, target.getName());
        selection.reset(target).ifPresentOrElse(
                removed -> messages.send(sender, "command.reset.done",
                        player, selection.classPlaceholder(removed)),
                () -> messages.send(sender, "command.reset.no-class", player));
    }
}
