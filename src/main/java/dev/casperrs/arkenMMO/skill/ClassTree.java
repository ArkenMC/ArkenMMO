package dev.casperrs.arkenMMO.skill;

import dev.casperrs.arkenMMO.playerclass.PlayerClass;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

/** A class's core skill and its archetypes, in footer tab order. */
public record ClassTree(PlayerClass playerClass, Skill core, List<Archetype> archetypes) {

    /** {@code skills} are in {@link SkillNode} order. */
    public record Archetype(String key, List<Skill> skills) {

        public Skill at(SkillNode node) {
            return skills.get(node.ordinal());
        }
    }

    /** Includes the core skill. */
    public Optional<Skill> find(String id) {
        return Stream.concat(Stream.of(core), archetypes.stream().flatMap(a -> a.skills().stream()))
                .filter(skill -> skill.id().equals(id))
                .findFirst();
    }

    public Archetype archetypeOf(Skill skill) {
        return archetypes.stream()
                .filter(archetype -> archetype.key().equals(skill.archetype()))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException(skill.id() + " has no archetype here"));
    }
}
