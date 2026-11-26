# Architecture

Paper 26.2, Java 25, Paper API only. Package root: `dev.casperrs.arkenMMO`. `ArkenMMO` wires everything: services, listeners and commands are registered only there.

| Package | Responsibility |
|---|---|
| `text` | `Messages`: all player-facing MiniMessage from `messages.yml` (one MiniMessage instance) |
| `pack` | `ResourcePackSettings` (config), `ResourcePackService` (sends the pack, runs actions once it has loaded) |
| `menu` | Generic locked chest menus: `Menu` (buttons, plain items, in-place changes, an action for all other clicks), `MenuListener` (cancels all clicks and drags, runs actions on the next tick) and `MenuIcons` (the items shown). Never knows about features |
| `playerclass` | `PlayerClass` (IDs), `ClassStorage` (player persistent data), `ClassSelection` (rules), `ClassMenus` (layout and items), `ClassCommand` |
| `skill` | `/skills`. Rules without Bukkit types: `SkillCatalog`, `ClassTree`, `Skill`, `SkillNode`, `TreeRules` (unit tested), `Loadout`, `ClassSkills`. Data: `SkillStorage` (player persistent data), `SkillBook` (all changes), `SkillSettings` (test level and points), `SkillValues` (`skill-values.yml`). Menus: `SkillMenus`, `TreeScreen`, `LoadoutScreen`, `TreeView` (slot maps), `SkillItems`, `SkillSession` (one opening), `SkillContext`; `SkillsCommand`. Depends on `playerclass`, never the reverse |
| `casting` | Input: `CastingListener` (events to clicks), `ComboInput` (per-player combos, delayed left clicks, debug log), `ComboTracker` (rules, no Bukkit types, unit tested), `UsableTargets`, `StandInWeapons` (temporary). Casting: `SkillCaster` (loadout slot to skill, checks, cost, cooldown), `Casters`, `CasterState`, `ManaRules`, `CombatListener`, `CastingHud` (action bar). What skills implement and use: `SkillAction`, `SkillFeedback` (sound and effect). Depends on `skill`, `playerclass`, `sound`, `vfx` and `text` |
| `combat` | Used by skills, knows no feature: `SkillTargets` (PvE filter, cone, radius, aim), `SkillDamage`, `OngoingAction`, `OngoingActions` (one shared task), `OngoingListener` (cleanup and fall protection) |
| `warrior` | One `SkillAction` per castable Warrior skill. Depends on `casting`, `combat` and `skill`; only `ArkenMMO` knows it |
| `sound` | `SoundService`: loads `sounds.yml` (optional) and is the only code that plays sounds |
| `vfx` | `Effects` (`play(id, location, viewer)`, reload, shutdown; one shared task while something animates), `EffectPresets`, `LayerParser`, `LayerSettings` (`effects.yml`), `ParticleLayer`, `Shapes`, `Playback`. Knows no feature; owned by the vfx-designer (`design/effects.md`) |

## Notes
- Everything runs on the main thread; there is no I/O beyond reading config files at startup. The server saves player persistent data with the player.
- Class data needs the player online (`/class reset` included). Later per-class progress is keyed by `PlayerClass#id()`; switching only has to change which ID is stored as chosen.
- A new menu uses `Menu`; feature code does not listen to inventory events itself.
- Skills are stored in one container per class under the player's `skills` key (`owned`, `loadout`, `reset_ready_at`); XP, level, rebirth and evolution values go beside them. `/class reset` keeps them. A saved tree the rules no longer allow is emptied when it is next read.
- Skill numbers live in `skill-values.yml` and fill the placeholders of the same name in the skill's description in `messages.yml`.
- Menu slots must match the painted art (see `docs/briefs/classes.md` and `design/gui-skill-tree.md`).

## Casting input
- Left clicks come from `LEFT_CLICK_AIR`/`LEFT_CLICK_BLOCK` and `PrePlayerAttackEntityEvent`; right clicks from `PlayerInteractEvent` and `PlayerInteractEntityEvent` (which includes the "at entity" event). `PlayerArmSwingEvent` is only logged.
- One click per player per tick. `ComboInput#ignore` claims the tick for a use of a block or entity, so later events from the same press don't count.
- A client's swing for a dropped item can arrive before the drop, so a left click waits a tick and a drop discards it. Any later click of that player counts the waiting one first, which keeps the order.
- A right click within 250 ms of the previous right click counts as the held button repeating.
- Click events are only watched (`MONITOR`), never cancelled, so the vanilla hit or use still happens.

## Casting and skills
- A completed combo is a loadout slot (1-4) of the saved loadout. A new skill action is registered by skill ID in `ArkenMMO`; skills without one say they can't be cast yet.
- `SkillAction#prepare` changes nothing; cost and cooldown are only taken when it returns something to run.
- Anything that outlives the cast is an `OngoingAction`, so quit, death, world change and disable end it.
- All skill damage goes through `SkillDamage`; all targets through `SkillTargets`.
- A skill's sound event and effect have the same ID, played together by `SkillFeedback`. Effects play only through `Effects.play`. `ArkenMMO` shuts `Effects` down after ending ongoing actions; there is no reload command yet.
- A sound's `fallback` only replaces a blank or invalid `key`: ItemsAdder sends the pack, and the server can't know whether a client has a custom sound.
- Mana, cooldowns and repeat costs are kept in memory until restart. Power and mana numbers are the `power` and `mana` sections of `skill-values.yml`.

## Standards
- Package by feature, one responsibility per class; classes under about 500 lines, methods under about 60. No wildcard imports or package cycles.
- Comments only for what the code can't say; no `@param`/`@return` tags.
- `config.yml` holds only what an admin sets (resource pack first); player text goes in `messages.yml`; internal values are constants.
- Records and `final` fields by default; `@Nullable` or `Optional` on purpose.
