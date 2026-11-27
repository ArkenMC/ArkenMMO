# Player inventory texture

Status: **waiting for the user's approval** (2026-11-27, fifth version: v4 plus a hairline grid with gold studs, bright gold sockets and a pillar down to the rule; v4 was the third version's regions plus ornament, after the user asked for more detail with Wynncraft's inventory as the reference). A deliberate vanilla override.

**Reference (v4):** Wynncraft's 2.1 inventory, studied from screenshots (Wynntils' bank gallery image and the Wynngineer's Vision and Wynn Darkmode re-theme galleries on Modrinth): an ornate outer case, gridless grouped regions, a dark recess behind the character, special slots set apart from the bar. We took the structure only; colours, shapes and every pixel are ours, in the menus' iron, parchment and gold.

| | |
|---|---|
| Files | `resourcepack/assets/minecraft/textures/gui/container/inventory.png`; `.../textures/gui/sprites/recipe_book/button.png` and `button_highlighted.png`; `.../textures/gui/sprites/container/slot/helmet.png`, `chestplate.png`, `leggings.png`, `boots.png` (our silhouettes) and `shield.png` (fully clear) |
| Generator | `design/scripts/gui_inventory.py` (art, recipe sprites and checks; rounded shapes in `pixelkit/rounded.py`, ornaments in `pixelkit/invdecor.py`), `design/scripts/gui_slot_icons.py` (empty-slot sprites and checks), `design/scripts/zz_inventory_preview.py` (previews) |
| Size | 512x512; art in the top-left **352x332** (vanilla 176x166 on the 2x grid), everything else alpha 0. Recipe sprites 40x36 (vanilla 20x18 GUI px on the 2x grid), alpha 0 everywhere; slot sprites 32x32 (vanilla 16x16), binary alpha |
| Look | the player-inventory area of the skill menus: iron shell with a bevelled rim, gridless recessed regions, parchment title plate with a gold gem, gold rule. Four flat regions: the character panel, the main inventory block, the hotbar bar and the crafting block (below). Every rounded corner uses one pixel-art recipe on the GUI pixel grid. Ornament (v4): gold corner brackets, an arched brick alcove behind the model, armour sockets, a fluted pillar, a crest medallion, a hairline grid with gold studs in the gridless regions. No class colour |
| Colours | 14, all from the frozen palette (iron 0-5, parchment, gold); alpha 0 or 255. Shell body `iron` 2 `#282a39`; region fill `iron` 3 `#3a3e50` (the crafting cells' floor); crafting block fill `iron` 1 `#1a1925`; region edge ring 1 art px, top/left `#0d0b14`, bottom/right `iron` 4 `#525869` |

## Layout (GUI px, top-left of each 18x18 cell; art px are double)
**Corner recipe (everywhere):** one pixel-art corner of 3-1-1 GUI px: the outermost row loses 3 px, the next two rows 1 px each, so the curve is made of whole GUI-pixel steps (2x2 art px) and it is its own mirror image. It rounds the shell's outline (the rim's 7 rings follow the steps), every region's outer corners, and, because the block is cut back from the panel by a 2 GUI px diamond, the L-block's inner corner (concentric, same stairs). Rings are counted along rows and columns, so they stay stairs.

Four flat recessed regions replace every cell frame except the crafting 2x2 and the result slot. A region reaches 1 GUI px beyond its cells where there is room. Edge: a 1 art px ring, dark top/left, `iron` 4 bottom/right, and a 1 GUI px inner shadow just inside the top and left (one step darker than the fill: `iron` 2, or `#0d0b14` in the crafting block). The shadow only lies in the margin outside the cells, never inside a cell, so item areas stay flat. The game still draws items and ghost icons at cell + 1.

| What | Position |
|---|---|
| Character panel | GUI box (6,6)-(78,100), fill `iron` 3, behind the armour sockets, the alcove, the first four storage cells (x 7 / 25 / 43 / 61 at y83) and the gap y79..83. 1 GUI px of extra fill on the top and left; the right and bottom edges stop 1 GUI px inside the cells (on the item areas' edge). **Its right edge is one straight line**, last filled art column 155 (GUI 77), centred on the column boundary x79 |
| Main inventory block | L-shape, fill `iron` 3: storage row y83 columns 4..8 and rows y101 / y119 columns 0..8; boxes (79,82)-(170,102) and (6,102)-(170,138), minus the panel grown by 2 GUI px. Outer corners cut with the recipe; the inner corner of the L is the panel's rounded corner grown, so it is filleted with the same stairs |
| Seam (gap) | between the panel and the block, vertically (x79) and horizontally (y101) and round the corner: lit ring (panel, art px 156), 2 art px of plain shell, dark ring (block, 159), then the block's fill from 160. The room comes from the cells' 1 GUI px margins: the panel ends at its item areas' edge and the block starts at its own. The item areas keep every pixel (apart from rounded-corner cuts in their outermost GUI px) |
| Hotbar bar | GUI box (6,140)-(151,160), fill `iron` 3, cells 1..8. The ninth cell (151,141) is outside it, plain shell colour, still usable. Gap to the block: ring, 2 art px shell, ring, the same as the seam |
| Crafting block | GUI box (96,16)-(171,54), fill `iron` 1 `#1a1925` (darker, so it reads as its own block), behind the 2x2, the arrow and the result. 1 GUI px under the title plate (1 art px of shell, then the ring); the plate has a 2 art px shadow (`iron` 1) to the right and below. No padding on the right (the result slot's ring sits at the edge) |
| Armour sockets | x7, y 7 / 25 / 43 / 61: framed `slot_cell` cells like the menus', on top of the panel |
| Alcove | GUI (25,7)-(77,79), behind the player model: `iron` 1 bricks (8x4 GUI px, running bond, `iron` 0 mortar, `iron` 2 lit top edge, a few chipped corners), a round arch (columns lost per row 7-5-3-2-2-1-1-1 GUI px) with `iron` 2 spandrels and a keystone with a small gold gem, a 2 art px recessed ring (dark top/left, `iron` 4 / `iron` 2 bottom/right), floor flags and a two-step dais whose top is at y71 (where the model's feet land, estimated), two iron sconces with gold flames at y ~24 |
| Pillar | art (162,14)-(186,160): fluted iron shaft with gold capital and base bands, the class menu divider's look, between the panel and the crafting block. Its base stands on the gold rule (its last row is the rule's top row), so it also runs over the offhand cell's item area (see Offhand) |
| Crest | centre art (267,134), under the crafting block: octagonal medallion (gold rim, `iron` 1 face, the class menu's gold crossed swords), gold blades tapering to each side with two gems each. It covers the hidden recipe button's area only with its left blade |
| Grid | a 1 art px line, `iron` 4 `#525869`, in the 2 GUI px margin between every two neighbouring gridless cells of one region (art column `2x-1` / row `2y-1` for the cell at x / y): 3 in the panel row, 4 + 8 + 8 vertical and 5 + 9 horizontal in the block, 7 in the bar. It is clipped to the region fill, spans each cell's rect and never enters an item area; it stops 2 art px short of the region edge |
| Studs | a gold stud (2x2 GUI px: `gold` 3 body, `gold` 4 top-left pixels, `gold` 2 bottom/right edge) on every corner where four gridless cells of one region meet: y101 between columns 4..8 and y119 across the block (12), on the grid's intersections. Never inside an item area |
| Ninth hotbar | (151,141): a framed socket with the same bright gold first ring as the result (`gold` 3 `#dca636` on all four sides), set apart from the bar |
| Corner brackets | the menus' gold L fittings (arm 11) on all four shell corners, over the rim |
| Offhand | (76, 61): no art, plain shell, except that the pillar (art x162..186) passes through the right part of its item area. The slot still exists: an item put there (F key) renders at (77,62) over the shell and the pillar, with the panel's right ring under its left edge |
| Crafting 2x2 | x 97 / 115, y 17 / 35: still framed `slot_cell` cells, unchanged |
| Crafting result | (153, 27); same cell with a bright gold first ring (`gold` 3 on all four sides; the bottom/right used to be `gold` 1 and read dark) |
| Title plate | (94,4)-(163,15), parchment with a gold gem at the right end, centred on the title's text rows y6..y13 |
| Arrow | gold block arrow, shaft from x135, tip at x151, centred on y35.5, unchanged |
| Gold rule | art y 158..161, from art x162 to 334, ending in a small gold gem at (339,159); between the crafting block and the main inventory; left of it is the panel's edge. It stays where it was: it sits under the offhand slot's item area, not over it |
| Shell shading | the rim's own top-left highlight (`iron` 5 / `iron` 4 rings) plus a 2 art px `iron` 1 shadow just inside the rim along the top and left |
| Recipe book button | hidden everywhere: both sprites are fully transparent (the button still clicks). The area (104,61)-(124,79) is plain shell colour |

All 46 cell origins were measured from InventivetalentDev/minecraft-assets@26.2 `inventory.png` (every 18x18 cell: 55 grey top-left ring, 139 grey floor, white bottom-right) and match the vanilla list in the script; 5 are drawn with frames (the crafting 2x2 and the result), 39 sit in a gridless region and 2 (offhand, ninth hotbar) are plain shell. The result slot is a plain 18x18 cell in 26.2, and the vanilla arrow is a grey 3-px shaft x135..149 with a head to x150. `recipe_book/button.png` exists in 26.2 and has no `.mcmeta`, so a plain sprite stretches to the drawn size.

## Slot sprites
Verified at InventivetalentDev/minecraft-assets@26.2 (`assets/minecraft/textures/gui/sprites/container/slot/`): `helmet.png`, `chestplate.png`, `leggings.png`, `boots.png`, `shield.png` all exist, are 16x16 and have no `.mcmeta` (404), so ours stretch to the drawn 16 GUI px. The vanilla icons are single-colour grey (`#555555`) outlines.
- Ours: original silhouettes (helmet with a visor slit, chestplate with a V neck and seam, leggings with a belt, a pair of boots), 1 art px `iron` 0 outline, body `iron` 5 `#747b8a`, bottom/right edge and details `iron` 4 `#525869`. Two steps lighter than the fill (`iron` 3; they were `iron` 4 and `iron` 3 until the fill was brightened, when they got too faint) and quieter than items. They are sprites, not painted into `inventory.png`, so they vanish under worn armour.
- They also draw in the creative survival tab's armour cells (cell floor `iron` 3, the same as the regions): the outline and `iron` 5 body read there too (preview `inventory_icons_on_creative_tab_x2.png`).
- `shield.png` is fully transparent (32x32), so the game's grey shield ghost does not appear on the plain shell where the offhand slot is. This also hides it in the creative survival tab's offhand cell (34,19), which is plain `iron` 3 floor there.

## Build check
`gui_inventory.py` fails the build when: the generated cell origins differ from the measured list; any art lies outside 352x332; alpha is not binary; the silhouette is not exactly the stepped shell outline or a corner is not clear; a colour is outside the palette; a framed cell (crafting, result) has an inner wall that is not exactly one art px inside its rect or no floor; **the shell outline or any region mask has a step off the GUI pixel grid** (rows and columns must come in identical pairs, i.e. every step is on an even art coordinate); the item area (cell + 1 GUI px, less its outermost GUI px) of any gridless panel, block or bar cell is not one flat fill colour; the offhand's item area is not plain shell colour (its first columns and the pillar's columns excepted); the result or ninth hotbar ring is not one `gold` 3 on all four sides; the pillar does not end on the gold rule; a grid line is missing in the sample cells; the alcove leaves the panel, touches an armour socket or does not fill the model box; a crafting cell is not inside the crafting block; a gridless cell is not inside exactly one region; the panel's right edge is not one straight line at art column 155; the seam between panel and block (art x156..159) is not free of block fill; any region has a square outer corner (listed corner pixels must be empty); regions overlap or are missing; the gold rule does not run from art x162 to x333; a recipe sprite is not 40x36 and fully transparent. `gui_slot_icons.py` fails when a sprite is not 32x32, alpha is not binary, a colour is outside the palette or equals the region fill (`iron` 3), a silhouette is not solid inside 2 px margins, two silhouettes are equal, or `shield.png` is not fully transparent.

## Unverified
- Title text position: **verified in game** (2026-11-27, the user's in-game screenshot): "Crafting" sits centred on the plate with `TITLE_PLATE` (94,4)-(163,15) (game draws it at GUI (97, 6), `#404040`, no shadow). The vanilla source itself was not re-read from 26.2.
- Recipe button position (about x104, y61) is from memory of the vanilla code. With both sprites clear it does not matter visually.
- A uniformly scaled 512x512 container texture: vanilla container backgrounds blit with an explicit 256x256 texture size, so the UVs are normalised and the file's real size should not matter (the same trick HD packs such as Faithful 64x use for the GUI), but this was not read from the 26.2 source or tested in game.
- The plate is deliberately wide for longer translations of the title; a very long one still overflows.
- The dais height (y71) assumes the model's feet land about 7 GUI px above the box's bottom; check in game and move `DAIS_TOP` if the feet float or sink.
- The game draws the empty armour ghost icons itself (ours, in the sprites) and the model on the panel; the in-game screenshot shows the model and icons reading well on `iron` 3. The stepped corners and the seam are judged from mock-ups at GUI scale 2 and 3.
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
