# Project guide for Claude

<!-- Replace every <…> below, then delete this comment. -->
**ArkenMMO**: Classes, levelling, rebirths and related MMO features.

A **Paper Minecraft plugin**, built with **Maven** (Paper API only, no NMS). The target version is the `paper-api` version `pom.xml` declares (Paper 26.x).

## The team (plugin `mc-plugin-team`)
The agent team comes from the **`mc-plugin-team`** plugin ([Casper-RS/mc-plugin-team](https://github.com/Casper-RS/mc-plugin-team)), enabled in `.claude/settings.json`:
- agents run as `mc-plugin-team:<agent>` (e.g. `subagent_type: "mc-plugin-team:plugin-coder"`)
- `/mc-plugin-team:feature <name> <description>` runs a feature end to end
- every agent preloads **`team-context`** (the team and git identities, ownership model, workflow, gates, report format, agent memory, ground rules)
- the ownership hook ships with the plugin and reads **this repo's** `.claude/ownership.json`

Everything below is specific to this repo: this file, `.claude/ownership.json`, `docs/`, `design/`, and the agents' memory in `.claude/agent-memory/mc-plugin-team-<agent>/`.

## Docs (in `docs/`)

| File | Covers | Read when |
|---|---|---|
| `design.md` | the design document: what the plugin should be (Summary first, then sections) | start of every job; the full section before building something it covers |
| `briefs/<feature>.md` | feature brief from `briefs/TEMPLATE.md` | before working on that feature |
| `paper-26x-reference.md` | Java 25, version strings, Adventure 5, world keys, API changes, rules | before any code |
| `toolchain.md` | mise: pinned Java/Maven/Python, build/test/asset tasks, worktree trust | before any build or test |
| `minimessage.md` | all player-facing text: MiniMessage, placeholders, security, fonts/glyphs | any feature that shows text |
| `integrations.md` | ItemsAdder & ModelEngine | the project uses either plugin |
| `architecture.md` | package structure & conventions (maintained by plugin-tester) | always, if it exists |
| `research/*.md` | resource pack research notes | before building a researched feature |
| `reviews/*.md` | test & review reports | after a review |
| `balance/model.md`, `balance/targets.md` | economy formula contract and pacing targets (only if the plugin has an economy) | before any economy code |

## Plugin config owned by designers

| File | Covers | Owner |
|---|---|---|
| `src/main/resources/sounds.yml` | game event → sound key, vanilla fallback, volume, pitch range, source | sound-designer |
| `src/main/resources/effects.yml` | effect presets and performance `limits` | vfx-designer |
| `src/main/resources/balance/*.yml` | every balance value (format in `docs/balance/model.md`) | balance-designer |

## Ownership
Who may edit what is defined in `.claude/ownership.json` (human-controlled) and summarised in the `team-context` skill. The orchestrator (Rickroll Rick, the main session) owns `CLAUDE.md`, `docs/briefs/`, `docs/design.md` (only its "Differences from the current build" list, unless the user asks) and `.github/`. `mise run ownership-check <branch>` checks every commit against its author's paths before a merge.

## Ground rules
- Build with `mise run build`, test with `mise run test`, full check with `mise run check`, assets with `mise run validate-assets` and `mise run sound-check`, pacing with `mise run balance-check`, pack with `mise run pack`. Never run plain `mvn`; use `mise exec -- mvn …`. CI runs the same checks on every push and PR.
- Never shade Paper, Adventure/MiniMessage, ItemsAdder or ModelEngine; they use `provided` scope.
- Never hardcode sounds or particles: sounds go through `sounds.yml` events, effects through `Effects.play(id)`.
- Never set balance values in code.
- If a feature needs something the target version or an integration doesn't support, stop and report it instead of working around it.
- Only the user merges into `main`.
