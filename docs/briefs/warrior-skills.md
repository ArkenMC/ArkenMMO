# warrior-skills (first castable skills)

**Status:** review (built; not tested in game)
**Created:** 2026-11-26 · **Depends on:** skill menus (on main)

## Goal
Try real skills: Cleave and three Warrior's Rage actives, cast with mouse combos, with clean effects and original sounds.

## Player story
With an iron sword I click a combo. The skill from that loadout slot fires: a sharp slash, a leap and slam, a spinning storm or a heavy finisher. The action bar shows my clicks, mana and why a cast failed.

## Read
`AGENTS.md`, `.claude/agent-memory/shared/*.md`, `docs/briefs/skills.md`, research `docs/research/mmo-classes-levelling.md` 7.1, 7.5, 8. **Target: Paper 26.2** with ItemsAdder; older notes that say 26.3 must be re-checked.

## Skills (draft values; configurable)
P = `6 + 0.5 * (level - 1)` with the test level (30 → 20.5).
| Skill | Mana / cooldown | Effect | Feel |
|---|---|---|---|
| `warrior.cleave` | 20 / 4 s | 130% P to all enemies in a 3.5 m, 120-degree cone | quick slash arc, sharp swoosh |
| `warrior.leaping_strike` | 25 / 8 s | leap up to 8 m; landing deals 120% P in 3 m; no fall damage from the leap | launch whoosh, ground slam with dust |
| `warrior.whirlwind` | 35 / 10 s | 3 pulses over 1.5 s, 60% P each, 4 m | blade rings, rising wind |
| `warrior.execute` | 30 / 9 s | 180% P single target; 300% below 30% health | crimson strike, deep thud; bigger below 30% |

Clean and readable over flashy. Warrior crimson. Others see and hear skills too.

## Acceptance criteria
- [ ] Combos from the prototype (`skills/plugin-coder`) cast the skill in that loadout slot. Core skills can be on the loadout.
- [ ] Only for Warriors holding the temporary stand-in weapon (iron sword).
- [ ] 100 mana; +4/s, +8/s after 5 s out of combat; recasting the same spell within 4 s adds 25% of base cost per repeat, up to +100%.
- [ ] Cooldowns; a failed cast costs nothing and says why. Action bar: combo, mana, failures.
- [ ] Only owned skills cast. Others and all passives do nothing and say so when cast.
- [ ] PvE: never hits players, tamed animals, villagers or armor stands. Damage has the player as source, so protection plugins can cancel it.
- [ ] Channels and delayed hits end on quit, death, world change and disable.
- [ ] Sounds only through `sounds.yml` events, effects only through `Effects.play(id)`.

## Out of scope
Class weapons, basic attack damage changes, XP and levels, passives, other skills and classes, ultimates.

## Assets needed
| Kind | What | Owner |
|---|---|---|
| sound | events below | sound-designer |
| effect | engine and presets below | vfx-designer |
| model / texture | none | |

## Research needed
None separate; check APIs against the 26.2 Javadocs.

## Open questions
None.

## Contract (fixed names; change only via the orchestrator)
| Kind | ID | Owner | Notes |
|---|---|---|---|
| sound events | `combo_click_left`, `combo_click_right`, `cast_fail` | sound-designer | only the caster hears these |
| sound events | `skill_warrior_cleave`, `skill_warrior_leaping_strike`, `skill_warrior_leaping_strike_impact`, `skill_warrior_whirlwind` (once per pulse), `skill_warrior_execute`, `skill_warrior_execute_low` | sound-designer | `_low` replaces the normal one below 30% health |
| effects | `skill_warrior_cleave`, `skill_warrior_leaping_strike`, `skill_warrior_leaping_strike_impact`, `skill_warrior_whirlwind` (once per pulse), `skill_warrior_execute`, `skill_warrior_execute_low` | vfx-designer | no placeholders |
| effect locations | cleave: caster's feet with caster's yaw; leap: take-off feet; impact: landing feet; whirlwind: caster's feet; execute: target's feet, yaw from caster | both | `viewer` is null (everyone sees) |
| Java API | `Effects.play(String effectId, Location loc, @Nullable Player viewer)` in package `vfx` | vfx-designer | coder wires construction, reload and shutdown |
| config | `src/main/resources/sounds.yml` | sound-designer | loaded and played by plugin-coder |

## Tasks
| Agent | Task | Needs (gate) | Branch |
|---|---|---|---|
| vfx-designer | `Effects` engine and 6 presets | contract | `warrior-skills/vfx-designer` |
| sound-designer | 9 events | contract | `warrior-skills/sound-designer` |
| plugin-coder | C1: reapply the combo prototype, then mana, cooldowns, the four skills, sound playing | contract | `warrior-skills/plugin-coder` |
| plugin-coder | C2: connect `Effects` | vfx-designer merged | same |

Unit tests only for combo input and tree rules.

## Status
| Agent | Status | Branch | Verdict | Notes |
|---|---|---|---|---|
| all | merged | `warrior-skills/*` | build and 19 tests pass | in-game test open |

## Merge order
1. sound-designer
2. vfx-designer
3. plugin-coder

## Needs human review
- [ ] In game: all four combos, damage, leap distance and fall damage, effects.
- [ ] Audition the sounds; check ItemsAdder includes `sounds.json` and the `.ogg` files.
