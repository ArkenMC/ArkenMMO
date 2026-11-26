# Shared memory

Facts and user decisions every agent needs. Rules: `AGENTS.md`. Add one dated line per fact with its source; put longer topics in their own file here and link them.

## Facts
- 2026-11-25: Resource pack format for 26.3 is 97.1 (https://minecraft.wiki/w/Pack_format).

- 2026-11-26: ArkenCore (private repo; don't copy its code here) offers no public Java API for parties. Other plugins read them through PlaceholderAPI: `%arken_party_has_<name>%` says whether that player is in the viewer's party (ArkenCore `docs/party.md`, read with the user's OK).
- 2026-11-26: MythicMobs 5.14.0 and PlaceholderAPI 2.12.3 list 26.3 support (listings only, untested). Coordinates, plugin.yml setup, GUI approach and caveats: `docs/research/skills-integrations.md`, `skill-tree-gui.md`, `skill-tree-art.md`, `casting-input-sources.md`.
- 2026-11-26: Tested in game by the user: `/papi parse <viewer> %arken_party_has_<name>%` returned `false` before the other player was in the viewer's party and `true` after they joined.

## User decisions
- 2026-11-26: All skills stage decisions, including rebirth ideas for later: [skills-decisions.md](skills-decisions.md).
- 2026-11-25: Class selection uses a plain vanilla resource pack (`docs/briefs/classes.md`).
- 2026-11-25: Skill sounds may be custom `.ogg` files; use the sound-designer for sounds and the vfx-designer for effects.
- 2026-11-25: Skill tree art direction is in `design/gui-style-guide.md`.

## Where earlier findings are
- GUI technique and sources: `.claude/agent-memory/mc-plugin-team-resource-pack-researcher/MEMORY.md`
- Pack tools and GUI art pipeline: `.claude/agent-memory/mc-plugin-team-model-designer/MEMORY.md`
- Build and API facts: `.claude/agent-memory/mc-plugin-team-plugin-coder/MEMORY.md`
