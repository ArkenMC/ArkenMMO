package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.menu.Menu;
import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.function.BiConsumer;
import java.util.function.Predicate;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

/** One archetype's tree page. Changes redraw the open menu; it only reopens when its title changes. */
final class TreeScreen {

    // Footer slots, painted into the titles
    private static final int BACK = 45;
    private static final int FIRST_TAB = 46;
    private static final int RESET = 49;
    private static final int SCROLL_UP = 50;
    private static final int SCROLL_DOWN = 51;
    private static final int LOADOUT = 52;
    private static final int INFO = 53;
    private static final int CORE = 0;

    private record Page(SkillSession session, Menu menu, String titleKey) {
    }

    private final SkillContext context;
    private final BiConsumer<Player, SkillSession> openLoadout;

    TreeScreen(SkillContext context, BiConsumer<Player, SkillSession> openLoadout) {
        this.context = context;
        this.openLoadout = openLoadout;
    }

    void open(Player player, SkillSession session) {
        ClassSkills skills = context.book().get(player, session.tree);
        String titleKey = titleKey(session, skills);
        Page page = new Page(session, new Menu(context.messages().get(titleKey)), titleKey);
        page.menu().onOtherClick(context.guarded(session, viewer -> {
            if (session.hasSelection()) {
                session.clearSelection();
                refresh(viewer, page);
            }
        }));
        render(page, skills);
        page.menu().open(player);
    }

    private void refresh(Player player, Page page) {
        ClassSkills skills = context.book().get(player, page.session().tree);
        if (titleKey(page.session(), skills).equals(page.titleKey())) {
            render(page, skills);
        } else {
            open(player, page.session());
        }
    }

    private static String titleKey(SkillSession session, ClassSkills skills) {
        ClassTree.Archetype archetype = session.archetype();
        Predicate<SkillNode> owned = node -> skills.owned().contains(archetype.at(node).id());
        return "skills.titles.tree_" + session.tree.playerClass().id() + "_" + archetype.key()
                + "_" + session.view.titleSuffix(owned);
    }

    private void render(Page page, ClassSkills skills) {
        renderStones(page, skills);
        renderLinks(page, skills);
        renderFooter(page, skills);
    }

    private void renderStones(Page page, ClassSkills skills) {
        SkillSession session = page.session();
        session.view.nodeSlots().forEach((node, slot) -> {
            Skill skill = session.archetype().at(node);
            page.menu().button(slot, stone(session, skills, skill),
                    context.guarded(session, viewer -> clickStone(viewer, page, skill)));
        });
        if (session.view == TreeView.UPPER) {
            page.menu().item(CORE, context.items().skill(session.tree.core(), SkillItems.Look.OWNED,
                    false, null, status("core")));
        }
        PlayerClass playerClass = session.tree.playerClass();
        for (int slot : session.view.sealedSlots()) {
            page.menu().item(slot, context.items().painted(playerClass, "skills.menu.sealed",
                    Placeholder.component("archetype",
                            context.items().archetypeName(playerClass, session.archetype().key()))));
        }
    }

    private void renderLinks(Page page, ClassSkills skills) {
        SkillSession session = page.session();
        ClassTree.Archetype archetype = session.archetype();
        for (TreeView.Link link : session.view.links()) {
            boolean lit = skills.owned().contains(archetype.at(link.from()).id())
                    && skills.owned().contains(archetype.at(link.to()).id());
            for (TreeView.Piece piece : link.pieces()) {
                if (lit) {
                    page.menu().item(piece.slot(),
                            context.items().connector(session.tree.playerClass(), piece.shape()));
                } else {
                    page.menu().clear(piece.slot());
                }
            }
        }
    }

    private ItemStack stone(SkillSession session, ClassSkills skills, Skill skill) {
        if (TreeRules.owns(session.tree, skills.owned(), skill)) {
            return ownedStone(session, skills, skill);
        }
        Set<TreeRules.Gate> missing = context.book().missing(session.tree, skills, skill);
        if (!missing.isEmpty()) {
            List<Component> text = new ArrayList<>(status("locked"));
            missing.forEach(gate -> text.addAll(requirement(session, skills, skill, gate)));
            return context.items().skill(skill, SkillItems.Look.LOCKED, true, null, text);
        }
        return skill.equals(session.confirming)
                ? context.items().skill(skill, SkillItems.Look.CONFIRM, true, null, status("confirm"))
                : context.items().skill(skill, SkillItems.Look.AVAILABLE, true, null, status("available"));
    }

    private ItemStack ownedStone(SkillSession session, ClassSkills skills, Skill skill) {
        SkillItems items = context.items();
        if (!session.boughtNow.contains(skill.id())) {
            return items.skill(skill, SkillItems.Look.OWNED, false, null, status("owned"));
        }
        Optional<Skill> blocking = context.book().blocking(session.tree, skills, skill);
        if (blocking.isPresent()) {
            return items.skill(skill, SkillItems.Look.OWNED, false, null, status("undo-refused",
                    Placeholder.component("blocking", items.skillName(blocking.get()))));
        }
        return skill.equals(session.confirming)
                ? items.skill(skill, SkillItems.Look.CONFIRM, false, null,
                        status("undo-confirm", SkillItems.number("cost", skill.node().cost())))
                : items.skill(skill, SkillItems.Look.OWNED, false, null, status("undoable"));
    }

    private List<Component> status(String key, TagResolver... resolvers) {
        return context.messages().getList("skills.hover.status." + key, resolvers);
    }

    private List<Component> requirement(SkillSession session, ClassSkills skills, Skill skill, TreeRules.Gate gate) {
        String base = "skills.hover.requirements.";
        return switch (gate) {
            case LEVEL -> context.messages().getList(base + "level",
                    SkillItems.number("level", skill.node().requiredLevel()));
            case POINTS -> context.messages().getList(base + "points",
                    SkillItems.number("free", context.book().freePoints(session.tree, skills)));
            case CONNECTION -> {
                // Only the entry node has no links, and it is never unconnected
                List<Component> names = skill.node().links().stream()
                        .map(link -> context.items().skillName(session.archetype().at(link)))
                        .toList();
                yield names.size() == 1
                        ? context.messages().getList(base + "one-skill",
                                Placeholder.component("required", names.getFirst()))
                        : context.messages().getList(base + "either-skill",
                                Placeholder.component("required_a", names.get(0)),
                                Placeholder.component("required_b", names.get(1)));
            }
        };
    }

    private void clickStone(Player player, Page page, Skill skill) {
        SkillSession session = page.session();
        boolean second = skill.equals(session.confirming);
        session.clearSelection();
        ClassSkills skills = context.book().get(player, session.tree);
        boolean undo = session.boughtNow.contains(skill.id())
                && context.book().canRefund(session.tree, skills, skill);
        if (undo || context.book().canBuy(session.tree, skills, skill)) {
            if (!second) {
                session.confirming = skill;
            } else if (undo) {
                if (context.book().refund(player, session.tree, skill)) {
                    session.boughtNow.remove(skill.id());
                }
            } else if (context.book().buy(player, session.tree, skill)) {
                session.boughtNow.add(skill.id());
            }
        }
        refresh(player, page);
    }

    private void renderFooter(Page page, ClassSkills skills) {
        SkillSession session = page.session();
        PlayerClass playerClass = session.tree.playerClass();
        SkillItems items = context.items();
        Menu menu = page.menu();

        menu.button(BACK, items.painted(playerClass, "skills.menu.close"),
                context.guarded(session, Player::closeInventory));
        List<ClassTree.Archetype> archetypes = session.tree.archetypes();
        for (int index = 0; index < archetypes.size(); index++) {
            ClassTree.Archetype archetype = archetypes.get(index);
            int tab = index;
            menu.button(FIRST_TAB + index,
                    items.tab(playerClass, archetype.key(),
                            index == session.archetype ? "skills.menu.tab-open" : "skills.menu.tab",
                            TreeRules.spent(archetype, skills.owned())),
                    context.guarded(session, viewer -> showTab(viewer, page, tab)));
        }
        menu.button(RESET, resetButton(session, skills),
                context.guarded(session, viewer -> clickReset(viewer, page)));
        scrollButton(page, SCROLL_UP, TreeView.UPPER, "skills.menu.scroll-up");
        scrollButton(page, SCROLL_DOWN, TreeView.LOWER, "skills.menu.scroll-down");
        menu.button(LOADOUT, items.painted(playerClass, "skills.menu.loadout"),
                context.guarded(session, viewer -> {
                    session.clearSelection();
                    openLoadout.accept(viewer, session);
                }));
        menu.item(INFO, infoItem(session, skills));
    }

    private void showTab(Player player, Page page, int tab) {
        SkillSession session = page.session();
        boolean selected = session.hasSelection();
        session.clearSelection();
        if (tab != session.archetype) {
            session.archetype = tab;
            session.view = TreeView.UPPER;
            open(player, session);
        } else if (selected) {
            refresh(player, page);
        }
    }

    /** The arrow toward the view already shown is painted as unusable and does nothing. */
    private void scrollButton(Page page, int slot, TreeView target, String textKey) {
        SkillSession session = page.session();
        if (session.view == target) {
            page.menu().clear(slot);
            return;
        }
        page.menu().button(slot, context.items().painted(session.tree.playerClass(), textKey),
                context.guarded(session, viewer -> {
                    session.clearSelection();
                    session.view = target;
                    open(viewer, session);
                }));
    }

    private ItemStack resetButton(SkillSession session, ClassSkills skills) {
        PlayerClass playerClass = session.tree.playerClass();
        if (!context.book().canReset(skills)) {
            long wait = context.book().resetWaitSeconds(skills);
            return context.items().described(playerClass, "gui/button/reset_unavailable",
                    wait > 0 ? "skills.menu.reset-cooldown" : "skills.menu.reset-empty",
                    SkillItems.number("seconds", wait));
        }
        String model = session.confirmingReset ? "gui/button/reset_confirm" : "gui/button/reset";
        return context.items().described(playerClass, model,
                session.confirmingReset ? "skills.menu.reset-confirm" : "skills.menu.reset",
                SkillItems.number("points", TreeRules.spent(session.tree, skills.owned())),
                SkillItems.number("cooldown", SkillBook.RESET_COOLDOWN.toSeconds()));
    }

    private void clickReset(Player player, Page page) {
        SkillSession session = page.session();
        boolean second = session.confirmingReset;
        session.clearSelection();
        if (context.book().canReset(context.book().get(player, session.tree))) {
            if (!second) {
                session.confirmingReset = true;
            } else if (context.book().reset(player, session.tree)) {
                session.boughtNow.clear();
            }
        }
        refresh(player, page);
    }

    private ItemStack infoItem(SkillSession session, ClassSkills skills) {
        PlayerClass playerClass = session.tree.playerClass();
        TagResolver.Builder resolvers = TagResolver.builder()
                .resolver(Placeholder.component("class", context.items().className(playerClass)))
                .resolver(SkillItems.number("level", context.book().level()))
                .resolver(SkillItems.number("max_level", SkillSettings.MAX_LEVEL))
                .resolver(SkillItems.number("free", context.book().freePoints(session.tree, skills)));
        int number = 1;
        for (ClassTree.Archetype archetype : session.tree.archetypes()) {
            resolvers.resolver(Placeholder.component("archetype_" + number,
                    context.items().archetypeName(playerClass, archetype.key())));
            resolvers.resolver(SkillItems.number("spent_" + number,
                    TreeRules.spent(archetype, skills.owned())));
            number++;
        }
        return context.items().painted(playerClass, "skills.menu.info", resolvers.build());
    }
}
