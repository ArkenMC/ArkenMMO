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

# Creative inventory

Status: **waiting for the user's approval** (2026-11-26). Generator `design/scripts/gui_creative_inventory.py`, previews `design/scripts/zz_creative_preview.py`. Same look as the survival inventory (iron shell, `slot_cell`, parchment plate, gold gem and rule), no class colour.

## Files
| File | Size | Notes |
|---|---|---|
| `textures/gui/container/creative_inventory/tab_inventory.png` | 512x512, art 390x272 | survival tab: 41 cells, model recess, destroy slot. No title plate |
| `.../tab_items.png` | same | every category tab: 5 rows + hotbar, scroll track, title plate with gem and rule |
| `.../tab_item_search.png` | same | tab_items plus the search field; the plate is short so it stays clear of the field |
| `textures/gui/sprites/container/creative_inventory/scroller.png`, `scroller_disabled.png` | 24x30 | gold and iron handle |
| `.../tab_{top,bottom}_{selected,unselected}_{1..7}.png` | 52x64 each (28 files) | 26x32 GUI px |

The 30 sprites need no `.mcmeta`: vanilla has none for them (404 for every one at `minecraft-assets@26.2`), so they stretch to their drawn size.

## Layout (GUI px; 195x136 drawn area, cell = 18x18 top-left corner)
| What | Position |
|---|---|
| Item rows | x = 8 + 18n (n 0..8), y 17 / 35 / 53 / 71 / 89, hotbar y 111 (54 cells) |
| Survival tab | armour (53,5) (53,32) (107,5) (107,32); offhand (34,19); main rows y 53 / 71 / 89, hotbar y 111 (41 cells) |
| Destroy slot | cell (172,111); in vanilla its floor is red `#ab7f7f` with a dark X. Ours: darker iron floor and a steel X (shape, not colour) |
| Model box | black (73,6)-(104,48); outer ring (72,5)-(105,49), dark grey top and left, white bottom and right |
| Scroll track | outer (174,17)-(187,128), 14x112, floor 12 wide; the 12x15 scroller slides in it, y 18 + 95 * offset |
| Search field | outer (80,4)-(169,15); the game's edit box (unbordered) sits at (82,6), 80x9, white text |
| Title text | game draws it at (8,6) in the tab's label colour (`#404040`) when the tab shows a title |
| Plates | items (5,4)-(130,15), then a rule and a gem at the right edge; search (5,4)-(76,15), no gem |
| Gold rule | art y 216..219, between the main rows and the hotbar, ending 4 art px before the track |
| Tabs | top row y = -28, bottom row y = 132 (panel height - 4); column c at x = 27c for c 0..5, the seventh right-aligned at x = 169 (195 - 27 + 1) |

## Tabs
- Vanilla order: unselected tabs are drawn first (behind the panel), the panel, then the selected tab on top. The selected tab is panel-coloured and covers the panel's 4 GUI px edge, so it opens into the panel.
- Diffed all 28 vanilla sprites: tab 2..6 are identical in every set; tab 1 and tab 7 differ only in the 3 rows (top) or 3 rows (bottom) that overlap the panel, and only on the side that meets the panel's own wall (column 1 left, column 7 right). Unselected tabs are identical in all 7 positions. Selected top tab: rows 29-31 overlap, selected bottom: rows 0-2. Unselected top is opaque from row 2, unselected bottom to row 28.
- Ours: the same shapes at 2x. Selected: shell rim on top and sides with a gold crest line along the outer edge, open at the panel end (rows 56-63 / 0-7 overlap, the panel body runs through; tab 1 and 7 keep the panel's wall on the outer side). Unselected: one step darker iron (body iron 1), 2 px dark outline, corners cut by 2 and 1 GUI px.
- Tab icons: assumed drawn at tab x + 5, y + 9 (top) or + 6 (bottom); the mock uses that.

## Build check
`gui_creative_inventory.py` fails when: generated cells differ from the measured literal lists (54, 54, 41 + the destroy slot); any art outside 390x272; alpha is not binary or more than the four 2x2 corner texels are clear; a colour is outside the palette; a cell's inner wall is not exactly one art px inside its rect; a floor is wrong; the model box, scroll track or search field is not plain; the title plate reaches the search field; a sprite has the wrong size or non-binary alpha; tabs 2..6 differ or tab 1 / 7 do not differ. Colours: 9 (survival tab), 14 (items), 10 (search), 10 in all the sprites together; all palette.

## Unverified (creative)
- Draw positions: the 26.2 source was not available. Confirmed from NeoForge's patch of the 1.21.x `CreativeModeInventoryScreen` (unchanged vanilla context lines): title at (8,6) when `showTitle()`, tab y `topPos - 28` or `topPos + imageHeight - 4`, tab size 26x32, `27 * column` for the left-aligned tabs, scroller at its sprite size 12x15 positioned by `scrollOffs`, search box at (82,6) 80x9 unbordered, selected tab drawn through the sprite arrays. The right-alignment formula (x = imageWidth - 27 * (7 - column) + 1) and the order unselected, panel, selected are from memory, but fit the sprite diff exactly.
- Whether the survival tab and the search tab draw a title: believed from older versions that the survival tab hides it and search shows "Search Items". No plate is on the survival tab; if the game draws a title there, it is dark grey on dark iron.
- Long titles: items plate is 125 GUI px wide (about 110 px of text); the search plate fits "Search Items" only.
- Scaled sprites and textures: as for the survival inventory (not read from the 26.2 source).
- Open question for the user: destroy slot colour. Ours is neutral (no red). Option: a deep crimson floor behind the X, as a warning colour; the style guide keeps crimson for the Warrior class, so it is not used without a decision.
