# Shared memory

Facts and user decisions every agent needs. Rules: `AGENTS.md`. Add one dated line per fact with its source; put longer topics in their own file here and link them.

## Facts
- 2026-11-25: Resource pack format for 26.3 is 97.1 (https://minecraft.wiki/w/Pack_format).
- 2026-11-26: Resource pack format for 26.2 is 88.0; patches have no own row (https://minecraft.wiki/w/Pack_format). Latest stable API then: `paper-api 26.2.build.135-stable` (repo.papermc.io maven-metadata).
- 2026-11-26: No 26.3 changelog entry touches item model definitions, tooltip sprites, nine-slice .mcmeta, bitmap fonts or slot highlights (minecraft.wiki Java_Edition_26.3, last ~30% not read); our pack needs no art change for 26.2.

## User decisions
- 2026-11-26: The server runs Paper 26.2 with ItemsAdder 4.0.18, which works fine on it (user, from the live server). The plugin build and checks run in GitHub Actions; local sessions may lack mise.
- 2026-11-26: The pack ships through ItemsAdder as content folder `arkenmmo` (`mise run itemsadder`, `tools/itemsadder.py`); `resourcepack/` stays the source. ItemsAdder item `arkenmmo:emerald` is in `itemsadder/contents/arkenmmo/configs/emerald.yml`.
- 2026-11-26: The plugin no longer sends or waits for a resource pack: `pack` package, `config.yml` and the pack messages are removed. ItemsAdder applies the pack before join (`auto_apply.before_join: true`) and kicks on decline/fail (server's ItemsAdder config.yml).
- 2026-11-26: **Target is Paper 26.2**, not 26.3, so ItemsAdder can be used. Pack format 88.0. Notes written before this date that say 26.3 are about the old target.
- 2026-11-26: The emerald is a custom item (`arkenmmo:emerald` item model and tooltip style), not a vanilla override (`design/item-emerald.md`).
- 2026-11-25: Class selection uses a plain vanilla resource pack (`docs/briefs/classes.md`).
- 2026-11-25: Skill sounds may be custom `.ogg` files; use the sound-designer for sounds and the vfx-designer for effects.
- 2026-11-25: Skill tree art direction is in `design/gui-style-guide.md`.

- 2026-11-26: ItemsAdder wiki (wiki.itemsadder.com, version not stated on pages): merging a pack = copy its `assets/` to `contents/<folder>/resourcepack/`, then `/iazip`; `contents-folders-priorities` in config.yml orders folders. Item `tooltip_style` needs IA 4.0.9+ and MC 1.21.2+. `resource: generate: false` + `model_path` for an own model. Data `components:` need the separate ItemsAdderAdditions addon. API: `CustomStack.getInstance(id)`, `ItemsAdderLoadDataEvent`. SpigotMC refuses automated fetches (403).

## Where earlier findings are
- GUI technique and sources: `.claude/agent-memory/mc-plugin-team-resource-pack-researcher/MEMORY.md`
- Pack tools and GUI art pipeline: `.claude/agent-memory/mc-plugin-team-model-designer/MEMORY.md`
- Build and API facts: `.claude/agent-memory/mc-plugin-team-plugin-coder/MEMORY.md`
