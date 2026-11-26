package dev.casperrs.arkenMMO.skill;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.Objects;
import net.kyori.adventure.text.minimessage.tag.resolver.Placeholder;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

/** Each skill's numbers from {@code skill-values.yml}, with the bundled file as fallback. */
public final class SkillValues {

    private static final String FILE_NAME = "skill-values.yml";

    private final YamlConfiguration yaml;

    private SkillValues(YamlConfiguration yaml) {
        this.yaml = yaml;
    }

    public static SkillValues load(JavaPlugin plugin) {
        File file = new File(plugin.getDataFolder(), FILE_NAME);
        if (!file.exists()) {
            plugin.saveResource(FILE_NAME, false);
        }
        YamlConfiguration yaml = YamlConfiguration.loadConfiguration(file);
        try (Reader bundled = new InputStreamReader(
                Objects.requireNonNull(plugin.getResource(FILE_NAME)), StandardCharsets.UTF_8)) {
            yaml.setDefaults(YamlConfiguration.loadConfiguration(bundled));
        } catch (IOException e) {
            throw new UncheckedIOException("Could not read the bundled " + FILE_NAME, e);
        }
        return new SkillValues(yaml);
    }

    /** The number at a path such as {@code warrior.cleave.damage}; 0 if neither file has one. */
    public double number(String path) {
        return yaml.getDouble(path);
    }

    /** One placeholder per number of the skill, named like its key. */
    TagResolver placeholders(Skill skill) {
        String path = skill.playerClass().id() + "." + skill.key();
        TagResolver.Builder resolvers = TagResolver.builder();
        // Both are needed: a section the admin changed hides the bundled keys it leaves out
        addAll(resolvers, yaml.getDefaults() == null ? null : yaml.getDefaults().getConfigurationSection(path));
        addAll(resolvers, yaml.getConfigurationSection(path));
        return resolvers.build();
    }

    private static void addAll(TagResolver.Builder resolvers, ConfigurationSection section) {
        if (section != null) {
            section.getValues(false).forEach((key, value) ->
                    resolvers.resolver(Placeholder.unparsed(key, String.valueOf(value))));
        }
    }
}
