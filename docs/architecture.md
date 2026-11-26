# Architecture

Paper 26.2, Java 25, Paper API only. Package root: `dev.casperrs.arkenMMO`. `ArkenMMO` wires everything: services, listeners and commands are registered only there.

| Package | Responsibility |
|---|---|
| `text` | `Messages`: all player-facing MiniMessage from `messages.yml` (one MiniMessage instance) |
| `menu` | Generic locked chest menus: `Menu` (rectangular buttons) and `MenuListener` (cancels all clicks and drags, runs actions on the next tick). Never knows about features |
| `playerclass` | `PlayerClass` (IDs), `ClassStorage` (player persistent data), `ClassSelection` (rules), `ClassMenus` (layout and items), `ClassCommand` |

## Notes
- Everything runs on the main thread; the feature does no I/O of its own beyond reading `messages.yml` at startup. The server saves player persistent data with the player.
- Class data needs the player online (`/class reset` included). Later per-class progress is keyed by `PlayerClass#id()`; switching only has to change which ID is stored as chosen.
- A new menu uses `Menu`; feature code does not listen to inventory events itself.
- Menu slots must match the painted art (see `docs/briefs/classes.md`).

## Standards
- Package by feature, one responsibility per class; classes under about 500 lines, methods under about 60. No wildcard imports or package cycles.
- Comments only for what the code can't say; no `@param`/`@return` tags.
- `config.yml` holds only what an admin sets (there is none yet: ItemsAdder sends the resource pack, see `AGENTS.md`); player text goes in `messages.yml`; internal values are constants.
- Records and `final` fields by default; `@Nullable` or `Optional` on purpose.
