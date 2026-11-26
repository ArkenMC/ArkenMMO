# skills (skill trees, casting, weapons, levelling)

**Status:** in progress (menus built; levels, combat and weapons not yet)
**Target:** Paper 26.2 with ItemsAdder (changed 2026-11-26). The `docs/research/skill*` notes were checked against 26.3: re-check integration and API facts before relying on them.
**Created:** 2026-11-26 · **Depends on:** classes (on main)

## Goal
Each class levels up, buys skills in a painted skill tree and casts them with mouse combos. **Art quality is the top priority.**

## Player story
I get my class weapon, fight to earn XP and spend points in a dark, ancient-looking tree. Bought skills glow softly. I cast them with mouse combos and watch my mana and combo on the action bar.

## Decisions and design
- User decisions: `.claude/agent-memory/shared/skills-decisions.md`. **They win over the research draft.**
- Base design and numbers (untested): `docs/research/mmo-classes-levelling.md` sections 6-9. Check its 7.5 doubts and section 8 input pitfalls before building.
- Code follows `AGENTS.md` and `docs/architecture.md`.

## Acceptance criteria (Warrior first)
- [ ] Class XP and levels to 30; 18 points: one per level 1-10, then at 12, 15, 17, 20, 22, 25, 27, 30. XP values come from config.
- [ ] `/skills` opens the skill tree menu, with three branches. Click twice to buy. Gates and connections as in draft section 6.
- [ ] Future keystone and ultimate places show as sealed stones.
- [ ] Reset button at slot 49 on **every** tree page, with its own reset texture. Free after 10 s out of combat, 60 s cooldown. Purchases made while the tree is open can be undone if the tree stays valid.
- [ ] Cleave and the 18 Warrior skills of tiers 1-3 work; numbers from config.
- [ ] 4 spells on 3-click combos; loadout menu; new actives fill empty slots; action bar shows combo, mana and failures.
- [ ] Mana as in the decisions. Level-based power replaces vanilla weapon and enchantment damage for class weapons.
- [ ] Starter weapon given and restored; it can't be dropped, traded or stored. Config-defined extra weapons: class-restricted, player-bound, storable only in own inventory and ender chest. Weapons show actual DPS.
- [ ] Party XP and allies as in the decisions; spawner mobs give no XP; no PvP effects.
- [ ] `/class weapon give <player> <id>` (permission `arkenmmo.class.weapon`, default op) gives an extra weapon.
- [ ] Unit tests cover only tree rules, XP and combo input.
- [ ] A MythicMob without its own XP setting gives its underlying vanilla mob's XP.
- [ ] PlaceholderAPI (and MythicMobs if needed) are optional `provided` dependencies (approved by the user).
- [ ] The plugin works without MythicMobs, PlaceholderAPI and ArkenCore.
- [ ] Progress is stored per class and leaves room for rebirth and evolution.

Archer, Mage and Captain code follows after the user has tried Warrior. Their **art** is made now (A1 approved 2026-11-26; the user asked for all classes), using the draft skill lists (research 7.2-7.4).

## Next slice: menus (P2a, approved 2026-11-26)
Built after the art is merged, before levels and combat. It doesn't wait for the casting prototype.
- `/skills` opens the player's class tree, for **all four classes**: archetype tabs, scrolling, back and info.
- Click twice to buy; stones and paths light up; sealed stones; reset and undo.
- Loadout menu: arrange owned actives in the 4 combo slots.
- Hover text and tooltip styles as in `design/gui-skill-tree.md`, like the class menu; text in config. Every skill's hover describes what it does and names its archetype.
- Players get temporary test points from config; purchases and loadout are saved per class.
- No XP, levels, mana, weapons or skill effects yet.
- Paths, names, item keys, glyphs and slots come from the art spec. Archetype display names are in the user decisions.

## Out of scope
Keystones, ultimates (including the sneak + 5-click combo), levels 31-50, rebirths, evolutions, fragments, reset tokens, mob levels of our own, PvP, a party system.

## Assets needed
| Kind | What | Owner |
|---|---|---|
| texture / glyph | Warrior tree pages and backdrop, node and connector states, sealed stones, 19 skill icons, footer buttons including reset, loadout menu | model-designer |
| model / texture | Warrior starter sword | model-designer |
| sound | tree and combo feedback, cast sounds for Warrior actives (custom `.ogg`) | sound-designer |
| effect | Warrior skill effects | vfx-designer |

## Research needed
1. **Casting prototype:** left-click detection, click repeat, entity and block clicks, bow drawing for Archer (draft section 8).
2. MythicMobs and PlaceholderAPI on Paper 26.3: compatibility and the API needed.
3. **Art:** MMO skill icon readability, skill tree layouts and ancient carving references. Learn from them; copy nothing.
4. How to show owned/locked states and connectors in a chest menu with a vanilla resource pack.

## Open questions
None.

## Contract (fixed names; change only via the orchestrator)
| Kind | ID | Owner | Notes |
|---|---|---|---|
| command, permission | `/skills`, `arkenmmo.skills` | plugin-coder | opens the tree; default everyone |
| command, permission | `/class weapon give <player> <id>`, `arkenmmo.class.weapon` | plugin-coder | default op |
| branches | `warrior.guardian`, `warrior.berserker`, `warrior.duelist` | plugin-coder | |
| core skill | `warrior.cleave` | plugin-coder | |
| guardian n1-n6 | `warrior.shield_bash`, `.iron_hide`, `.stalwart`, `.challenging_shout`, `.second_wind`, `.bulwark` | plugin-coder | |
| berserker n1-n6 | `warrior.leaping_strike`, `.bloodthirst`, `.fury`, `.whirlwind`, `.relentless`, `.execute` | plugin-coder | |
| duelist n1-n6 | `warrior.lunge`, `.footwork`, `.focus`, `.riposte`, `.opportunist`, `.hamstring` | plugin-coder | |
| combo slots | 1 `R-L-R`, 2 `R-R-R`, 3 `R-L-L`, 4 `R-R-L` | plugin-coder | Archer mirrored |
| footer | 45 back, 46-48 branch tabs, **49 reset**, 50-51 scroll, 52 loadout, 53 info | both | info moved from 49 in the draft |
| sound events | `skill_unlock`, `skill_unlock_denied`, `skill_tree_reset`, `class_level_up`, `combo_click_left`, `combo_click_right`, `cast_fail`, `skill_warrior_<name>` per active | sound-designer | |
| effects | `class_level_up`, `skill_warrior_<name>` per active | vfx-designer | |
| item models, glyphs | set after the art layout is approved | model-designer | |

## Tasks
Agents are launched only when the user asks.

| Agent | Task | Needs (gate) | Branch |
|---|---|---|---|
| resource-pack-researcher | research 2-4 | brief | feature branch (docs) |
| plugin-coder | P1: casting prototype | brief | `skills/plugin-coder` |
| model-designer | A1: art research, one Warrior tree page and sample icons as previews | brief, research 3-4 | `skills/model-designer` |
| model-designer | A2: all Warrior assets | user approves A1 | `skills/model-designer` |
| sound-designer | Warrior sounds | contract | `skills/sound-designer` |
| vfx-designer | effects engine and Warrior effects | contract | `skills/vfx-designer` |
| plugin-coder | P2: levels, tree, weapons, mana, skills, integrations | P1 tried by the user, research 2 | `skills/plugin-coder` |

## Status
| Agent | Status | Branch | Verdict | Notes |
|---|---|---|---|---|
| all | planned | | | |

## Merge order
1. model-designer
2. sound-designer
3. vfx-designer
4. plugin-coder

## Needs human review
- [ ] Approve art previews.
- [ ] Audition sounds.
- [ ] In-game: combos, skills, tree, weapons, XP, reset.
