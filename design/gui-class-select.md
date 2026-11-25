# Asset: class selection pages

**Status:** placeholder (page 1, waiting for the user's approval of the Warrior panel; the right panel is a deliberate placeholder)
**Brief:** `docs/briefs/classes.md`, task A1
**Pipeline:** plain vanilla resource pack, Paper 26.3. `pack.mcmeta` uses `min_format [97, 1]` and `max_format 97` ([Pack format](https://minecraft.wiki/w/Pack_format), 26.3 = 97.1, checked 2026-11-25). A 26.4 target needs a new check.
**Style:** `design/gui-style-guide.md`

## Purpose
The painted background of the class menu (a 9x6 chest): header, two class panels with name plates, the divider with page pips and the page arrow, and the player-inventory area. It is drawn as four bitmap font glyphs in the inventory title.

## Files
| File | What |
|---|---|
| `resourcepack/pack.mcmeta` | pack format 97.1 |
| `resourcepack/assets/arkenmmo/font/gui.json` | font `arkenmmo:gui`: the shifts plus two bitmap providers |
| `resourcepack/assets/arkenmmo/textures/font/gui/class_select_1_top.png` | 352x222: cells TL and TR |
| `resourcepack/assets/arkenmmo/textures/font/gui/class_select_1_bottom.png` | 352x222: cells BL and BR |
| `design/scripts/titles.json` | generated title strings, as `\uXXXX` escapes |
| `design/scripts/gui_class_select.py`, `design/scripts/pixelkit/` | generators (`mise run assets`) |
| `design/scripts/zz_gui_preview.py` | preview compositor, writes `target/previews/gui/` (not committed) |

There are no models, animations or pivots.

## For the coder
| Item | Value |
|---|---|
| Font | `arkenmmo:gui` |
| Page 1 glyphs (TL, TR, BL, BR) | `U+E001` `U+E002` `U+E003` `U+E004` |
| Shifts | `U+F801..U+F809` = -1, -2, -4 ... -256; `U+F821..U+F829` = +1 ... +256 |
| Page 1 title, in order | `F804 E001 F801 E002 F808 F806 F805 F801 E003 F801 E004` |
| Same as a string escape | `` |
| MiniMessage | `<!shadow><white><font:arkenmmo:gui>TITLE</font></white>` |
| Inventory | 54 slots |

- `TITLE` is the real characters, not the escape text, unless the config format decodes escapes (a double-quoted YAML string does).
- Title decoded: -8, TL, -1, TR, -177, BL, -1, BR. Page 2 (A2) swaps in `E005..E008` with the same shifts.
- After the title the pen is at GUI x 177 (not 8).
- Slots: left panel = columns 0-3 of rows 0-5; right panel = columns 5-8 of rows 0-5; page arrow = slots 40 and 49. Column 4 slots 4, 13, 22 and 31 do nothing.

## Dimensions
| Region | Art px (half-open) |
|---|---|
| Master | 352x444 (176x222 GUI); the last 2 rows are below the vanilla panel and clear |
| Header | y 0..34 |
| Left panel (click area) | x 14..158, y 34..250; frame from x 8 |
| Divider | x 158..194, y 34..250 |
| Right panel (click area) | x 194..338, y 34..250; frame to x 344 |
| Name plates | y 214..250 |
| Page arrow | x 158..194, y 178..250 |
| "Inventory" plate | x 10..180, y 252..274 (GUI 5..90, 126..137; the research note proposed 6..90, widened by 1 so the label does not touch the edge) |
| Player cells | 36x36 at x 14 + 36c; y 276, 312, 348; hotbar 392 |

No art overflows above or below the panel.

## Warrior panel
Great helm with ember eyes and a swept crimson crest, layered pauldrons with a steel horn, a crimson breastplate with a gold collar, a hooked cleaver hoisted over the right shoulder, a tower shield with a chevron and diamond, braced toward the centre. Backdrop: fortress at dusk, rays and a halo behind the helm, stone dais. Figure 124x158 art px, 22 colours; panel 39 colours; whole page 47; all from the frozen palette, no partial alpha.

## Placeholders
- The whole right panel (dim bow emblem and dim `ARCHER` plate). A2 replaces it.
- All Warrior art until the user approves it.

## Checked in the simulation, not in a client
The preview reads the real `font/gui.json`, PNGs and title string. The vanilla panel, "Inventory" letters and player items are our own stand-ins; no Mojang texture is used or committed, so the vanilla corner shape was **not** compared with `generic_54.png`. In game, still check: background alignment, player-row positions, the "Inventory" label on its plate, the corners, and the art at the GUI scales in use.
