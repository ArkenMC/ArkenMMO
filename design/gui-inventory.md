# Player inventory texture

Status: **waiting for the user's approval** (2026-11-26). A deliberate vanilla override.

| | |
|---|---|
| File | `resourcepack/assets/minecraft/textures/gui/container/inventory.png` |
| Generator | `design/scripts/gui_inventory.py` (art and checks), `design/scripts/zz_inventory_preview.py` (previews) |
| Size | 512x512; art in the top-left **352x332** (vanilla 176x166 on the 2x grid), everything else alpha 0 |
| Look | the player-inventory area of the skill menus: iron shell, recessed iron cells, parchment plate with a gold gem, gold rule, gold corner brackets. Built from `pixelkit/chrome.py` (`shell`, `slot_cell`, `gem`, `corner_bracket`). No class colour |
| Colours | 14, all from the frozen palette (iron, parchment, gold); alpha 0 or 255 |

## Layout (GUI px, top-left of each 18x18 cell; art px are double)
| What | Position |
|---|---|
| Armour | x7, y 7 / 25 / 43 / 61 |
| Offhand | (76, 61) |
| Crafting 2x2 | x 97 / 115, y 17 / 35 |
| Crafting result | (153, 27); same cell with a gold first ring |
| Main inventory | x = 7 + 18n (n 0..8), y 83 / 101 / 119 |
| Hotbar | x = 7 + 18n, y 141 |
| Player model box | black box (26,8)-(74,77); the recess outer frame is (25,7) to (75,78). Dark iron, a faint floor line 8 GUI px above the bottom. Keep it calm: the model draws on top |
| Title plate | (94,5)-(163,16), parchment with a gold gem at the right end, behind the title text the game draws ("Crafting" at 97, 8; unverified, see below) |
| Arrow | gold block arrow, shaft from x135, tip at x151, centred on y35.5 |
| Gold rule | art y 160..163, from art x7 to 345, between the crafting area and the main inventory |
| Recipe book button | about (104,61), 20x18: kept plain iron; the game draws the button sprite on top |

All 46 cell origins were measured from InventivetalentDev/minecraft-assets@26.2 `inventory.png` (every 18x18 cell: 55 grey top-left ring, 139 grey floor, white bottom-right) and match the list above. The result slot is a plain 18x18 cell in 26.2 (no larger frame), and the vanilla arrow is a grey 3-px shaft x135..149 with a head to x150. The model box outer ring is dark grey on the top and left, white on the bottom and right, and touches the offhand cell at x76.

## Build check
`gui_inventory.py` fails the build when: the generated cell origins differ from the measured list; any art lies outside 352x332; alpha is not binary (only the four 2x2 corner texels may be clear); a colour is outside the palette; a cell's inner wall is not exactly one art px inside its rect (a one-pixel shift fails); the model box holds more than its three iron tones; the recipe button area is not plain.

## Unverified
- Title text position and that no "Inventory" label is drawn in the survival inventory (believed `titleLabelX = 97`, `titleLabelY = 8` from memory; no source page found). If the text sits elsewhere, move `TITLE_PLATE`.
- Recipe button position (about x104, y61) is from memory of the vanilla code.
- A uniformly scaled 512x512 container texture: vanilla container backgrounds blit with an explicit 256x256 texture size, so the UVs are normalised and the file's real size should not matter (the same trick HD packs such as Faithful 64x use for the GUI), but this was not read from the 26.2 source or tested in game.
- The plate is deliberately wide for longer translations of the title; a very long one still overflows.

## Follow-up
The creative inventory (`creative_inventory/tab_inventory.png`) is not touched.
