---
name: skills-stage-verified
description: Skills stage research (2026-11-26) - MythicMobs/PlaceholderAPI 26.3, skill tree GUI/art, casting input; where notes are, URLs, dead ends
metadata:
  type: reference
---
Full write-ups (don't re-research): docs/research/skills-integrations.md, skill-tree-gui.md, skill-tree-art.md, casting-input-sources.md. Older: [[gui-263-verified]], [[gui-sources]].

## Key facts
- VOLATILE: MythicMobs 5.14.0 (2026-10-30) lists 26.3; PlaceholderAPI 2.12.3 (2026-07-03) lists 26.3 and now needs `_` after identifier.
- Maven: io.lumine:Mythic-Dist:5.14.0 @ https://mvn.lumine.io/repository/maven-public/ ; me.clip:placeholderapi:2.12.3 @ https://repo.helpch.at/releases/
- Mythic online Javadocs are old (5.4.0-SNAPSHOT). Neither vendor documents thread safety.
- Paper plugin deps default required=true, join-classpath=true, load=OMIT.
- Open: return values of %arken_party_has_x% (ArkenCore); PAPI default booleans yes/no; user approval for PAPI compile dependency.
- composite models draw in list order; item/generated layer0..4, higher on top (NeoForge docs, not wiki).
- Warrior tree n1-n6: 17 legal owned sets per branch.

## URLs (checked 2026-11-26; format URL | confirmed | stability)
- https://hangar.papermc.io/Lumine/MythicMobs/versions | version/MC table | volatile
- https://api.modrinth.com/v2/project/{mythicmobs,placeholderapi}/version?game_versions=%5B%2226.3%22%5D | dates, versions (works better than the HTML page) | volatile
- https://wiki.mythiccraft.io/mythicmobs/API | repo, events table, isMythicMob example | stable
- https://mvn.lumine.io/repository/maven-public/io/lumine/Mythic-Dist/maven-metadata.xml | release 5.14.0 | volatile
- https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/ (bukkit/events/MythicMobDeathEvent, core/mobs/MobExecutor, core/mobs/ActiveMob, api/mobs/MythicMob .html) | signatures | stable
- https://wiki.placeholderapi.com/developers/using-placeholderapi/ | repo, paper-plugin.yml | stable
- https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/java/me/clip/placeholderapi/replacer/CharsReplacer.java (+ PlaceholderAPI.java, resources/config.yml) | parsing, fallback, booleans | stable
- https://repo.extendedclip.com/releases/me/clip/placeholderapi/maven-metadata.xml | 2.12.3 | volatile
- https://docs.papermc.io/paper/dev/getting-started/paper-plugins/ | dependency defaults | stable
- https://docs.neoforged.net/docs/resources/client/models/ and /items | layer and composite order | stable
- https://docs.phoenixdevt.fr/mmocore/features/skill-trees.html | chest tree states/paths | stable
- https://treeapp.io/wiki/how-nodes-are-rendered/ ; https://nathanielinman.com/ability-icon-user-experience/ | node states, icon rules (weak) | stable
- https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/ ; https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | colour, 3:1 | stable
- https://en.wikipedia.org/wiki/Runes ; /Runestone | stave shapes, paint, bands (first 100k only) | stable
- https://www.digital-epigraphy.com/tutorials/lets-talk-about-sun-and-shadow-a-fundamental-update-on-drawing-drop-shadow-transitions-in-photoshop | sunk relief lighting reversed | stable
- https://www.adl.org/resources/hate-symbol/othala-rune | appropriated rune | stable
- https://jd.papermc.io/paper/26.3/ PlayerInteractEvent, PlayerArmSwingEvent, PlayerStopUsingItemEvent, EntityShootBowEvent | casting | stable
- https://github.com/Vontus/MagicBottle/issues/34 | drop causes LEFT_CLICK_AIR | stable
- https://minecraft.wiki/w/Bow | draw/release/arrow need | stable

## Dead ends
icy-veins talent guide (403), hub.spigotmc.org SPIGOT-5632 (403), wiki.placeholderapi.com/users/faq (404), slynyrd 2018 pixelblog-6 (404), slynyrd pixelblog-13-rocks (no rules in text), minecraft.net 26.3 article (timeout), Dota2CharacterTextureGuide.pdf (only a redirect notice), Mythic-Dist/PAPI POM fetches show no dependencies section, misode versions page (empty). No studio skill-icon guide found by search.
