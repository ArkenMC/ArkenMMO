# classes (class selection)

**Status:** review
**Created:** 2026-11-25 · **Depends on:** none

## Goal
Players pick one of four classes (Warrior, Archer, Mage, Captain) in a custom-painted menu. **The quality of the art is the top priority.** Skill trees and skills are a later feature with its own brief.

## Player story
After the tutorial (another plugin runs our command), I see two large pixel-art heroes. I flip to the other two, hover a hero to read about the class, click it, confirm, and the choice is saved.

## User decisions (2026-11-25)
- Two pages, two large panels per page: page 1 Warrior + Archer, page 2 Mage + Captain.
- One arrow button, same slots on both pages: "Next" on page 1, "Back" on page 2.
- Characters are chunky, blocky, Minecraft-like heroes (big heads, large weapons), facing slightly toward the centre, one colour identity each, name plate below. Style reference described by the user: faceted blocky class figurines with strong silhouettes (a warrior/paladin in gold plate with a big sword, a mage holding a staff and a flame, a green-hooded hunter), name banner at each base.
- Art is generated with Python (Pillow). **The Warrior panel and page frame are approved by the user first** (as many rounds as needed; this overrides the one-attempt rule). Only then the other three classes.
- No inventory hover highlight. This is global: both highlight sprites are transparent, so it disappears in every inventory.
- Plain vanilla resource pack. The server has ItemsAdder 4.0.18, which doesn't support 26.3.
- The class choice is final. Switching comes later: keep the code single-responsibility so it is easy to add (progress will be stored per class ID).
- **No unit, integration or e2e tests, none at all.**
- Code: mind async (only thread-safe work off the main thread), efficient, reusable methods; overloading and overriding where they remove real duplication; no speculative abstractions.
- Custom sounds (`.ogg`) and effects come with the skills feature, not this one.

## Acceptance criteria
- [ ] `/class select <player>` (permission `arkenmmo.class.select`, default op; works from console) opens the menu for a player without a class; for a player with a class it tells the sender and does nothing.
- [ ] `/class` (everyone) opens the menu if the sender has no class; otherwise it tells them their class.
- [ ] `/class reset <player>` (permission `arkenmmo.class.reset`, default op) removes the player's class.
- [ ] Two pages as above; the whole panel (24 slots) is clickable and shows one identical class tooltip.
- [ ] Clicking a class opens a confirm screen saying the choice is final, with Confirm and Back. Closing any screen chooses nothing.
- [ ] The class is saved and survives rejoin and restart.
- [ ] No click or drag can move, take or insert items while a menu is open.
- [ ] The plugin sends the resource pack (required) using URL, SHA-1 and UUID from the first section of `config.yml`, with an on/off switch; incomplete settings log a warning and send nothing. A menu requested while the pack is still loading opens once it has loaded.
- [ ] All player-facing text is MiniMessage from config. Exception: text painted into the art (headers, class names, "THIS CHOICE IS FINAL", "CONFIRM", "BACK"). Item tooltips still carry the final-choice wording and button names from config.

## Out of scope
Skill trees, skills, levelling, rebirths, class switching, custom sounds, effects, ItemsAdder integration.

## Assets needed
| Kind | What | Owner |
|---|---|---|
| texture / glyph | 2 class page backgrounds, 4 confirm backgrounds, 4 class tooltip styles, transparent highlight sprites, blank item model, `pack.mcmeta`, `pack.png` | model-designer |
| sound | none | |
| effect | none | |

## Research
Done: `docs/research/custom-gui-and-pixel-art.md` (geometry, font JSON, title string, pipeline, style guide, review checklist), `docs/research/mmo-classes-levelling.md` (class fantasy; Captain).

## Open questions
None.

## Contract (fixed names; change only via the orchestrator)
| Kind | ID | Owner | Notes |
|---|---|---|---|
| font | `arkenmmo:gui` | model-designer | shifts `U+F801..F809` = -1..-256, `U+F821..F829` = +1..+256 |
| glyphs | page 1 `U+E001..E004`, page 2 `U+E005..E008` | model-designer | order TL, TR, BL, BR |
| glyphs | confirm: warrior `U+E101..E104`, archer `U+E105..E108`, mage `U+E109..E10C`, captain `U+E10D..E110` | model-designer | same order |
| title string | research note §1.4 | model-designer | same shifts for every background; only the 4 glyphs differ |
| layout, class page | left panel: columns 0-3, rows 0-5; right panel: columns 5-8, rows 0-5; arrow: slots 40 and 49 | both | arrow is painted into the background |
| layout, confirm | chosen class panel: columns 0-3 (art only, not clickable); Confirm: columns 5-8, rows 1-2; Back: columns 5-8, rows 3-4 | both | buttons painted into the background |
| item model | `arkenmmo:gui/blank` | model-designer | `minecraft:empty` |
| tooltip style | `arkenmmo:warrior`, `arkenmmo:archer`, `arkenmmo:mage`, `arkenmmo:captain` | model-designer | |
| class id | `warrior`, `archer`, `mage`, `captain` | plugin-coder | |
| permissions | `arkenmmo.class.select`, `arkenmmo.class.reset` | plugin-coder | |

Art sources live in `design/scripts/` (helpers and hand-edited grids in subfolders there). The style guide is `design/gui-style-guide.md`. Previews are written to `target/previews/gui/` (not committed).

## Tasks
| Agent | Task | Needs (gate) | Branch |
|---|---|---|---|
| model-designer | A1: pipeline, preview compositor, page frame, Warrior panel. A2: everything else | brief; A2 needs the user's approval of A1 | `classes/model-designer` |
| plugin-coder | commands, menus, storage, pack sending; no tests | contract (slots and glyphs are fixed) | `classes/plugin-coder` |

## Status
| Agent | Status | Branch | Verdict | Notes |
|---|---|---|---|---|
| model-designer | merged | `classes/model-designer` | asset checks pass | final tweaks done; in-game check open |
| plugin-coder | merged | `classes/plugin-coder` | build passes | not run in-game |

## Merge order
1. model-designer
2. plugin-coder

## Needs human review
- [ ] In-game: background alignment, player-inventory cells and "Inventory" plate, art at the used GUI scale, tooltips, hidden highlight.
- [ ] In-game: commands, paging, confirm, persistence, pack download.
