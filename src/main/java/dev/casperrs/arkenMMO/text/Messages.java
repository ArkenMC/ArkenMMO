package dev.casperrs.arkenMMO.text;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Objects;
import net.kyori.adventure.audience.Audience;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.MiniMessage;
import net.kyori.adventure.text.minimessage.tag.resolver.TagResolver;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

/** Player-facing text from {@code messages.yml}, with the bundled file as fallback for missing keys. */
public final class Messages {

    private static final String FILE_NAME = "messages.yml";
    private static final MiniMessage MINI_MESSAGE = MiniMessage.miniMessage();

    private final YamlConfiguration yaml;

    private Messages(YamlConfiguration yaml) {
        this.yaml = yaml;
    }

    public static Messages load(JavaPlugin plugin) {
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
        return new Messages(yaml);
    }

    public Component get(String key, TagResolver... resolvers) {
        return parse(Objects.requireNonNullElse(yaml.getString(key), key), resolvers);
    }

    public List<Component> getList(String key, TagResolver... resolvers) {
        return yaml.getStringList(key).stream().map(line -> parse(line, resolvers)).toList();
    }

    public void send(Audience audience, String key, TagResolver... resolvers) {
        audience.sendMessage(get(key, resolvers));
    }

    private static Component parse(String text, TagResolver... resolvers) {
        return MINI_MESSAGE.deserialize(text, resolvers);
    }
}
