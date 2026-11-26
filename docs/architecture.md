# Architecture

Paper 26.2, Java 25, Paper API only. Package root: `dev.casperrs.arkenMMO`. `ArkenMMO` wires everything: services, listeners and commands are registered only there.

| Package | Responsibility |
|---|---|
| `text` | `Messages`: all player-facing MiniMessage from `messages.yml` (one MiniMessage instance) |
| `pack` | `ResourcePackSettings` (config), `ResourcePackService` (sends the pack, runs actions once it has loaded) |
| `menu` | Generic locked chest menus: `Menu` (buttons, plain items, in-place changes, an action for all other clicks), `MenuListener` (cancels all clicks and drags, runs actions on the next tick) and `MenuIcons` (the items shown). Never knows about features |
| `casting` | 3-click combos: `ComboTracker` (rules, no Bukkit types), `CastingListener` (events to clicks), `ComboInput` (per-player state, action bar, debug log), `UsableTargets`, `StandInWeapons` (temporary) |
| `playerclass` | `PlayerClass` (IDs), `ClassStorage` (player persistent data), `ClassSelection` (rules), `ClassMenus` (layout and items), `ClassCommand` |
| `skill` | `/skills`. Rules without Bukkit types: `SkillCatalog`, `ClassTree`, `Skill`, `SkillNode`, `TreeRules` (unit tested), `Loadout`, `ClassSkills`. Data: `SkillStorage` (player persistent data), `SkillBook` (all changes), `SkillSettings` (test level and points), `SkillValues` (`skill-values.yml`). Menus: `SkillMenus`, `TreeScreen`, `LoadoutScreen`, `TreeView` (slot maps), `SkillItems`, `SkillSession` (one opening), `SkillContext`; `SkillsCommand`. Depends on `playerclass`, never the reverse |

## Notes
- Everything runs on the main thread; the feature does no I/O of its own beyond reading config at startup. The server saves player persistent data with the player.
- Class data needs the player online (`/class reset` included). Later per-class progress is keyed by `PlayerClass#id()`; switching only has to change which ID is stored as chosen.
- A new menu uses `Menu`; feature code does not listen to inventory events itself.
- Skills are stored in one container per class under the player's `skills` key (`owned`, `loadout`, `reset_ready_at`); XP, level, rebirth and evolution values go beside them. `/class reset` keeps them. A saved tree the rules no longer allow is emptied when it is next read.
- Skill numbers live in `skill-values.yml` and fill the placeholders of the same name in the skill's description in `messages.yml`.
- Menu slots must match the painted art (see `docs/briefs/classes.md` and `design/gui-skill-tree.md`).

## Casting input
- Left clicks come from `LEFT_CLICK_AIR`/`LEFT_CLICK_BLOCK` and `PrePlayerAttackEntityEvent`; right clicks from `PlayerInteractEvent` and `PlayerInteractEntityEvent` (which includes the "at entity" event). `PlayerArmSwingEvent` is only logged.
- One click per player per tick. `ComboInput#ignore` claims the tick for a drop or a use of a block or entity, so later events from the same press don't count.
- A right click within 250 ms of the previous right click counts as the held button repeating.
- Click events are only watched (`MONITOR`), never cancelled. The one exception is the arrow of an Archer draw that was a combo click.

## Standards
- Package by feature, one responsibility per class; classes under about 500 lines, methods under about 60. No wildcard imports or package cycles.
- Comments only for what the code can't say; no `@param`/`@return` tags.
- `config.yml` holds only what an admin sets (resource pack first); player text goes in `messages.yml`; internal values are constants.
- Records and `final` fields by default; `@Nullable` or `Optional` on purpose.
