# Skills stage: MythicMobs and PlaceholderAPI on Paper 26.3

## Target version
**Paper 26.3** (`pom.xml`: `paper-api 26.3.build.205-stable`). Checked 2026-11-26. Compatibility facts are **volatile**.

Tags: **[V]** read in an official source (listing, vendor wiki, repository, source code), **[J]** read in Mythic's online Javadocs, which are old (header says **5.4.0-SNAPSHOT**), **[U]** unverified.

## Summary
1. Both plugins list 26.3: **MythicMobs 5.14.0** and **PlaceholderAPI 2.12.3** [V]. A listing is not an in-game test [U]; there is no test server.
2. Compile against `io.lumine:Mythic-Dist:5.14.0` and `me.clip:placeholderapi:2.12.3`, both `provided`. Declare both as optional in `paper-plugin.yml`.
3. XP: read the Mythic **internal name** when the mob is first damaged, cache it, and award XP from **one** path (`EntityDeathEvent` plus our contribution ledger).
4. Party: `setPlaceholders(viewer, "%arken_party_has_<name>%")`; ally only on an exact "true" value. **The values ArkenCore returns are unknown** [U].
5. Isolate each plugin's imports in one class behind a small interface. Call both on the main thread.

## Version notes
| Plugin | Latest release | Listed Minecraft versions | Source |
|---|---|---|---|
| MythicMobs | 5.14.0, 2026-10-30 | 1.21.4 to 26.3 (Modrinth; Hangar says 1.21.1 to 26.3). 5.13.0 stops at 26.2 | [Hangar](https://hangar.papermc.io/Lumine/MythicMobs/versions), [Modrinth API](https://api.modrinth.com/v2/project/mythicmobs/version?game_versions=%5B%2226.3%22%5D) |
| PlaceholderAPI | 2.12.3, 2026-07-03 | up to 26.3 (listing metadata) | [Modrinth API](https://api.modrinth.com/v2/project/placeholderapi/version?game_versions=%5B%2226.3%22%5D) |

- The server needs MythicMobs **5.14.0 or newer** on 26.3.
- 2.12.3 changelog: `setPlaceholders` now **requires an underscore after the identifier** [V]. `%arken_party_has_Name%` qualifies.
- I found no 26.3 bug report for MythicMobs 5.14.0 by web search. I did not search its issue tracker directly [U].

## Pack file layout
Not applicable.

## Plugin side

### Dependencies
**Approval:** the user's decisions approve MythicMobs as an optional compile-time dependency. They do not say the same for **PlaceholderAPI**. The orchestrator should confirm it with the user before `pom.xml` changes.

```xml
<repository>
    <id>lumine</id>
    <url>https://mvn.lumine.io/repository/maven-public/</url>
</repository>
<repository>
    <id>placeholderapi</id>
    <url>https://repo.helpch.at/releases/</url>
</repository>

<dependency>
    <groupId>io.lumine</groupId>
    <artifactId>Mythic-Dist</artifactId>
    <version>5.14.0</version>
    <scope>provided</scope>
</dependency>
<dependency>
    <groupId>me.clip</groupId>
    <artifactId>placeholderapi</artifactId>
    <version>2.12.3</version>
    <scope>provided</scope>
</dependency>
```
- Mythic repository and artifact [V] ([API wiki](https://wiki.mythiccraft.io/mythicmobs/API), whose example still says 5.12.1). 5.14.0 is the `release` in the [repository metadata](https://mvn.lumine.io/repository/maven-public/io/lumine/Mythic-Dist/maven-metadata.xml) [V].
- PlaceholderAPI repository [V] ([developer page](https://wiki.placeholderapi.com/developers/using-placeholderapi/); it also names `https://repo.extendedclip.com/releases/` for Gradle). Both report 2.12.3 as latest.
- The fetch tool showed no `<dependencies>` in either POM, so no exclusions should be needed [U until `mise run build`].
- Pin release versions, not `-SNAPSHOT`. CI must be able to reach both repositories.

### paper-plugin.yml
`required` and `join-classpath` default to **true**, and `load` defaults to `OMIT`, which gives undefined order [V] ([Paper plugins](https://docs.papermc.io/paper/dev/getting-started/paper-plugins/)). So write all three:
```yaml
dependencies:
  server:
    MythicMobs:
      load: BEFORE
      required: false
      join-classpath: true
    PlaceholderAPI:
      load: BEFORE
      required: false
      join-classpath: true
```
`load: BEFORE` means the dependency loads before us [V]. Do **not** add ArkenCore: we never call it directly.

### When a plugin is absent
- Put all `io.lumine.*` imports in one class and all `me.clip.*` imports in another. Main code sees only small interfaces. Construct an implementation only after `Bukkit.getPluginManager().isPluginEnabled(...)` is true. Otherwise the JVM may throw `NoClassDefFoundError` (project rule in `docs/integrations.md`).
- Do not put their types in fields, method signatures or `@EventHandler` parameters of classes that always load.

| Missing | Behaviour |
|---|---|
| MythicMobs | every mob uses the vanilla XP table |
| PlaceholderAPI | allies are only the player and their companions (user decision) |
| ArkenCore (PAPI present) | no `arken` expansion, so the placeholder comes back **unchanged** [V], which is "not an ally" |

Suggested shape (names are free):
```java
interface MobKinds { Optional<String> mythicType(Entity entity); }   // empty = not a Mythic mob
interface PartyLookup { boolean inParty(Player viewer, Player other); }
```

### (a) XP per MythicMob
API:

| Call | Evidence |
|---|---|
| `MythicBukkit.inst().getMobManager().isMythicMob(Entity)` | wiki example [V] |
| `MythicBukkit.inst().getMobManager().getActiveMob(UUID)` returns `Optional<ActiveMob>` | [J] [MobExecutor](https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/core/mobs/MobExecutor.html) |
| `ActiveMob#getType()` returns `MythicMob`; `MythicMob#getInternalName()` | [J] [ActiveMob](https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/core/mobs/ActiveMob.html), [MythicMob](https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/api/mobs/MythicMob.html) |
| `io.lumine.mythic.bukkit.events.MythicMobDeathEvent`: `getEntity()`, `getMobType()` (a `MythicMob`), `getMobLevel()`, `getKiller()`, `getDrops()` | [J] [event](https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/bukkit/events/MythicMobDeathEvent.html); the wiki lists it as not cancellable [V] |

Packages from the Javadocs: `MythicBukkit` in `io.lumine.mythic.bukkit`, `ActiveMob` in `io.lumine.mythic.core.mobs`, `MythicMob` in `io.lumine.mythic.api.mobs`. The compiler is the final check against 5.14.0. Tutorials using `io.lumine.xikage...` are obsolete.

```java
return MythicBukkit.inst().getMobManager()
        .getActiveMob(entity.getUniqueId())
        .map(mob -> mob.getType().getInternalName());
```

**Recommended design** (a design choice, not a Mythic rule):
- A Mythic mob is also a Bukkit entity, so using both `MythicMobDeathEvent` and `EntityDeathEvent` risks **double XP**. Use only `EntityDeathEvent`.
- Whether Mythic still has the `ActiveMob` registered when our death handler runs depends on listener order [U]. So look the type up when the contribution ledger first records damage on the entity, and store it in the ledger entry. No contribution means no XP anyway.
- Then `MythicMobDeathEvent` is not needed.
- Config: XP by Mythic internal name (case-sensitive match is safest [U]) and by vanilla entity type. Proposed rule for an unlisted Mythic mob: use its vanilla entity type's value; an entry of 0 turns XP off. Confirm in the brief.
- `getKiller()` can name only one player, and our split uses the ledger, so do not rely on it.
- `getMobLevel()` is not needed (XP is per type). The Javadoc contradicts itself on its type (`double` signature, "int" text).
- Mythic mobs removed by a Mythic mechanic without dying give no death event, so no XP [U].
- **Spawners:** check the entity's Paper spawn reason for vanilla and trial spawners (not re-checked here; confirm at compile time). Whether mobs from **MythicMobs' own spawners** can be told apart is [U]. An admin can give those mob types 0 XP.

### (b) `%arken_party_has_<name>%`
```java
String result = PlaceholderAPI.setPlaceholders(viewer, "%arken_party_has_" + other.getName() + "%");
```
- Signature: `setPlaceholders(Player player, String text)` and an `OfflinePlayer` overload [V] ([source](https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/java/me/clip/placeholderapi/PlaceholderAPI.java), master branch). `viewer` is the player whose party is asked about.
- Parsing [V] ([CharsReplacer](https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/java/me/clip/placeholderapi/replacer/CharsReplacer.java), master): the identifier ends at the **first** underscore (`arken`); the rest (`party_has_<name>`) may contain more underscores and spaces; parameter case is kept. If the expansion is missing or returns `null`, the original text is returned.
- **Return values [U].** Shared memory only says the placeholder tells whether the player is in the viewer's party. PlaceholderAPI's own booleans are configurable and default to `yes` / `no` ([config.yml](https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/resources/config.yml)); `PlaceholderAPIPlugin.booleanTrue()` returns the configured one [V]. An expansion may ignore that setting.
  - **Ask the user** to run `/papi parse <viewer> %arken_party_has_<member>%` and the same for a non-member.
  - Until then: trim, then accept case-insensitively `booleanTrue()`, `yes` or `true`. Everything else, including the unchanged placeholder, an empty string and exceptions, means **not an ally**.
- Also unknown [U]: what it returns for the viewer's own name, for offline players, or with no party. Treat self as an ally **before** calling.
- Only pass names of online `Player` objects, never typed text. Never feed other player-controlled text to `setPlaceholders`.

### Thread safety
- **Neither vendor documents it** (Mythic API wiki, PlaceholderAPI developer pages and `PlaceholderAPI.java`: no statement in what I read). The only warning on the PlaceholderAPI page is in its Hytale section.
- Rule for us: call both **only on the main thread**, as the repo requires for Bukkit calls. The `arken` expansion is third-party code whose thread safety we cannot know.
- Whether Mythic events always fire on the main thread is [U]; we do not need them.
- Cost: how expensive ArkenCore's lookup is, is unknown. Ask only for nearby candidates when a heal, taunt-like effect or XP split needs it, never per tick for all players. If area effects repeat it, cache for about 1 s and drop the cache on quit.

## Pitfalls
- Omitting `required: false` makes ArkenMMO fail without the plugin.
- Result checks like `!result.equals("no")` turn the unchanged placeholder into "ally". Use the whitelist.
- Double XP from two death events.
- `/mythicmobs reload` and mob renames: config keys that match nothing should not error.
- Never shade either plugin.
- Without PlaceholderAPI or ArkenCore everyone is a stranger, so the party XP split falls back to the solo rule.

## Sources
- https://hangar.papermc.io/Lumine/MythicMobs/versions
- https://modrinth.com/plugin/mythicmobs/version/5.14.0
- https://api.modrinth.com/v2/project/mythicmobs/version?game_versions=%5B%2226.3%22%5D
- https://api.modrinth.com/v2/project/placeholderapi/version?game_versions=%5B%2226.3%22%5D
- https://wiki.mythiccraft.io/mythicmobs/API
- https://mvn.lumine.io/repository/maven-public/io/lumine/Mythic-Dist/maven-metadata.xml
- https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/bukkit/events/MythicMobDeathEvent.html
- https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/core/mobs/MobExecutor.html
- https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/core/mobs/ActiveMob.html
- https://www.mythiccraft.io/javadocs/mythic/io/lumine/mythic/api/mobs/MythicMob.html
- https://wiki.placeholderapi.com/developers/using-placeholderapi/
- https://repo.extendedclip.com/releases/me/clip/placeholderapi/maven-metadata.xml
- https://repo.helpch.at/releases/me/clip/placeholderapi/maven-metadata.xml
- https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/java/me/clip/placeholderapi/PlaceholderAPI.java
- https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/java/me/clip/placeholderapi/replacer/CharsReplacer.java
- https://raw.githubusercontent.com/PlaceholderAPI/PlaceholderAPI/master/src/main/resources/config.yml
- https://docs.papermc.io/paper/dev/getting-started/paper-plugins/

## Hand-off
**Contract IDs:** none new.

| Who | Next |
|---|---|
| **main session / user** | Confirm PlaceholderAPI as a compile-time dependency. Get the two `/papi parse` outputs. Confirm the unlisted-Mythic-mob XP rule. Server needs MythicMobs 5.14.0+ and PlaceholderAPI 2.12.3+ |
| **plugin-coder (P2)** | Repositories, dependencies and `paper-plugin.yml` entries above; two isolated hooks; Mythic type cached in the contribution ledger; one XP path; party whitelist check; main thread only. Run `mise run build` to confirm the Mythic signatures. Record the new dependencies in `docs/architecture.md` if its owner asks |
| **model-designer, sound-designer, vfx-designer** | Nothing |
