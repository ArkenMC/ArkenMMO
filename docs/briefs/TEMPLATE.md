# <feature-name>

**Status:** planned  <!-- planned | in progress | review | done -->
**Created:** YYYY-MM-DD · **Depends on:** <features whose code/API must already be on main, or "none">

## Goal
One or two sentences: what this feature adds and why it matters for the game.

## Player story
As a player, I … so that … (one short paragraph describing the experience, including how it feels: sounds, effects, feedback).

## Acceptance criteria
- [ ] Concrete, testable statements (what happens, for whom, with which numbers coming from config)
- [ ] …

## Out of scope
- What this feature deliberately does not do (and which later feature might)

## Assets needed
| Kind | What | Owner |
|---|---|---|
| model / texture / glyph | … | model-designer |
| sound | … | sound-designer |
| effect | … | vfx-designer |

(Write "none" for a kind that isn't needed.)

## Research needed
Open technical questions for the researcher (API, resource pack format, version support), or "none".

## Open questions
Questions for the user that block or shape the design. The brief isn't approved while any are unanswered.

## Contract (fixed names; change only via the orchestrator)
| Kind | ID | Owner | Notes |
|---|---|---|---|
| item model | `<ns>:<id>` | model-designer | |
| sound event | `<event>` | sound-designer | key `<ns>:<category>.<name>`, fallback `minecraft:…` |
| effect | `<effect_id>` | vfx-designer | placeholders: … |
| message key | `<section.key>` | plugin-coder | in messages.yml |
| config key | `<file>: <path>` | owner | |

## Tasks
| Agent | Task | Needs (gate) | Branch |
|---|---|---|---|
| resource-pack-researcher | … | — | feature branch (docs) |
| model-designer | … | contract | `<feature>/model-designer` |
| sound-designer | … | contract | `<feature>/sound-designer` |
| vfx-designer | … | contract | `<feature>/vfx-designer` |
| plugin-coder | … | contract, research, APIs on the feature branch | `<feature>/plugin-coder` |
## Status
| Agent | Status | Branch | Verdict | Notes |
|---|---|---|---|---|
| | planned | | | |

## Merge order
1. …

## Needs human review
- [ ] Audition sounds: …
- [ ] Check in-game: …
