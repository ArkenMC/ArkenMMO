package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.menu.Menu;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.List;
import java.util.Optional;
import java.util.function.BiConsumer;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

/** Puts owned actives on the combo slots: pick a skill, then click a slot. */
final class LoadoutScreen {

    // Painted into the titles
    private static final int[] SEATS = {10, 12, 14, 16};
    private static final int FIRST_POOL = 27;
    private static final int CORE = 40;
    private static final int BACK = 45;
    private static final int INFO = 53;
    private static final List<String> COMBOS = List.of("R-L-R", "R-R-R", "R-L-L", "R-R-L");
    private static final List<String> ARCHER_COMBOS = List.of("L-R-L", "L-L-L", "L-R-R", "L-L-R");

    private final SkillContext context;
    private final BiConsumer<Player, SkillSession> openTree;

    LoadoutScreen(SkillContext context, BiConsumer<Player, SkillSession> openTree) {
        this.context = context;
        this.openTree = openTree;
    }

    void open(Player player, SkillSession session) {
        PlayerClass playerClass = session.tree.playerClass();
        Menu menu = new Menu(context.messages().get("skills.titles.loadout_" + playerClass.id()));
        menu.onOtherClick(context.guarded(session, viewer -> {
            if (session.hasSelection()) {
                session.clearSelection();
                render(viewer, session, menu);
            }
        }));
        menu.button(BACK, context.items().painted(playerClass, "skills.menu.back"),
                context.guarded(session, viewer -> {
                    session.clearSelection();
                    openTree.accept(viewer, session);
                }));
        menu.item(INFO, context.items().painted(playerClass, "skills.menu.loadout-info"));
        render(player, session, menu);
        menu.open(player);
    }

    private void render(Player player, SkillSession session, Menu menu) {
        ClassSkills skills = context.book().get(player, session.tree);
        for (int seat = 0; seat < SEATS.length; seat++) {
            int index = seat;
            menu.button(SEATS[seat], seatItem(session, skills, seat),
                    context.guarded(session, viewer -> clickSeat(viewer, session, menu, index)));
        }
        List<Skill> pool = session.tree.archetypes().stream()
                .flatMap(archetype -> archetype.skills().stream())
                .filter(Skill::active)
                .toList();
        for (int index = 0; index < pool.size(); index++) {
            poolStone(session, skills, menu, FIRST_POOL + index, pool.get(index));
        }
        poolStone(session, skills, menu, CORE, session.tree.core());
    }

    private ItemStack seatItem(SkillSession session, ClassSkills skills, int seat) {
        PlayerClass playerClass = session.tree.playerClass();
        String combo = combo(playerClass, seat);
        Optional<Skill> assigned = skills.loadout().at(seat).flatMap(session.tree::find);
        TagResolver picked = Placeholder.component("picked", session.picked == null
                ? Component.empty() : context.items().skillName(session.picked));
        if (assigned.isPresent()) {
            return context.items().skill(assigned.get(), SkillItems.Look.OWNED, false, combo,
                    status(session.picked == null ? "seat" : "seat-picked", picked));
        }
        return context.items().painted(playerClass,
                session.picked == null ? "skills.menu.seat-empty" : "skills.menu.seat-empty-picked",
                Placeholder.unparsed("combo", combo), picked);
    }

    private void poolStone(SkillSession session, ClassSkills skills, Menu menu, int slot, Skill skill) {
        boolean owned = TreeRules.owns(session.tree, skills.owned(), skill);
        boolean picked = skill.equals(session.picked);
        int seat = skills.loadout().seats().indexOf(skill.id());
        String key = !owned ? "pool-locked" : picked ? "pool-picked" : seat >= 0 ? "pool-assigned" : "pool-free";
        SkillItems.Look look = !owned ? SkillItems.Look.LOCKED
                : picked ? SkillItems.Look.CONFIRM : SkillItems.Look.OWNED;
        TagResolver combo = Placeholder.unparsed("combo",
                seat >= 0 ? combo(session.tree.playerClass(), seat) : "");
        menu.button(slot, context.items().skill(skill, look, false, null, status(key, combo)),
                context.guarded(session, viewer -> clickPool(viewer, session, menu, skill)));
    }

    private List<Component> status(String key, TagResolver resolver) {
        return context.messages().getList("skills.hover.loadout." + key, resolver);
    }

    private void clickPool(Player player, SkillSession session, Menu menu, Skill skill) {
        boolean owned = TreeRules.owns(session.tree, context.book().get(player, session.tree).owned(), skill);
        session.picked = owned && !skill.equals(session.picked) ? skill : null;
        render(player, session, menu);
    }

    private void clickSeat(Player player, SkillSession session, Menu menu, int seat) {
        ClassSkills skills = context.book().get(player, session.tree);
        Skill picked = session.picked;
        session.picked = null;
        if (picked == null) {
            context.book().saveLoadout(player, session.tree, skills.loadout().clear(seat));
        } else if (TreeRules.owns(session.tree, skills.owned(), picked)) {
            context.book().saveLoadout(player, session.tree, skills.loadout().assign(seat, picked.id()));
        }
        render(player, session, menu);
    }

    private static String combo(PlayerClass playerClass, int seat) {
        return (playerClass == PlayerClass.ARCHER ? ARCHER_COMBOS : COMBOS).get(seat);
    }
}
