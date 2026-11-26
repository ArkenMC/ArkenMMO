# Asset: skill tree and loadout menus

**Status:** all four classes built and wired into the pack (A2). The A1 look and layout were approved by the user; the other classes, the redraws, the off-page paths and the loadout menu are **not yet approved**. All art is placeholder until then.
**Brief:** `docs/briefs/skills.md` · **Style:** `design/gui-style-guide.md` · **References:** `design/skill-tree-visual-research.md`
**Pipeline:** plain vanilla resource pack, Paper 26.3, namespace `arkenmmo`. `pack.mcmeta` is unchanged (`min_format [97, 1]`, `max_format 97`).
**Sounds, effects:** none made here. The Warrior starter sword is not part of this task.

## Files
| File | What |
|---|---|
| `design/scripts/gui_skill_tree.py` | writes everything below into the pack (`mise run assets`) |
| `design/scripts/pixelkit/treetheme.py` | classes, branches, skills, combos, class colours |
| `design/scripts/pixelkit/iconkit.py`, `treeicons.py`, `icons_*.py` | 24x24 master masks: 76 skills and 12 tab sigils |
| `design/scripts/pixelkit/treenodes.py` | node states, lit connectors, reset |
| `design/scripts/pixelkit/treerelief.py`, `treeslab.py`, `treestone.py`, `treebars.py` | backdrops, grooves, seals, header, footer, off-page paths, loadout, slot maps |
| `design/scripts/zz_skill_tree_preview.py` | checks the pack and writes `target/previews/skills/` (not committed) |
| `resourcepack/assets/arkenmmo/textures/font/gui/{tree,loadout}_*.png` | 64 backgrounds as 128 tiles |
| `resourcepack/assets/arkenmmo/font/gui.json` | their providers, merged with the class menu's |
| `resourcepack/assets/arkenmmo/{textures/item,models/item,items}/gui/{skill,button}/` | 315 items |
| `design/scripts/titles.json` | title strings |

Several generators share `gui.json` and `titles.json`: `pack.write_font` and `pack.write_titles` merge, so run order does not matter.

## Dimensions
Background 352x444 art px (176x222 GUI). Item 32x32 (16x16 GUI). Icon 24x24 at item offset 4. Groove 8 px at item px 12..20. No 3D models, pivots or animations.

## For the coder

### Item models
Set `item_model` to `arkenmmo:` plus the key.

| Key | Count | When |
|---|---|---|
| `gui/skill/<class>/<skill>/{locked,available,confirm,owned}` | 18 skills per class | tree and loadout |
| `gui/skill/<class>/<core>/{owned,confirm}` | 1 per class | tree: `owned`; loadout: `confirm` while picked |
| `gui/skill/<class>/link/{h,v,corner_es,corner_sw}` | 4 per class | lit connector pieces; hide their tooltip |
| `gui/button/{reset,reset_confirm,reset_unavailable}` | 3, shared | slot 49 on every tree page |
| `gui/blank` (existing) | - | every painted clickable: footer buttons, sealed stones |

`<skill>` is the contract ID without the class prefix.

| Class | Node | `<skill>` | Stone | States |
|---|---|---|---|---|
| warrior | core | `cleave` | square with two bars | `owned`, `confirm` |
| warrior | guardian n1 | `shield_bash` | square (active) | all four |
| warrior | guardian n2 | `iron_hide` | octagon (passive) | all four |
| warrior | guardian n3 | `stalwart` | octagon (passive) | all four |
| warrior | guardian n4 | `challenging_shout` | square (active) | all four |
| warrior | guardian n5 | `second_wind` | octagon (passive) | all four |
| warrior | guardian n6 | `bulwark` | square (active) | all four |
| warrior | berserker n1 | `leaping_strike` | square (active) | all four |
| warrior | berserker n2 | `bloodthirst` | octagon (passive) | all four |
| warrior | berserker n3 | `fury` | octagon (passive) | all four |
| warrior | berserker n4 | `whirlwind` | square (active) | all four |
| warrior | berserker n5 | `relentless` | octagon (passive) | all four |
| warrior | berserker n6 | `execute` | square (active) | all four |
| warrior | duelist n1 | `lunge` | square (active) | all four |
| warrior | duelist n2 | `footwork` | octagon (passive) | all four |
| warrior | duelist n3 | `focus` | octagon (passive) | all four |
| warrior | duelist n4 | `riposte` | square (active) | all four |
| warrior | duelist n5 | `opportunist` | octagon (passive) | all four |
| warrior | duelist n6 | `hamstring` | square (active) | all four |
| archer | core | `vault` | square with two bars | `owned`, `confirm` |
| archer | marksman n1 | `power_shot` | square (active) | all four |
| archer | marksman n2 | `eagle_eye` | octagon (passive) | all four |
| archer | marksman n3 | `steady_aim` | octagon (passive) | all four |
| archer | marksman n4 | `piercing_shot` | square (active) | all four |
| archer | marksman n5 | `weak_spot` | octagon (passive) | all four |
| archer | marksman n6 | `hunters_mark` | square (active) | all four |
| archer | skirmisher n1 | `volley` | square (active) | all four |
| archer | skirmisher n2 | `fleet_foot` | octagon (passive) | all four |
| archer | skirmisher n3 | `momentum` | octagon (passive) | all four |
| archer | skirmisher n4 | `rapid_fire` | square (active) | all four |
| archer | skirmisher n5 | `light_step` | octagon (passive) | all four |
| archer | skirmisher n6 | `tumble` | square (active) | all four |
| archer | hunter n1 | `flame_arrow` | square (active) | all four |
| archer | hunter n2 | `tracker` | octagon (passive) | all four |
| archer | hunter n3 | `survivalist` | octagon (passive) | all four |
| archer | hunter n4 | `wolf_companion` | square (active) | all four |
| archer | hunter n5 | `barbed_heads` | octagon (passive) | all four |
| archer | hunter n6 | `frost_arrow` | square (active) | all four |
| mage | core | `blink` | square with two bars | `owned`, `confirm` |
| mage | pyromancer n1 | `fireball` | square (active) | all four |
| mage | pyromancer n2 | `kindling` | octagon (passive) | all four |
| mage | pyromancer n3 | `inner_heat` | octagon (passive) | all four |
| mage | pyromancer n4 | `flame_wave` | square (active) | all four |
| mage | pyromancer n5 | `ash_siphon` | octagon (passive) | all four |
| mage | pyromancer n6 | `meteor` | square (active) | all four |
| mage | frostweaver n1 | `ice_lance` | square (active) | all four |
| mage | frostweaver n2 | `chill_touch` | octagon (passive) | all four |
| mage | frostweaver n3 | `frost_armor` | octagon (passive) | all four |
| mage | frostweaver n4 | `frost_nova` | square (active) | all four |
| mage | frostweaver n5 | `shatter` | octagon (passive) | all four |
| mage | frostweaver n6 | `blizzard` | square (active) | all four |
| mage | lifebinder n1 | `mending_light` | square (active) | all four |
| mage | lifebinder n2 | `gentle_soul` | octagon (passive) | all four |
| mage | lifebinder n3 | `radiance` | octagon (passive) | all four |
| mage | lifebinder n4 | `sanctuary` | square (active) | all four |
| mage | lifebinder n5 | `smite` | octagon (passive) | all four |
| mage | lifebinder n6 | `sunburst` | square (active) | all four |
| captain | core | `rallying_strike` | square with two bars | `owned`, `confirm` |
| captain | vanguard n1 | `quarry_mark` | square (active) | all four |
| captain | vanguard n2 | `hardened_resolve` | octagon (passive) | all four |
| captain | vanguard n3 | `lead_from_the_front` | octagon (passive) | all four |
| captain | vanguard n4 | `press_the_attack` | square (active) | all four |
| captain | vanguard n5 | `gallant_example` | octagon (passive) | all four |
| captain | vanguard n6 | `scattering_shout` | square (active) | all four |
| captain | standard_bearer n1 | `plant_standard` | square (active) | all four |
| captain | standard_bearer n2 | `tall_colours` | octagon (passive) | all four |
| captain | standard_bearer n3 | `close_ranks` | octagon (passive) | all four |
| captain | standard_bearer n4 | `call_herald` | square (active) | all four |
| captain | standard_bearer n5 | `steadfast_company` | octagon (passive) | all four |
| captain | standard_bearer n6 | `sworn_bond` | square (active) | all four |
| captain | warchanter n1 | `war_ballad` | square (active) | all four |
| captain | warchanter n2 | `stirring_melody` | octagon (passive) | all four |
| captain | warchanter n3 | `long_refrain` | octagon (passive) | all four |
| captain | warchanter n4 | `anthem_of_courage` | square (active) | all four |
| captain | warchanter n5 | `clear_voice` | octagon (passive) | all four |
| captain | warchanter n6 | `coda` | square (active) | all four |

### Titles and glyphs
MiniMessage: `<!shadow><white><font:arkenmmo:gui>TITLE</font></white>`, 54 slots. The last column is the `titles.json` text (a double-quoted YAML string decodes it). Branch order is the footer tab order.

| Title key | Glyphs (TL TR BL BR, hex) | Title string |
|---|---|---|
| `tree_warrior_guardian_a` | `E201 E202 E203 E204` | `\uf804\ue201\uf801\ue202\uf808\uf806\uf805\uf801\ue203\uf801\ue204` |
| `tree_warrior_guardian_b` | `E205 E206 E207 E208` | `\uf804\ue205\uf801\ue206\uf808\uf806\uf805\uf801\ue207\uf801\ue208` |
| `tree_warrior_guardian_b_left` | `E301 E302 E303 E304` | `\uf804\ue301\uf801\ue302\uf808\uf806\uf805\uf801\ue303\uf801\ue304` |
| `tree_warrior_guardian_b_right` | `E305 E306 E307 E308` | `\uf804\ue305\uf801\ue306\uf808\uf806\uf805\uf801\ue307\uf801\ue308` |
| `tree_warrior_guardian_b_both` | `E309 E30A E30B E30C` | `\uf804\ue309\uf801\ue30a\uf808\uf806\uf805\uf801\ue30b\uf801\ue30c` |
| `tree_warrior_berserker_a` | `E209 E20A E20B E20C` | `\uf804\ue209\uf801\ue20a\uf808\uf806\uf805\uf801\ue20b\uf801\ue20c` |
| `tree_warrior_berserker_b` | `E20D E20E E20F E210` | `\uf804\ue20d\uf801\ue20e\uf808\uf806\uf805\uf801\ue20f\uf801\ue210` |
| `tree_warrior_berserker_b_left` | `E30D E30E E30F E310` | `\uf804\ue30d\uf801\ue30e\uf808\uf806\uf805\uf801\ue30f\uf801\ue310` |
| `tree_warrior_berserker_b_right` | `E311 E312 E313 E314` | `\uf804\ue311\uf801\ue312\uf808\uf806\uf805\uf801\ue313\uf801\ue314` |
| `tree_warrior_berserker_b_both` | `E315 E316 E317 E318` | `\uf804\ue315\uf801\ue316\uf808\uf806\uf805\uf801\ue317\uf801\ue318` |
| `tree_warrior_duelist_a` | `E211 E212 E213 E214` | `\uf804\ue211\uf801\ue212\uf808\uf806\uf805\uf801\ue213\uf801\ue214` |
| `tree_warrior_duelist_b` | `E215 E216 E217 E218` | `\uf804\ue215\uf801\ue216\uf808\uf806\uf805\uf801\ue217\uf801\ue218` |
| `tree_warrior_duelist_b_left` | `E319 E31A E31B E31C` | `\uf804\ue319\uf801\ue31a\uf808\uf806\uf805\uf801\ue31b\uf801\ue31c` |
| `tree_warrior_duelist_b_right` | `E31D E31E E31F E320` | `\uf804\ue31d\uf801\ue31e\uf808\uf806\uf805\uf801\ue31f\uf801\ue320` |
| `tree_warrior_duelist_b_both` | `E321 E322 E323 E324` | `\uf804\ue321\uf801\ue322\uf808\uf806\uf805\uf801\ue323\uf801\ue324` |
| `loadout_warrior` | `E281 E282 E283 E284` | `\uf804\ue281\uf801\ue282\uf808\uf806\uf805\uf801\ue283\uf801\ue284` |
| `tree_archer_marksman_a` | `E221 E222 E223 E224` | `\uf804\ue221\uf801\ue222\uf808\uf806\uf805\uf801\ue223\uf801\ue224` |
| `tree_archer_marksman_b` | `E225 E226 E227 E228` | `\uf804\ue225\uf801\ue226\uf808\uf806\uf805\uf801\ue227\uf801\ue228` |
| `tree_archer_marksman_b_left` | `E325 E326 E327 E328` | `\uf804\ue325\uf801\ue326\uf808\uf806\uf805\uf801\ue327\uf801\ue328` |
| `tree_archer_marksman_b_right` | `E329 E32A E32B E32C` | `\uf804\ue329\uf801\ue32a\uf808\uf806\uf805\uf801\ue32b\uf801\ue32c` |
| `tree_archer_marksman_b_both` | `E32D E32E E32F E330` | `\uf804\ue32d\uf801\ue32e\uf808\uf806\uf805\uf801\ue32f\uf801\ue330` |
| `tree_archer_skirmisher_a` | `E229 E22A E22B E22C` | `\uf804\ue229\uf801\ue22a\uf808\uf806\uf805\uf801\ue22b\uf801\ue22c` |
| `tree_archer_skirmisher_b` | `E22D E22E E22F E230` | `\uf804\ue22d\uf801\ue22e\uf808\uf806\uf805\uf801\ue22f\uf801\ue230` |
| `tree_archer_skirmisher_b_left` | `E331 E332 E333 E334` | `\uf804\ue331\uf801\ue332\uf808\uf806\uf805\uf801\ue333\uf801\ue334` |
| `tree_archer_skirmisher_b_right` | `E335 E336 E337 E338` | `\uf804\ue335\uf801\ue336\uf808\uf806\uf805\uf801\ue337\uf801\ue338` |
| `tree_archer_skirmisher_b_both` | `E339 E33A E33B E33C` | `\uf804\ue339\uf801\ue33a\uf808\uf806\uf805\uf801\ue33b\uf801\ue33c` |
| `tree_archer_hunter_a` | `E231 E232 E233 E234` | `\uf804\ue231\uf801\ue232\uf808\uf806\uf805\uf801\ue233\uf801\ue234` |
| `tree_archer_hunter_b` | `E235 E236 E237 E238` | `\uf804\ue235\uf801\ue236\uf808\uf806\uf805\uf801\ue237\uf801\ue238` |
| `tree_archer_hunter_b_left` | `E33D E33E E33F E340` | `\uf804\ue33d\uf801\ue33e\uf808\uf806\uf805\uf801\ue33f\uf801\ue340` |
| `tree_archer_hunter_b_right` | `E341 E342 E343 E344` | `\uf804\ue341\uf801\ue342\uf808\uf806\uf805\uf801\ue343\uf801\ue344` |
| `tree_archer_hunter_b_both` | `E345 E346 E347 E348` | `\uf804\ue345\uf801\ue346\uf808\uf806\uf805\uf801\ue347\uf801\ue348` |
| `loadout_archer` | `E285 E286 E287 E288` | `\uf804\ue285\uf801\ue286\uf808\uf806\uf805\uf801\ue287\uf801\ue288` |
| `tree_mage_pyromancer_a` | `E241 E242 E243 E244` | `\uf804\ue241\uf801\ue242\uf808\uf806\uf805\uf801\ue243\uf801\ue244` |
| `tree_mage_pyromancer_b` | `E245 E246 E247 E248` | `\uf804\ue245\uf801\ue246\uf808\uf806\uf805\uf801\ue247\uf801\ue248` |
| `tree_mage_pyromancer_b_left` | `E349 E34A E34B E34C` | `\uf804\ue349\uf801\ue34a\uf808\uf806\uf805\uf801\ue34b\uf801\ue34c` |
| `tree_mage_pyromancer_b_right` | `E34D E34E E34F E350` | `\uf804\ue34d\uf801\ue34e\uf808\uf806\uf805\uf801\ue34f\uf801\ue350` |
| `tree_mage_pyromancer_b_both` | `E351 E352 E353 E354` | `\uf804\ue351\uf801\ue352\uf808\uf806\uf805\uf801\ue353\uf801\ue354` |
| `tree_mage_frostweaver_a` | `E249 E24A E24B E24C` | `\uf804\ue249\uf801\ue24a\uf808\uf806\uf805\uf801\ue24b\uf801\ue24c` |
| `tree_mage_frostweaver_b` | `E24D E24E E24F E250` | `\uf804\ue24d\uf801\ue24e\uf808\uf806\uf805\uf801\ue24f\uf801\ue250` |
| `tree_mage_frostweaver_b_left` | `E355 E356 E357 E358` | `\uf804\ue355\uf801\ue356\uf808\uf806\uf805\uf801\ue357\uf801\ue358` |
| `tree_mage_frostweaver_b_right` | `E359 E35A E35B E35C` | `\uf804\ue359\uf801\ue35a\uf808\uf806\uf805\uf801\ue35b\uf801\ue35c` |
| `tree_mage_frostweaver_b_both` | `E35D E35E E35F E360` | `\uf804\ue35d\uf801\ue35e\uf808\uf806\uf805\uf801\ue35f\uf801\ue360` |
| `tree_mage_lifebinder_a` | `E251 E252 E253 E254` | `\uf804\ue251\uf801\ue252\uf808\uf806\uf805\uf801\ue253\uf801\ue254` |
| `tree_mage_lifebinder_b` | `E255 E256 E257 E258` | `\uf804\ue255\uf801\ue256\uf808\uf806\uf805\uf801\ue257\uf801\ue258` |
| `tree_mage_lifebinder_b_left` | `E361 E362 E363 E364` | `\uf804\ue361\uf801\ue362\uf808\uf806\uf805\uf801\ue363\uf801\ue364` |
| `tree_mage_lifebinder_b_right` | `E365 E366 E367 E368` | `\uf804\ue365\uf801\ue366\uf808\uf806\uf805\uf801\ue367\uf801\ue368` |
| `tree_mage_lifebinder_b_both` | `E369 E36A E36B E36C` | `\uf804\ue369\uf801\ue36a\uf808\uf806\uf805\uf801\ue36b\uf801\ue36c` |
| `loadout_mage` | `E289 E28A E28B E28C` | `\uf804\ue289\uf801\ue28a\uf808\uf806\uf805\uf801\ue28b\uf801\ue28c` |
| `tree_captain_vanguard_a` | `E261 E262 E263 E264` | `\uf804\ue261\uf801\ue262\uf808\uf806\uf805\uf801\ue263\uf801\ue264` |
| `tree_captain_vanguard_b` | `E265 E266 E267 E268` | `\uf804\ue265\uf801\ue266\uf808\uf806\uf805\uf801\ue267\uf801\ue268` |
| `tree_captain_vanguard_b_left` | `E36D E36E E36F E370` | `\uf804\ue36d\uf801\ue36e\uf808\uf806\uf805\uf801\ue36f\uf801\ue370` |
| `tree_captain_vanguard_b_right` | `E371 E372 E373 E374` | `\uf804\ue371\uf801\ue372\uf808\uf806\uf805\uf801\ue373\uf801\ue374` |
| `tree_captain_vanguard_b_both` | `E375 E376 E377 E378` | `\uf804\ue375\uf801\ue376\uf808\uf806\uf805\uf801\ue377\uf801\ue378` |
| `tree_captain_standard_bearer_a` | `E269 E26A E26B E26C` | `\uf804\ue269\uf801\ue26a\uf808\uf806\uf805\uf801\ue26b\uf801\ue26c` |
| `tree_captain_standard_bearer_b` | `E26D E26E E26F E270` | `\uf804\ue26d\uf801\ue26e\uf808\uf806\uf805\uf801\ue26f\uf801\ue270` |
| `tree_captain_standard_bearer_b_left` | `E379 E37A E37B E37C` | `\uf804\ue379\uf801\ue37a\uf808\uf806\uf805\uf801\ue37b\uf801\ue37c` |
| `tree_captain_standard_bearer_b_right` | `E37D E37E E37F E380` | `\uf804\ue37d\uf801\ue37e\uf808\uf806\uf805\uf801\ue37f\uf801\ue380` |
| `tree_captain_standard_bearer_b_both` | `E381 E382 E383 E384` | `\uf804\ue381\uf801\ue382\uf808\uf806\uf805\uf801\ue383\uf801\ue384` |
| `tree_captain_warchanter_a` | `E271 E272 E273 E274` | `\uf804\ue271\uf801\ue272\uf808\uf806\uf805\uf801\ue273\uf801\ue274` |
| `tree_captain_warchanter_b` | `E275 E276 E277 E278` | `\uf804\ue275\uf801\ue276\uf808\uf806\uf805\uf801\ue277\uf801\ue278` |
| `tree_captain_warchanter_b_left` | `E385 E386 E387 E388` | `\uf804\ue385\uf801\ue386\uf808\uf806\uf805\uf801\ue387\uf801\ue388` |
| `tree_captain_warchanter_b_right` | `E389 E38A E38B E38C` | `\uf804\ue389\uf801\ue38a\uf808\uf806\uf805\uf801\ue38b\uf801\ue38c` |
| `tree_captain_warchanter_b_both` | `E38D E38E E38F E390` | `\uf804\ue38d\uf801\ue38e\uf808\uf806\uf805\uf801\ue38f\uf801\ue390` |
| `loadout_captain` | `E28D E28E E28F E290` | `\uf804\ue28d\uf801\ue28e\uf808\uf806\uf805\uf801\ue28f\uf801\ue290` |

Blocks: tree upper and lower `E201-E278`, loadout `E281-E290`, lit lower variants `E301-E390`. In use elsewhere: `E001-E008`, `E101-E110`, shifts `F801-F809`, `F821-F829`.

### Which tree background
- Upper view: `tree_<class>_<branch>_a`.
- Lower view, by which paths from the upper view are lit (both ends owned):

| n2 and n4 owned | n3 and n6 owned | Title key suffix |
|---|---|---|
| no | no | `_b` |
| yes | no | `_b_left` |
| no | yes | `_b_right` |
| yes | yes | `_b_both` |

The incoming paths are painted in the title, because there is no slot above row 0. If a purchase, undo or reset on the lower view changes this table's result, the menu has to be reopened with the new title. Using only `_b` also works; the incoming paths then stay unlit. The paths leaving the upper view lead to sealed stones and are never lit in this release.

### Tree slot maps (`slot = row * 9 + column`)
| View | Stones | Connectors | Sealed (painted; add `gui/blank` with a tooltip that names no skill) |
|---|---|---|---|
| upper | 0 core, 4 n1, 20 n2, 24 n3, 38 n4, 40 n5, 42 n6 | 2 corner_es, 3 h, 5 h, 6 corner_sw, 11 v, 15 v, 29 v, 33 v, 39 h, 41 h | none |
| lower | 2 n4, 4 n5, 6 n6 | 3 h, 5 h | stones 20 (n7), 24 (n8), 40 (n9); grooves 11, 15, 29, 33, 38, 39, 41, 42 |

Slot 0 is the free core skill: always `owned`, upper view only.

| Edge | Upper slots | Lower slots |
|---|---|---|
| n1-n2 | 2, 3, 11 | - |
| n1-n3 | 5, 6, 15 | - |
| n2-n4 | 29 | in the title |
| n3-n6 | 33 | in the title |
| n4-n5 | 39 | 3 |
| n5-n6 | 41 | 5 |

Put an edge's pieces in only when both its ends are owned; otherwise leave those slots empty. The node rules are unchanged: n5 is the either-side middle passive.

Footer: 45 back, 46-48 branch tabs, **49 reset**, 50 scroll up, 51 scroll down, 52 loadout, 53 info. All but 49 are painted. The unusable scroll arrow (up on the upper view, down on the lower) is dark and should do nothing.

### Loadout menu slot map
| What | Slots |
|---|---|
| Combo seats 1-4, labels painted above | 10, 12, 14, 16 |
| Painted labels, Warrior, Mage, Captain | R-L-R, R-R-R, R-L-L, R-R-L |
| Painted labels, Archer (mirrored) | L-R-L, L-L-L, L-R-R, L-L-R |
| Pool: the 9 branch actives, tab order, each n1, n4, n6 | 27-35 |
| Core active | 40 |
| Back, info | 45, 53 (the rest of row 5 is plain; no reset here) |

A seat holds the assigned skill's `owned` item, or nothing when empty. A pool stone shows `owned` or `locked`; the picked one shows `confirm`. Proposed gesture (not decided): click an owned pool stone to pick it, then a seat to assign; click a filled seat with nothing picked to clear it.

### Menu behaviour approved with the A1 layout
- **Reset:** first click shows `reset_confirm`, lore gives the points returned and "Click again to reset"; any other click, a page change or closing cancels.
- **Undo:** clicking a stone bought during this opening shows its `confirm` art with "Click again to undo"; the second click refunds it, unless that would break the tree (say why in lore).
- `menu.Menu` needs a way to set or clear a slot with no click action (connectors, seats).

## Art
Actives are squares, passives octagons. One mask per skill; all states are generated from it.

| State | Look | Cue besides colour |
|---|---|---|
| locked | dull slate rune cut into dark stone, no ring | no ring, thinner rune |
| available | thin steel ring, slate rune | ring |
| confirm | pale rune, four corner brackets (gold; ivory for the Captain, whose glow is gold) | brackets |
| owned | class-colour ring, halo and rune, still | four rivets, lit connectors |
| sealed | rough plug with an askew iron band; the ultimate is wider with two bands and blank wax | irregular outline |

**Off-page paths:** on the upper view the grooves under n4 and n6 (columns 2 and 6) break through the footer ledge and end in a pale down-pointing head shaped like the scroll arrow; column 6 leads into the scroll-down button. On the lower view they enter through the header into n4 and n6, with up-pointing heads that match the scroll-up arrow. n5 has no connection across the view edge. To make room, all footer buttons are 4 art px shorter than in the A1 preview.

**Backdrops:** one layout; each class has its own carving. Warrior: helm over crossed axes, grave swords. Archer: antlered skull before crossed arrows, firs. Mage: pointed arch with a crystal, crowned staves. Captain: crowned war banner over crossed spears, pennon lances. The loadout has no carving.

## Palette (frozen; no additions)
| Class | Stone | Glow, dark to light | Gem |
|---|---|---|---|
| warrior | `ember_stone` 0-4 | crimson 0, crimson 1, crimson 2, crimson 3, crimson 4, crimson 5 | `crimson` |
| archer | `dusk_forest` 0-4 | forest 0, forest 1, forest 2, forest 3, forest 4, forest 5 | `forest` |
| mage | `night_teal` 1-5 | violet 0, violet 1, violet 2, violet 3, violet 4, violet 5 | `violet` |
| captain | `dawn_stone` 0-4 | leather 0, gold 0, gold 1, gold 2, gold 3, gold 4 | `navy` |

Shared: `iron`, `steel`, `gold`, `ivory`, `parchment`, `leather`. The Mage stone is `night_teal` steps 1-5. Hex values are in `pixelkit/palette.py`.

## Placeholders
All of this art, until the user approves it.

## Not verified
Simulated only, with no 26.3 client: item-over-title draw order, exact alignment, player rows, cursor position when a menu reopens, and the look at the user's GUI scale. GUI scale 3 samples the 2x art unevenly (1.5 px per art px). The vanilla panel, "Inventory" letters and player items in previews are stand-ins.
