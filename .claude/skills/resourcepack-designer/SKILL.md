---
name: resourcepack-designer
description: Design ArkenMMO resource pack content without the mc-plugin-team plugin - models, textures, GUI art and glyphs, sounds, and particle or display effects. Use when the user wants to design, draw, animate or retune any of these and the mc-plugin-team agents are not available.
---

# Designers without the team plugin

For anyone working on ArkenMMO without `mc-plugin-team`. If `mc-plugin-team:*` agents are available, use the team workflow in `CLAUDE.md` instead.

Without the plugin, the team parts of `CLAUDE.md` (the plugin team, ownership checks, agent identities, merge rules for agent branches) don't apply. Its ground rules and docs still do.

## The designers
| Agent | For | Guide |
|---|---|---|
| `model-designer` | models, textures, animations, GUI images, glyphs, ItemsAdder/ModelEngine content, `pack.mcmeta` | `references/models.md` |
| `sound-designer` | `.ogg` sounds, `sounds.json`, `sounds.yml` | `references/sounds.md` |
| `vfx-designer` | particle and display-entity effects, particle textures, `effects.yml`, the `vfx` Java package | `references/vfx.md` |

## Running them
- When the user asks for design work, launch the matching agent. Their request is the permission to launch it.
- Give the agent the full request, plus any names or IDs already agreed.
- Run independent designers in parallel. If one needs another's asset (an effect using a custom item model), run that one first and pass on the IDs. Never run two on the same files.
- An agent can't ask the user questions. If it comes back with one, ask the user, then continue that agent.
- Relay its result: files changed, IDs for the code, previews to look at and what needs a human check.

## Shared rules (every designer)
- **Commits:** don't commit or push unless the user asks. Use the user's own git identity.
- **Files:** edit only what your guide lists under "Your files". If something else needs changing, report it.
- **Brief:** if `docs/briefs/<feature>.md` covers the work, read it and use its IDs exactly. Otherwise the user's request is the brief: pick clear IDs and report them.
- **Version:** the target is the `paper-api` version in `pom.xml`. Check pack formats and APIs against sources for that exact version, never from recall.
- **Originality:** only original work. Never copy or trace textures, models or sounds from games (including Minecraft), packs or plugins. Use references to learn technique.
- **Notes:** the style guides and lessons in `design/` are how the project learns. Read them before a job and update them after it.
- **Rules and memory:** follow `AGENTS.md`. Before a job, read `.claude/agent-memory/shared/MEMORY.md`, your own `.claude/agent-memory/<agent>/` and the relevant `mc-plugin-team-*` folders (read-only for you). Save new verified facts in your folder, which is yours to write besides the files your guide lists. Put facts everyone needs in your report; the main session writes them to `shared/`.
- **Tools:** build, test and asset tasks run through `mise` (`docs/toolchain.md`). Run `mise install` once.
