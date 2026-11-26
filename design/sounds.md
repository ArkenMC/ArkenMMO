# Sounds

Events are in `src/main/resources/sounds.yml`. Keys are `arkenmmo:<name>`; files are under `resourcepack/assets/arkenmmo/sounds/`. All are original synthesis (no external source), mono. Regenerate with `mise run sounds`.

| Event | Sound key | Files | Feel | Vanilla fallback |
|---|---|---|---|---|
| `combo_click_left` | `ui.combo_click_left` | `ui/combo_click_left_1-3` (60 ms) | tiny low tock | `block.note_block.hat` |
| `combo_click_right` | `ui.combo_click_right` | `ui/combo_click_right_1-3` (60 ms) | the same, a fifth higher | `block.note_block.snare` |
| `cast_fail` | `ui.cast_fail` | `ui/cast_fail` (240 ms) | soft falling double buzz | `block.note_block.bass` |
| `skill_warrior_cleave` | `skill.warrior.cleave` | `skill/warrior/cleave_1-3` (340 ms) | sharp swoosh with a faint ring | `entity.player.attack.sweep` |
| `skill_warrior_leaping_strike` | `skill.warrior.leaping_strike` | `skill/warrior/leaping_strike_1-2` (500 ms) | push-off, rising whoosh | `entity.breeze.jump` |
| `skill_warrior_leaping_strike_impact` | `skill.warrior.leaping_strike_impact` | `skill/warrior/leaping_strike_impact_1-2` (800 ms) | ground slam, grit and dust | `item.mace.smash_ground` |
| `skill_warrior_whirlwind` | `skill.warrior.whirlwind` | `skill/warrior/whirlwind_1-3` (520 ms) | two blade passes, rising wind, ring | `entity.player.attack.sweep` |
| `skill_warrior_execute` | `skill.warrior.execute` | `skill/warrior/execute_1-2` (550 ms) | steel strike, deep thud | `entity.player.attack.crit` |
| `skill_warrior_execute_low` | `skill.warrior.execute_low` | `skill/warrior/execute_low_1-2` (1000 ms) | deeper second thud, crack, dark toll | `item.mace.smash_ground_heavy` |

Fallback keys were checked in `org.bukkit.Sound` of `paper-api 26.2.build.135-stable` (`javap`, 2026-11-26).

## Delivery through ItemsAdder
- `mise run itemsadder` puts `sounds.json`, `lang/en_us.json` and all `.ogg` files in `arkenmmo/resourcepack/assets/arkenmmo/` (checked in the zip).
- The [merge guide](https://wiki.itemsadder.com/adding-content/merge-resourcepacks) says to copy a pack's `assets` into `contents/<folder>/resourcepack/` and run `/iazip`. It does not mention sounds.
- The [sounds page](https://wiki.itemsadder.com/adding-content/adding-sounds/) shows a hand-written `sounds.json` in a namespace's `resourcepack` folder, but labels that method "4.0.10 and lower". For 4.0.12+ it shows a `sounds:` section in an ItemsAdder YAML config.
- **Unverified:** that 4.0.18 includes our `sounds.json` and subtitles in its generated pack. Test after `/iazip`: `/playsound arkenmmo:skill.warrior.cleave players @s`, and look for `sounds.json` in the generated pack. If it fails, either define the sounds with the YAML method or use the fallbacks.
- **No automatic fallback:** the game plays nothing for a missing custom key, and the server can't detect it. To use vanilla sounds, copy each `fallback` into its `key` in the server's `sounds.yml`.

## Needs human review
- [ ] Audition all 21 files; none has been heard. Check especially: clicks (subtle enough, left and right distinct), cast_fail (not annoying), the impact and both executes on small speakers and headphones, and that `_low` clearly sounds bigger.
- [ ] Whirlwind three times in game, at the coder's pulse spacing. A file overlay at 0.5 s and 0.75 s spacing peaks at -3.2 dBFS (no build-up).
- [ ] The fallbacks in game, with the volumes and pitches tuned for the custom sounds.
- [ ] The ItemsAdder test above, including subtitles.
