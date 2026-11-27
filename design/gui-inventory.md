# Player inventory texture

Status: **waiting for the user's approval** (2026-11-27, second version; no offhand section, themed armour icons). A deliberate vanilla override.

| | |
|---|---|
| Files | `resourcepack/assets/minecraft/textures/gui/container/inventory.png`; `.../textures/gui/sprites/recipe_book/button.png` and `button_highlighted.png`; `.../textures/gui/sprites/container/slot/helmet.png`, `chestplate.png`, `leggings.png`, `boots.png` (our silhouettes) and `shield.png` (fully clear) |
| Generator | `design/scripts/gui_inventory.py` (art, recipe sprites and checks; rounded shapes in `pixelkit/rounded.py`), `design/scripts/gui_slot_icons.py` (empty-slot sprites and checks), `design/scripts/zz_inventory_preview.py` (previews) |
| Size | 512x512; art in the top-left **352x332** (vanilla 176x166 on the 2x grid), everything else alpha 0. Recipe sprites 40x36 (vanilla 20x18 GUI px on the 2x grid), alpha 0 everywhere; slot sprites 32x32 (vanilla 16x16), binary alpha |
| Look | the player-inventory area of the skill menus: iron shell with a rounded, bevelled rim (corner radius 8 art px = 4 GUI px), recessed iron cells, parchment title plate with a gold gem, gold rule. One flat "character panel" (below). No class colour, no corner brackets (they clash with the rounded corners) |
| Colours | 14, all from the frozen palette (iron, parchment, gold); alpha 0 or 255. Panel fill `iron` 1 `#1a1925`; shell body `iron` 2 `#282a39`; panel edge: top/left `#0d0b14`, bottom/right `iron` 3 `#3a3e50` and `iron` 4 `#525869` |

## Layout (GUI px, top-left of each 18x18 cell; art px are double)
| What | Position |
|---|---|
| Character panel | one flat `iron` 1 region, no cell frames, covering: armour x7 y 7 / 25 / 43 / 61; model box outer (25,7)-(76,79); first four storage cells x 7 / 25 / 43 / 61 at y83; and the gap y79..83 between them. Silhouette: (7,7)-(76,79) plus the base (7,79)-(79,101), 1 GUI px of extra fill where there is room, outer corners rounded (radius 6 art px), the step where the narrower top meets the base filleted. There is no offhand tab. The bottom and right sides of the base are square: the cells below and beside it start there, so the panel's lip is those cells' own outer ring. Recessed 2-ring edge: dark top/left, lit bottom/right |
| Armour, storage 1..4 | no frame drawn; the game draws items and ghost icons at cell + 1 |
| Offhand | (76, 61): no art, plain shell colour (the panel's own edge reaches its first 4 GUI px). The slot still exists: an item put there (F key) renders at (77,62) over the shell |
| Crafting 2x2 | x 97 / 115, y 17 / 35 |
| Crafting result | (153, 27); same cell with a gold first ring |
| Main inventory | x = 7 + 18n (n 0..8), y 83 / 101 / 119; the first four of the top row belong to the panel, so 23 cells are drawn |
| Hotbar | x = 7 + 18n, y 141; the ninth (151,141) has no frame: plain shell colour, still usable |
| Title plate | (94,4)-(163,15), parchment with a gold gem at the right end, centred on the title's text rows y6..y13 |
| Arrow | gold block arrow, shaft from x135, tip at x151, centred on y35.5 |
| Gold rule | art y 160..163, from art x162 (GUI 81, 2 art px beyond the panel's right edge) to 345: it does not cross the panel |
| Recipe book button | hidden everywhere: both sprites are fully transparent (the button still clicks). The area (104,61)-(124,79) is plain shell colour |

## Slot sprites
Verified at InventivetalentDev/minecraft-assets@26.2 (`assets/minecraft/textures/gui/sprites/container/slot/`): `helmet.png`, `chestplate.png`, `leggings.png`, `boots.png`, `shield.png` all exist, are 16x16 and have no `.mcmeta` (404), so ours stretch to the drawn 16 GUI px. The vanilla icons are single-colour grey (`#555555`) outlines.
- Ours: original silhouettes (helmet with a visor slit, chestplate with a V neck and seam, leggings with a belt, a pair of boots), 1 art px `iron` 0 outline, body `iron` 4 `#525869`, bottom/right edge and details `iron` 3 `#3a3e50`. A few steps lighter than the panel (`iron` 1) and quieter than items. They are sprites, not painted into `inventory.png`, so they vanish under worn armour.
- They also draw in the creative survival tab's armour cells (cell floor `iron` 3): the outline and `iron` 4 body read there too (preview `inventory_icons_on_creative_tab_x2.png`).
- `shield.png` is fully transparent (32x32), so the game's grey shield ghost does not appear on the plain shell where the offhand slot is. This also hides it in the creative survival tab's offhand cell (34,19), which is plain `iron` 3 floor there.

36 cells are drawn. All 46 cell origins were measured from InventivetalentDev/minecraft-assets@26.2 `inventory.png` (every 18x18 cell: 55 grey top-left ring, 139 grey floor, white bottom-right) and match the vanilla list; the 10 not drawn are the 8 panel cells, the offhand and the ninth hotbar cell. The result slot is a plain 18x18 cell in 26.2, and the vanilla arrow is a grey 3-px shaft x135..149 with a head to x150. `recipe_book/button.png` exists in 26.2 and has no `.mcmeta`, so a plain sprite stretches to the drawn size.

## Build check
`gui_inventory.py` fails the build when: the generated cell origins differ from the measured list; any art lies outside 352x332; alpha is not binary; the silhouette is not exactly the rounded rectangle or a corner is not clear; a colour is outside the palette; a drawn cell's inner wall is not exactly one art px inside its rect (a one-pixel shift fails) or it has no floor; any of the 8 panel cells, the model box or the gap y79..83 is not one flat colour (panel fill), or the ninth hotbar cell or the offhand area (right of the panel's own edge) is not plain shell body; the gold rule does not run from art x162 to the right wall or reaches left of it; a recipe sprite is not 40x36 and fully transparent. `gui_slot_icons.py` fails when a sprite is not 32x32, alpha is not binary, a colour is outside the palette or equals the panel fill, a silhouette is not solid inside 2 px margins, two silhouettes are equal, or `shield.png` is not fully transparent.

## Unverified
- Title text position: the game draws "Crafting" at GUI (97, 6) in `#404040`, 8 px font, no shadow, and no "Inventory" label (`AbstractContainerScreen` defaults `titleLabelY = 6`; `InventoryScreen` only sets `titleLabelX = 97`). This is from knowledge of the vanilla source; it was not re-read from 26.2 because the network fetch failed. If the text sits elsewhere, move `TITLE_PLATE`.
- Recipe button position (about x104, y61) is from memory of the vanilla code. With both sprites clear it does not matter visually.
- A uniformly scaled 512x512 container texture: vanilla container backgrounds blit with an explicit 256x256 texture size, so the UVs are normalised and the file's real size should not matter (the same trick HD packs such as Faithful 64x use for the GUI), but this was not read from the 26.2 source or tested in game.
- The plate is deliberately wide for longer translations of the title; a very long one still overflows.
- The game draws the empty armour and offhand ghost icons itself, and the model on the panel's inner box; how they look on `iron` 1 is judged from a mock-up, not in game.
- The hidden recipe book button stays clickable (user decision); it also hides on the crafting table, furnace, smoker and blast furnace.

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
