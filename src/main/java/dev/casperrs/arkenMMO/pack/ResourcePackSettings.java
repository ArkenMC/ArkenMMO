package dev.casperrs.arkenMMO.pack;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.logging.Logger;
import java.util.regex.Pattern;
import org.bukkit.configuration.ConfigurationSection;
import org.jetbrains.annotations.Nullable;

/** The validated {@code resource-pack} section of {@code config.yml}. */
public record ResourcePackSettings(UUID id, URI url, String sha1) {

    private static final Pattern SHA1 = Pattern.compile("[0-9a-fA-F]{40}");

    /** Empty when the pack is switched off or incomplete; the reason is logged here. */
    public static Optional<ResourcePackSettings> read(ConfigurationSection config, Logger logger) {
        if (!config.getBoolean("resource-pack.enabled")) {
            logger.info("resource-pack.enabled is false: ArkenMMO sends no pack. The menu art must come from "
                    + "another one, such as the ItemsAdder pack.");
            return Optional.empty();
        }
        List<String> invalid = new ArrayList<>();
        URI url = parseUrl(text(config, "url"));
        if (url == null) {
            invalid.add("url (needs an http or https address)");
        }
        String sha1 = text(config, "sha1");
        if (!SHA1.matcher(sha1).matches()) {
            invalid.add("sha1 (needs 40 hex characters)");
        }
        UUID id = parseId(text(config, "id"));
        if (id == null) {
            invalid.add("id (needs a UUID)");
        }
        if (!invalid.isEmpty()) {
            logger.warning("No resource pack is sent, fix these resource-pack settings in config.yml: "
                    + String.join(", ", invalid));
            return Optional.empty();
        }
        return Optional.of(new ResourcePackSettings(id, url, sha1));
    }

    // No explicit fallback in getString: that would hide the defaults bundled in the jar
    private static String text(ConfigurationSection config, String key) {
        return Objects.requireNonNullElse(config.getString("resource-pack." + key), "").trim();
    }

    private static @Nullable URI parseUrl(String text) {
        try {
            URI url = new URI(text);
            boolean web = "http".equalsIgnoreCase(url.getScheme()) || "https".equalsIgnoreCase(url.getScheme());
            return web && url.getHost() != null ? url : null;
        } catch (URISyntaxException e) {
            return null;
        }
    }

    private static @Nullable UUID parseId(String text) {
        try {
            return UUID.fromString(text);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
