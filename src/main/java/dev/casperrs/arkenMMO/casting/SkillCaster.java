package dev.casperrs.arkenMMO.casting;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import dev.casperrs.arkenMMO.skill.ClassSkills;
import dev.casperrs.arkenMMO.skill.ClassTree;
import dev.casperrs.arkenMMO.skill.Skill;
import dev.casperrs.arkenMMO.skill.SkillBook;
import dev.casperrs.arkenMMO.skill.SkillCatalog;
import dev.casperrs.arkenMMO.skill.SkillValues;
import dev.casperrs.arkenMMO.skill.TreeRules;
import dev.casperrs.arkenMMO.sound.SoundService;
import dev.casperrs.arkenMMO.text.Messages;
import java.util.Map;
import java.util.Optional;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.entity.Player;

/**
 * Casts the skill on a loadout slot: checks it, takes mana, starts the cooldown and runs its action.
 * A failed cast costs nothing and says why. Main thread only.
 */
public final class SkillCaster {

    private static final long LINE_MILLIS = 2000;

    private final SkillBook book;
    private final SkillValues values;
    private final Casters casters;
    private final CastingHud hud;
    private final SoundService sounds;
    private final Messages messages;
    private final Map<String, SkillAction> actions;

    /** {@code actions} are keyed by skill ID; skills without one can't be cast yet. */
    public SkillCaster(SkillBook book, SkillValues values, Casters casters, CastingHud hud, SoundService sounds,
                       Messages messages, Map<String, SkillAction> actions) {
        this.book = book;
        this.values = values;
        this.casters = casters;
        this.hud = hud;
        this.sounds = sounds;
        this.messages = messages;
        this.actions = Map.copyOf(actions);
    }

    /** {@code slot} is 1-4; {@code combo} fills the click placeholders of the success line. */
    void cast(Player player, PlayerClass playerClass, int slot, TagResolver combo) {
        ClassTree tree = SkillCatalog.of(playerClass);
        ClassSkills skills = book.get(player, tree);
        Optional<Skill> seated = skills.loadout().at(slot - 1).flatMap(tree::find);
        if (seated.isEmpty()) {
            fail(player, "empty", Placeholder.unparsed("slot", Integer.toString(slot)));
            return;
        }
        Skill skill = seated.get();
        TagResolver name = Placeholder.component("skill",
                messages.get("skills.list." + playerClass.id() + "." + skill.key() + ".name"));
        SkillAction action = actions.get(skill.id());
        if (!TreeRules.owns(tree, skills.owned(), skill)) {
            fail(player, "not-owned", name);
        } else if (!skill.active()) {
            fail(player, "passive", name);
        } else if (action == null) {
            fail(player, "unavailable", name);
        } else {
            payAndPerform(player, skill.id(), action, name, combo);
        }
    }

    private void payAndPerform(Player player, String skillId, SkillAction action, TagResolver name,
                               TagResolver combo) {
        CasterState state = casters.of(player);
        long now = Casters.now();
        long wait = state.cooldownLeft(skillId, now);
        if (wait > 0) {
            fail(player, "cooldown", name, number("seconds", Math.ceilDiv(wait, 1000L)));
            return;
        }
        double cost = state.cost(skillId, values.number(skillId + ".mana"), now);
        if (state.mana(now) < cost) {
            fail(player, "mana", name, number("cost", (long) Math.ceil(cost)));
            return;
        }
        Optional<Runnable> performance = action.prepare(player);
        if (performance.isEmpty()) {
            fail(player, "no-target", name);
            return;
        }
        state.cast(skillId, cost, Math.round(values.number(skillId + ".cooldown") * 1000), now);
        hud.show(player, messages.get("casting.cast", combo, name), LINE_MILLIS);
        performance.get().run();
    }

    private void fail(Player player, String reason, TagResolver... resolvers) {
        sounds.playTo(player, "cast_fail");
        hud.show(player, messages.get("casting.fail." + reason, resolvers), LINE_MILLIS);
    }

    private static TagResolver number(String name, long value) {
        return Placeholder.unparsed(name, Long.toString(value));
    }
}
