# Asset: class selection menus

**Status:** placeholder until the user approves task A2 (A1 was approved before the "more minecraft ish" change)
**Brief:** `docs/briefs/classes.md`
**Pipeline:** plain vanilla resource pack, Paper 26.3. `pack.mcmeta` uses `min_format [97, 1]` and `max_format 97` ([Pack format](https://minecraft.wiki/w/Pack_format), 26.3 = 97.1, checked 2026-11-25). A 26.4 target needs a new check.
**Style:** `design/gui-style-guide.md`

## Purpose
Painted backgrounds for the six class menu screens (9x6 chests), four tooltip styles, an invisible slot highlight, the invisible clickable item and the pack icon.

## Files
| File | What |
|---|---|
| `resourcepack/pack.mcmeta`, `pack.png` | pack format 97.1; 128x128 icon with the four heads |
| `resourcepack/assets/arkenmmo/font/gui.json` | font `arkenmmo:gui`: shifts plus two bitmap providers per screen |
| `resourcepack/assets/arkenmmo/textures/font/gui/<screen>_{top,bottom}.png` | 352x222 each; screens `class_select_1`, `class_select_2`, `confirm_{warrior,archer,mage,captain}` |
| `resourcepack/assets/arkenmmo/textures/gui/sprites/tooltip/<class>_{background,frame}.png` (+ `.mcmeta`) | 100x100 tooltip sprites |
| `resourcepack/assets/arkenmmo/items/gui/blank.json` | `minecraft:empty` |
| `resourcepack/assets/minecraft/textures/gui/sprites/container/slot_highlight_{back,front}.png` (+ `.mcmeta`) | fully transparent, 24x24, nine-slice border 4 |
| `design/scripts/titles.json` | generated title strings as `\uXXXX` escapes |
| `design/scripts/gui_class_select.py`, `gui_items.py`, `pixelkit/` | generators (`mise run assets`) |
| `design/scripts/zz_gui_preview.py` | preview compositor, writes `target/previews/gui/` (not committed) |
| `design/scripts/reference/page1_approved_a1.png` | the approved A1 page, for the before/after view only (not in the pack) |

There are no 3D item models, animations or pivots: the heroes are rendered to flat PNGs by the scripts.

## For the coder
| Screen | Glyphs (TL, TR, BL, BR) | Title string |
|---|---|---|
| Class page 1 (Warrior, Archer) | `E001 E002 E003 E004` | `` |
| Class page 2 (Mage, Captain) | `E005 E006 E007 E008` | `` |
| Confirm Warrior | `E101 E102 E103 E104` | `` |
| Confirm Archer | `E105 E106 E107 E108` | `` |
| Confirm Mage | `E109 E10A E10B E10C` | `` |
| Confirm Captain | `E10D E10E E10F E110` | `` |

- MiniMessage: `<!shadow><white><font:arkenmmo:gui>TITLE</font></white>`. `TITLE` is the real characters, not the escape text, unless the config format decodes escapes (a double-quoted YAML string does). 54 slots.
- Title decoded: -8, TL, -1, TR, -177, BL, -1, BR. Afterwards the pen is at GUI x 177.
- Shifts: `U+F801..F809` = -1, -2, -4 ... -256; `U+F821..F829` = +1 ... +256.
- **Class pages:** left panel = columns 0-3, rows 0-5; right panel = columns 5-8, rows 0-5; page arrow = slots 40 and 49 (next on page 1, back on page 2). Slots 4, 13, 22 and 31 do nothing.
- **Confirm screens:** Confirm = columns 5-8, rows 1-2 (slots 14-17 and 23-26); Back = columns 5-8, rows 3-4 (slots 32-35 and 41-44). Columns 0-4 and rows 0 and 5 do nothing.
- Item model for the invisible clickable stacks: `arkenmmo:gui/blank`.
- Tooltip styles: `arkenmmo:warrior`, `arkenmmo:archer`, `arkenmmo:mage`, `arkenmmo:captain`.
- The slot highlight needs no code. It is hidden in **every** inventory while the pack is loaded.
- The art already shows "CHOOSE YOUR CLASS", the class names, "CONFIRM CHOICE", "THIS CHOICE IS FINAL", "CONFIRM" and "BACK". These are painted pixels, so changing config text does not change them.

## Dimensions (art px, half-open; 2 per GUI px)
| Region | Art px |
|---|---|
| Master per screen | 352x444 (176x222 GUI); the last 2 rows are below the vanilla panel and clear |
| Header | y 0..34 |
| Left panel (click area on pages) | x 14..158, y 34..250; frame from x 8 |
| Divider | x 158..194, y 34..250 |
| Right panel | x 194..338, y 34..250; frames and buttons reach x 344 |
| Name plates | y 214..250 |
| Page arrow | x 158..194, y 178..250 |
| Confirm / Back | y 70..142 / 142..214 (click areas x 194..338) |
| "Inventory" plate | x 10..180, y 252..274 (GUI 5..90; the research note proposed 6..90) |
| Player cells | 36x36 at x 14 + 36c; y 276, 312, 348; hotbar 392 |

No art overflows above or below the panel.

## Art
| Class | Figure (art px, colours) | Panel colours | Facing |
|---|---|---|---|
| Warrior | 122x157, 22 | 39 | right on page 1 and confirm |
| Archer | 131x150, 34 | 51 | left on page 1, right on confirm |
| Mage | 135x154, 32 | 45 | right on page 2 and confirm |
| Captain | 132x157, 30 | 44 | left on page 2, right on confirm |

## Placeholders
All of this art counts as placeholder until the user approves it.

## Checked in a simulation, not in a client
The preview reads the real `font/gui.json`, PNGs, `.mcmeta` files and title strings. The vanilla panel, the "Inventory" letters, player items and tooltip text are our own stand-ins. The tooltip placement (sprite drawn 12 GUI px outside the text) is from memory and unverified. Two vanilla tooltip sprites were downloaded to a scratch folder to measure their alpha geometry, then deleted; nothing of Mojang's is committed. `generic_54.png` was not compared. In game, check: alignment, player rows, the "Inventory" plate, corners, art at the used GUI scales, all four tooltips and the hidden highlight.
