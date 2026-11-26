# Custom inventory GUIs and pixel art (class selection, skill tree)

## Target version
**Paper 26.3** (`pom.xml`: `paper-api 26.3.build.205-stable`). Vanilla client plus our own pack. `pom.xml` and `paper-plugin.yml` declare no ItemsAdder or ModelEngine. The user has ItemsAdder installed; section 8 compares it and **recommends the plain pack**. Namespace: `arkenmmo`. Checked 2026-11-25.

**User decisions (2026-11-25):** class selection is paginated (2 classes per page, 2 pages, 6-row chest); the classes are Warrior, Archer, Mage and **Captain** (LOTRO-style commander with banners, marks and rallying, plus some Minstrel flavour); the pack may use whatever is best; no tests of any kind.

> **ItemsAdder on 26.3:** as of 2026-11-25 I found no stable release that supports it. Only 5.0.0 betas do (section 8). `docs/integrations.md` still says 4.1.0.

Evidence tags used below:
- **[V]** verified in an official source or the wiki for 26.x
- **[M]** measured or read from client bytecode on **26.1.2** by a third party ([materione gui.md](https://raw.githubusercontent.com/xef5000/materione/main/docs/architecture/gui.md)). Not re-checked on 26.3. I found no 26.2 or 26.3 note saying font metrics changed, but I did not read those changelogs in full.
- **[D]** derived by arithmetic from [V] or [M] facts
- **[U]** unverified. Check it in a real client before relying on it.

## Summary
1. Paint each menu background as **bitmap font glyphs in the inventory title** (font `arkenmmo:gui`), with white title colour and `space`-provider shifts. Author it at **2x density** (352x444 art px for the 176x222 GUI).
2. Put **items in the slots** for everything interactive or changing: invisible items (`minecraft:empty` model) for class sections, animated pane items for skill states and lit connectors. State changes then update slots without reopening.
3. The vanilla **hover highlight cannot be turned off per item or per menu** [U, no mechanism found]. Keep it, or restyle it globally.
4. pack.mcmeta uses `min_format [97,1]`, `max_format 97`. Send the pack as **required** through Adventure.
5. The art matters most: one texel grid, fixed ramps, light from the top left, and a render, look, revise loop with the checklist in section 6. Produce it with **Python/Pillow scripts that derive every position from the slot grid**, with a preview compositor (section 7).
6. Class selection is **2 pages of 2 large panels** (each 4 columns x 6 rows, 144x216 art px at 2x), one background per page (section 4). Use a **plain vanilla pack**, not ItemsAdder (section 8).

## Version notes
| Topic | 26.3 | What older guides say |
|---|---|---|
| Resource pack format | **97.1** [V] (26.1 = 84.0, 26.2 = 88.0) | `pack_format` integer. Not needed from format 65 on |
| Item textures | Own **items atlas** since 1.21.11, no mipmaps; one model cannot mix item and block atlases [V]. The 26.3 `atlases/items.json` stitches `textures/item/` [V] | blocks atlas |
| Custom items | `item_model` component and `assets/<ns>/items/*.json` [V] | `custom_model_data` overrides in vanilla models (obsolete) |
| Oversized GUI items | `oversized_in_gui`, default false means clipped to the slot [V]. Mojang does not officially support drawing outside the slot (MC-298139) [V] | display scale alone overflowed |
| GUI renderer | Rewritten in 1.21.6: layering follows submission order and bounds overlap [V] | z-offsets |
| Text shaders | Renamed in 26.2, changed again in 26.3 [V]. We use **no shaders** | many GUI tricks use `rendertype_text`; do not copy them |
| Window title updates | `InventoryView#setTitle` is deprecated and documented as broken; `title()` is read-only [V] | `setTitle` for animated GUIs |
| 26.3 other | Block model `shade` removed, `map_color` tint removed [V]. Neither affects flat GUI items | |

## 1. Background technique: title glyphs

### 1.1 Geometry of a 9x6 chest (GUI pixels, origin = panel top left)
| Element | Position |
|---|---|
| Panel | 176 x 222 (`imageHeight` = 114 + 6*18). Vanilla paints rows 0..220 [D] |
| Title pen origin | (8, 6), colour `0xFF404040` [M] |
| Chest slot (col c, row r), 16x16 item area | x = 8 + 18c, y = 18 + 18r [D, standard layout] |
| Chest slot 18x18 cell | x = 7 + 18c, y = 17 + 18r. Grid covers x 7..169, y 17..125 (162 x 108) |
| "Inventory" label | (8, 128), `0xFF404040`, drawn **after** the title, so on top of our art [M] |
| Player rows (3) item areas **[U]** | x = 8 + 18c, y = 139, 157, 175 (18x18 cells at y = 138, 156, 174) |
| Hotbar item areas **[U]** | y = 197 (cells at y = 196) |

The player rows follow the vanilla chest menu layout (first player row = 18 + rows*18 + 13) as I know it. I did not re-fetch it for 26.3. Before painting those cells, overlay them on the vanilla `generic_54.png`: its 6-row screen is image rows 0..124 followed by rows 126..221.

### 1.2 Font rules
- `bitmap` provider: `file`, `chars`, `ascent`, `height` (default 8). The image is divided evenly by row count and row length [V].
- **One glyph cell is at most 256 x 256 source pixels** [V][M] (257 shows the missing-glyph box on 26.1.2).
- **`ascent` <= `height`**, otherwise the **whole font file** fails to load [M]. Zero and negative ascents are valid [M].
- **Glyph top on screen (panel coordinates) = 13 - ascent** [M]. Panel top is `ascent: 13`.
- `height` is the drawn height in GUI px, so scale = height / cell pixel height. A 222 px tall cell with `height: 111` is 2x density [V][D]. Fractional resolution is only through this ratio.
- **Advance = trunc(0.5 + inkWidth * scale) + 1**. `inkWidth` is the rightmost column with alpha > 0, plus one [V for the ink rule][M for +1; rounding form U]. Keep drawn widths even at 2x.
- If a tile has a transparent right edge, put one pixel with alpha 1 in its last column so the advance stays fixed [D].
- `space` provider: `advances` maps a character to a float; negatives work in titles (they are forced to 0 only in chat) [V].
- Adjacent tiles need a **-1** shift between them [M].
- Art outside the panel is drawn, not clipped; only the window edge crops it. Clicks there do nothing [M].
- Title colour **multiplies** the texture, so set `<white>` [M]. Container titles have no shadow by default [U for 26.3]. Add `<!shadow>` anyway (equivalent to `<shadow:#00000000>`) [V].

### 1.3 Why 2x, not 1x or 4x
The font and items are sampled nearest-neighbour (standard behaviour, [U] as a documented guarantee). One art texel covers `guiScale / density` screen pixels.

| GUI scale | 1x | 2x | 4x |
|---|---|---|---|
| 2 | exact | exact | drops every 2nd texel |
| 3 | exact | **uneven (1.5)** | drops texels |
| 4 | exact | exact | exact |
| 5 | exact | uneven (2.5) | uneven |
| 6 | exact | exact | uneven |

GUI scale is capped at `min(floor(W/320), floor(H/240))` [M]. The maximum (what "Auto" picks) is 4 at 1920x1080, 6 at 2560x1440, 3 at 1280x720, 1366x768 and 1600x900 [D].

- **Recommendation: 2x.** It has four times the detail of 1x and is exact at the common even scales. At odd scales, 1 px lines vary in width, so keep important lines and lettering **at least 2 art px thick** wherever they must read well. Preview at 1.5x nearest as well.
- 1x is the safe retro option: exact at every scale, but a class panel is only 72x108 px.
- 4x (704x888) needs at least 12 tiles, shows artefacts at most scales, and stops looking like pixel art. Do not use it.
- Vanilla items, fonts and the highlight stay 1x. That is an accepted mixel boundary between "our art" and "game UI". **All of our art** (backgrounds, panes, connectors, tooltips if pixel-detailed) uses the 2x grid. Never mix 1x and 2x art inside our own images. The exception is tooltip nine-slices: see 2.3.

### 1.4 Tiling and font JSON
One 352x444 master, cut into two files of 352x222, each holding two 176x222 cells (both within 256).

`assets/arkenmmo/font/gui.json` (class page 1 shown; add the same two bitmap blocks, with new characters, for class page 2 and each other background):
```json
{
  "providers": [
    { "type": "space", "advances": {
      "": -1, "": -2, "": -4, "": -8, "": -16,
      "": -32, "": -64, "": -128, "": -256,
      "": 1, "": 2, "": 4, "": 8, "": 16,
      "": 32, "": 64, "": 128, "": 256 } },
    { "type": "bitmap", "file": "arkenmmo:font/gui/class_select_1_top.png",
      "ascent": 13, "height": 111, "chars": [""] },
    { "type": "bitmap", "file": "arkenmmo:font/gui/class_select_1_bottom.png",
      "ascent": -98, "height": 111, "chars": [""] }
  ]
}
```
`file` is relative to `textures/`, so the first PNG is `assets/arkenmmo/textures/font/gui/class_select_1_top.png`. Bottom ascent = 13 - 111 = -98 [D].

**Title string** (pen starts at panel x = 8; each tile's advance is 89):
```
                      -8, pen to panel x 0
          top-left, join, top-right (pen ends at 177)
    -177, back to x 0
          bottom-left, join, bottom-right
```
To add more glyphs or text afterwards, `` (-169) returns the pen to x = 8.

MiniMessage: `<!shadow><white><font:arkenmmo:gui>...</font></white>`. This is trusted config only, with no player input. A visible heading is best **painted into the art**. Default-font text after the glyphs works too, but sits on the title baseline only.

### 1.5 Layering, vanilla background, inventory area
- Order, bottom to top [M, 26.1.2]: screen dim, vanilla `generic_54` texture, **title glyphs**, **"Inventory" label**, highlight back, **slot items** and counts, highlight front, carried item, tooltip.
- Items draw above the art only where they **intersect the title's bounds** (the union of the glyph quads) [M]. **Invariant: every background spans the full 176x222**, so its bounds cover all slots.
- **Do not edit `textures/gui/container/generic_54.png`**; it changes every chest. Cover it with the glyph. The art must be **fully opaque over the whole vanilla panel shape** (176 x 221, with only the tiny rounded-corner pixels transparent), otherwise grey vanilla shows through. Check the corners against the vanilla PNG. The silhouette can grow outward but cannot shrink inward.
- Overflow budget [D]: at 720p scale 3 the GUI area is 427x240, leaving **9 px above and below** and about 125 px per side. Keep overflow at 8 px or less vertically and about 24 px or less per side (recipe viewer mods use the sides).
- **Player inventory:** the glyph covers it too, and players' real items render on top. Paint calm, dark, low-contrast slot cells there in the same frame style. Put no important art there. Do not put menu items into the player inventory (a risk of item loss, and it needs state restore).
- **"Inventory" label:** it cannot be removed per menu. Overriding the lang key `container.inventory` would affect all screens. Paint a **light plate** (parchment `#dcc291`) at about x 6..90, y 126..137 so the dark text reads. Translations vary in length, so give it room.

## 2. Invisible hoverable items

### 2.1 Model
`assets/arkenmmo/items/gui/blank.json`:
```json
{ "model": { "type": "minecraft:empty" } }
```
`minecraft:empty` renders nothing [V]. The stack still has a tooltip and clicks (standard slot behaviour). Item key: `arkenmmo:gui/blank`. Base material: `PAPER`, amount 1.

### 2.2 Tooltip control [V]
- `minecraft:tooltip_display`: `hide_tooltip` (boolean) and `hidden_components`.
- `ITEM_NAME` replaces the default name. `LORE` adds lines and is italic by default (see `docs/minimessage.md`).
- Every slot in one class section gets an **identical stack**, so the tooltip looks continuous as the mouse moves within the section.
- Filler or connector items that need no tooltip get `hideTooltip(true)`. This removes the tooltip only. **It does not remove the highlight** [U, no source says it does].
- With F3+H on, players also see the item id and component count. This is cosmetic.

### 2.3 Custom tooltip sprites (`tooltip_style`)
The component value `arkenmmo:warrior` resolves to `assets/arkenmmo/textures/gui/sprites/tooltip/warrior_background.png` and `warrior_frame.png`. A wrong id shows the missing texture [V].

Each PNG needs a `.png.mcmeta`. Vanilla 26.3 values [V] ([background](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/gui/sprites/tooltip/background.png.mcmeta), [frame](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/gui/sprites/tooltip/frame.png.mcmeta)):
```json
{ "gui": { "scaling": { "type": "nine_slice", "width": 100, "height": 100, "border": 9 } } }
```
```json
{ "gui": { "scaling": { "type": "nine_slice", "width": 100, "height": 100, "border": 10, "stretch_inner": true } } }
```
The first is the background, the second the frame. Vanilla's nine-slice `width`/`height`/`border` match 1x art, so author tooltips as **1x art**: author them at 100x100 on the 1x grid, copying the transparent margins of the vanilla PNGs. A 2x tooltip PNG is [U]. These sit on the text layer, so 1x is consistent there.

### 2.4 Hover highlight
- Since 1.21.2 it is two GUI sprites, `textures/gui/sprites/container/slot_highlight_back.png` and `slot_highlight_front.png`, each with a `.mcmeta`; both exist in 26.3 [V] ([listing](https://github.com/InventivetalentDev/minecraft-assets/tree/26.3/assets/minecraft/textures/gui/sprites/container)).
- By default it is a translucent light square on **one slot**, including over an invisible item, so a small square appears on top of the character art. Exact appearance over our art is [U].
- It **cannot highlight a whole section**, and the server gets **no hover event**.
- No per-item or per-menu switch was found for 26.x [U, absence]. Overriding the sprites affects **every inventory**.

| Option | Effect |
|---|---|
| A. Keep vanilla | No global change; a pale square over art |
| B. **Recommended:** subtle `back` (faint warm glow or corner ticks), fully transparent `front` | Applies globally but stays usable everywhere. `back` is behind items, so it shows over empty-model slots and is mostly hidden by opaque panes and items in normal inventories (weaker feedback there) |
| C. Both transparent | Cleanest art, but no highlight anywhere. Not recommended |

Option B is a **user decision**, because it changes vanilla inventories. If overriding, copy the vanilla `.mcmeta` and the 24x24 geometry from the 26.3 assets (contents not read here).

## 3. Skill sockets: items versus glyphs
| | Slot items (**recommended**) | Title glyphs |
|---|---|---|
| Change state | `inventory.setItem`, instant | Needs a new window; `setTitle` is deprecated [V] |
| Animation | `.png.mcmeta` [V] | None: fonts do not animate |
| Tooltip | Natural | Still needs an item |
| Size | 16x16 GUI, larger with `oversized_in_gui` | Any |

**Use glyphs only for the static background** (empty sockets and unlit connector tracks painted in). Use items for every state.

### 3.1 States (never colour alone)
| State | Look | Shape cue | Animation |
|---|---|---|---|
| `locked` | dim steel pane, skill icon nearly invisible or absent | padlock | none |
| `purchasable` | amber/gold rim, dim interior | bright corner ticks or small plus | pulse: 8 frames, `frametime` 3, about 1.2 s loop |
| `owned` | **filled glowing pane**, cyan-white core, top-left glass streak, skill icon bright | solid fill | slow shimmer: one long hold, then a diagonal streak |
| `excluded` (probably) | cracked dark crimson | diagonal slash or X | none |

Links: a lit item `link_h` or `link_v` placed in the connector slot; unlit = empty slot showing the painted track. Add a `link_<dir>_ready` variant only if the brief wants it. Corners and T-pieces are extra models, so fix the tree topology first. Connector items get `hideTooltip(true)`; the hover highlight still shows there.

Suggested grid (the game design research owns the topology): nodes on every other slot (columns 0,2,4,6,8, rows 0,2,4), connectors between them, row 5 for back, points and paging.

**Skill icons:** a "glowing pane" alone does not say which skill it is. If each skill needs an icon, use a `minecraft:composite` definition (pane model plus icon model) [V type exists]. Each skill and state is then one JSON file, so generate them by script. For the first version, shared state panes plus tooltips are the minimum.

### 3.2 Animated item texture
Vertical frame strip. At 2x: 32 wide, 32*N tall. `purchasable.png.mcmeta` [V]:
```json
{ "animation": { "frametime": 3, "interpolate": true } }
```
For the owned shimmer, use `frames` with per-frame `time`, for example `{"frames":[{"index":0,"time":50},1,2,3,4],"frametime":2}`. `interpolate` creates in-between colours, which is fine for glows; turn it off if edges look muddy. All items using one sprite animate in sync (a single atlas sprite, [U] but expected). No flashing faster than about 3 per second.

### 3.3 Item definition, model, oversize
`assets/arkenmmo/items/gui/skill/owned.json`:
```json
{ "model": { "type": "minecraft:model", "model": "arkenmmo:item/gui/skill/owned" } }
```
`assets/arkenmmo/models/item/gui/skill/owned.json`:
```json
{
  "parent": "minecraft:item/generated",
  "gui_light": "front",
  "textures": { "layer0": "arkenmmo:item/gui/skill/owned" }
}
```
Texture: `assets/arkenmmo/textures/item/gui/skill/owned.png`. It must be under `textures/item/`. 32x32 art fills the 16x16 slot.

Oversized (links bridging the 2 px gap between slots, or a glow halo): add `"oversized_in_gui": true` at the **top level of the items JSON**, and in the model `"display": {"gui": {"scale": [1.125, 1.125, 1]}}` with a 36x36 texture (18x18 GUI). A 24x24 halo uses scale 1.5 and 48x48. Limits: scale <= 4, translation -80..80, element coordinates -16..32 [V].

Cautions: not officially supported [V]; neighbour overlap order is unspecified [U]; one pack reports UV scaling errors and a missing top pixel row on oversized models (versions unstated) ([GUItem](https://modrinth.com/resourcepack/guitem)); oversized plus animation is [U]. **Design so that a clipped 16x16 version is still acceptable.** Prototype one pane and one link first. Fallback: 16x16 links with the 2 px gap painted as socket bridges in the background.

**Per-class pane colour:** either separate PNGs, or a greyscale pane with `"tints": [{"type":"minecraft:custom_model_data","index":0,"default":16777215}]` driven by the `custom_model_data` colors list [V]. Tinting multiplies one colour and destroys hue-shifted ramps, so **prefer hand-coloured PNGs**.

**Enchantment glint override: do not use it for state.** It is the fixed vanilla shimmer; its colour is global and it clashes with the palette. It shows nothing useful on an empty model [U].

## 4. Layouts and canvas sizes

### 4.1 Class selection: 2 pages, 2 panels per page (decided)
Each page has two tall panels of 4 columns x 6 rows, with column 4 as the divider. The page is symmetric about x = 88. Ranges below are half-open (`7..79` = pixels 7 to 78).

| Region | Columns | GUI x | GUI y | Raw slots (row*9 + col) | At 2x: art x, y |
|---|---|---|---|---|---|
| Header | - | 0..176 | 0..17 | none | 0..352, 0..34 |
| Left panel | 0-3 | 7..79 | 17..125 | cols 0-3, rows 0-5 (24) | 14..158, 34..250 |
| Divider | 4 | 79..97 | 17..125 | 4, 13, 22, 31, 40, 49 | 158..194, 34..250 |
| Right panel | 5-8 | 97..169 | 17..125 | cols 5-8, rows 0-5 (24) | 194..338, 34..250 |

| Piece (w x h) | 1x | **2x** | 4x (reference only) |
|---|---|---|---|
| Full background | 176x222 | **352x444** | 704x888 |
| Panel | 72x108 | **144x216** | 288x432 |
| Character area (y 17..107) | 72x90 | **144x180** | 288x360 |
| Name plate (y 107..125, bottom slot row) | 72x18 | **144x36** | 288x72 |
| Divider | 18x108 | **36x216** | 72x432 |
| Header | 176x17 | **352x34** | 704x68 |

- Figure about **100-124 art px wide and 140-168 tall**. Banner, staff or bow may use all 180 px. Keep at least 6 px of backdrop on most sides so the silhouette reads.
- Name plate lettering: custom pixel capitals about **12x16 art px, 3 px strokes, 2 px gap**. "WARRIOR" and "CAPTAIN" are 96 px wide and fit with ornament.
- Panel frames take about 4-6 art px inside each edge. They may extend 3 GUI px outward on the outer edges (x 4..7 and 169..172) without changing the click area. Nothing crosses into the other panel.
- The header holds a painted title ("CHOOSE YOUR CLASS") and a crest, with at most 8 GUI px overflow above the panel.
- Suggested pairing (design may change it): page 1 Warrior and Archer, page 2 Mage and Captain.
- All 24 slots of a panel get the same blank stack with that class's tooltip and `tooltip_style`.

### 4.2 Page arrows
Only real chest slots give a usable click. Outside the window, the click event has no coordinates, so arrows painted there cannot work. The player inventory is not usable either (section 1.5). That leaves the **divider column**:

| Choice | Slots | Notes |
|---|---|---|
| **Recommended:** one arrow per page | 40 and 49 together (rows 4-5) | Page 1 shows "next" (right arrow), page 2 "back" (left arrow). Target 18x36 GUI (36x72 art). Page pips go higher in the pillar |
| Two arrows | back = 40, next = 49 | Each 18x18 GUI; the unavailable one is painted dim and does nothing. Stacked left and right arrows read less naturally |

**Paint the arrow into that page's background** and put `arkenmmo:gui/blank` items on its slots with a "Next page" or "Previous page" tooltip. No arrow item model is needed. Slots 4, 13, 22 and 31 stay empty and show the highlight when hovered, like any empty slot.

### 4.3 Building the paging
- **One full background per page**, with its own glyphs and the same geometry:

| Page | Glyphs (TL, TR, BL, BR) | Files in `textures/font/gui/` |
|---|---|---|
| 1 | `E001 E002 E003 E004` | `class_select_1_top.png`, `class_select_1_bottom.png` |
| 2 | `E005 E006 E007 E008` | `class_select_2_top.png`, `class_select_2_bottom.png` |

- All four providers sit in the one `font/gui.json`: both `_top` files use `ascent 13`, both `_bottom` files `ascent -98`, all `height 111`. The title string follows section 1.4; page 2 swaps in `E005..E008`.
- The frame, header, divider and inventory area come from the same script function on both pages, so they are pixel-identical and only panels, pips and arrow change.
- **Switching page = a new inventory** with the other title, filled before opening, opened on the next tick. Do not call close first, and do not use `setTitle` (section 5.4). Cursor position staying put is [U].
- The old inventory fires `InventoryCloseEvent` with reason `OPEN_NEW` [V constant exists]. If the menu is forced (reopens when the player closes it), do not treat `OPEN_NEW` as a close.
- The holder stores the page number. The slot-to-action map is built per page.

### 4.4 Skill tree at 2x
Socket frame in the background: 36x36 at art position (2*(7+18c), 2*(17+18r)). A 32x32 pane item fills art (2*(8+18c), 2*(18+18r)). The frame is therefore a 2 art px ring; a heavier bevel may extend outward into empty neighbouring gutters. Unlit track: 8 art px wide, centred on the slot's centre line.

## 5. pack.mcmeta, delivery, plugin side

### 5.1 pack.mcmeta [V]
`resourcepack/pack.mcmeta`:
```json
{
  "pack": {
    "description": "ArkenMMO",
    "min_format": [97, 1],
    "max_format": 97
  }
}
```
No `pack_format` and **no `supported_formats`** (from format 65 on). The integer `max_format` 97 accepts any 97.x. 26.4 will need a bump.

### 5.2 Pack file layout
```
resourcepack/
  pack.mcmeta
  pack.png
  assets/arkenmmo/
    font/gui.json
    textures/font/gui/class_select_{1,2}_{top,bottom}.png  352x222 each
    textures/font/gui/skill_tree_{top,bottom}.png        352x222 each
    textures/gui/sprites/tooltip/<style>_{background,frame}.png (+ .mcmeta)
    textures/item/gui/skill/<state>.png (+ .mcmeta if animated)
    textures/item/gui/skill/link_{h,v}.png
    items/gui/blank.json
    items/gui/skill/<state>.json, link_h.json, link_v.json
    models/item/gui/skill/<state>.json, link_h.json, link_v.json
  assets/minecraft/textures/gui/sprites/container/       only for highlight option B
    slot_highlight_{back,front}.png (+ .mcmeta)
```
Art sources and previews belong in `design/`, never in `resourcepack/` (`tools/pack.py` zips every file there).

### 5.3 Delivery
- Adventure [V] ([docs](https://docs.papermc.io/adventure/resource-pack/), [builder Javadoc](https://jd.advntr.dev/api/latest/net/kyori/adventure/resource/ResourcePackRequest.Builder.html)): `ResourcePackInfo.resourcePackInfo().id(uuid).uri(uri).hash(sha1Hex).build()`, then `ResourcePackRequest.resourcePackRequest().packs(info).required(true).replace(false).prompt(component).callback(cb).build()`, then `audience.sendResourcePacks(request)`. (`id(...)`: the docs mention the UUID but do not show the setter [U]; the IDE will confirm.)
- **When:** preferably in `AsyncPlayerConnectionConfigureEvent`, so the pack is loaded before the player sees the world. Use `event.getConnection().getAudience()`. The connection continues when the handler returns [V]. To wait, block that **async** event on a `CompletableFuture` completed by the pack callback on a final status, with a timeout. Paper's [dialog docs](https://docs.papermc.io/paper/dev/dialogs/) show this blocking pattern for dialogs; applying it to packs is [U]. Never block on the main thread. Complete the future on disconnect too.
- [Paper #12865](https://github.com/PaperMC/Paper/issues/12865): `getResourcePackStatus()` stayed null for configure-phase packs. It was closed by PR #12866 (July 2025), so 26.3 should include the fix [U]. Tracking the callback result yourself is safer. Proxy setups have had configure-phase pack problems ([Velocity #1164](https://github.com/PaperMC/Velocity/issues/1164)).
- Statuses [V]: ACCEPTED and DOWNLOADED are intermediate. SUCCESSFULLY_LOADED, DECLINED, FAILED_DOWNLOAD, FAILED_RELOAD, INVALID_URL and DISCARDED are treated as final (that grouping is by their meaning). Client reports can be wrong or missing [V].
- `server.properties` alternative [V]: `resource-pack`, `resource-pack-id`, `resource-pack-sha1`, `require-resource-pack`, `resource-pack-prompt`; 250 MiB limit. Use one method, not both.
- Hosting: any direct-download HTTPS URL. `mise run pack` prints the SHA-1. Put url, sha1 and id in the first section of `config.yml`. Use a new URL per build (put the hash in the file name) and keep the UUID stable so clients refetch correctly [U, cache practice].

### 5.4 Paper 26.3 API
- `DataComponentTypes` [V] ([Javadoc](https://jd.papermc.io/paper/26.3/io/papermc/paper/datacomponent/DataComponentTypes.html)): `ITEM_MODEL` (Key), `ITEM_NAME` (Component), `LORE` (ItemLore), `TOOLTIP_STYLE` (Key), `TOOLTIP_DISPLAY` (TooltipDisplay), `CUSTOM_MODEL_DATA`, `ENCHANTMENT_GLINT_OVERRIDE` (Boolean). None is marked experimental.
- `TooltipDisplay.tooltipDisplay().hideTooltip(true).build()` [V].
```java
ItemStack stack = ItemStack.of(Material.PAPER);
stack.setData(DataComponentTypes.ITEM_MODEL, Key.key("arkenmmo", "gui/blank"));
stack.setData(DataComponentTypes.ITEM_NAME, name);
stack.setData(DataComponentTypes.TOOLTIP_STYLE, Key.key("arkenmmo", "warrior"));
```
- Open with `Bukkit.createInventory(holder, 54, titleComponent)` (a custom `InventoryHolder` identifies the menu; never match on the title). `MenuType.GENERIC_9X6.create(player, title)` plus `openInventory(view)` is the other route [V].
- While a menu is open: cancel **all** `InventoryClickEvent`s (including bottom-inventory shift-click, number keys, offhand swap, double-click) and `InventoryDragEvent`. Act only when `getRawSlot()` is 0..53, mapped by slot index. Check permission and eligibility again on every click. Defer open and close calls from click handlers to the next tick.
- State change: rewrite slots in place. A different background (class tree or page art) means opening a new inventory. The cursor normally stays put when one container directly replaces another [U]; do not call close first.
- **Without the pack**, titles show missing glyphs and items show the missing model. Require the pack, and do not open these menus unless it loaded (or offer a plain fallback only if the brief asks).

## 6. Pixel art style guide

### 6.1 Direction
Chunky **faceted blocky** characters: built from large flat planes (prisms and bevelled boxes), crisp edges, one colour identity each, heroic three-quarter pose, name banner below. Think "painted voxel miniature" rather than anime sprite. Do not copy or trace Mojang textures or other games' art.

### 6.2 Core rules
Definitions follow the [Pixel Joint tutorial](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) and [Derek Yu](https://www.derekyu.com/makegames/pixelart.html). The numbers are project proposals.
1. **One grid:** 2x for all our art. Draw at native size. No scaled-up, rotated or smoothly resized parts (mixels). Preview with nearest neighbour only.
2. **Silhouette first:** fill the figure solid black. All four classes must be tellable apart at 1x GUI size. Give each a different dominant shape (table below).

| Class | Dominant shape | Must have | Must not have |
|---|---|---|---|
| Warrior | **Wide, low, square**: huge pauldrons, planted stance, head sunk into the shoulders | closed or visored helm; tower shield or heavy two-handed blade held low or across | banner, flowing cape, bare face |
| Archer | **Slim diagonal**: side-on lunge | large bow arc, pointed hood, quiver over the shoulder | bulky armour |
| Mage | **Tall triangle**: narrow top, flared robe base | hat or deep hood, staff with a glowing orb, floating shard or flame | visible armour plates |
| Captain | **Tall vertical plus sweep**: a banner pole rising well above the head with a swallowtail flag, upright chest-out stance, one arm raised or pointing in a rally | **banner** with a simple emblem (this emblem doubles as the "mark" motif); open helm with plume or circlet and a **visible face**; half-cape swept to one side; **war horn** at the hip or in the free hand (the Minstrel note, optionally with a few rally arcs or notes) | tower shield, oversized pauldrons, raised heavy blade (a sword stays sheathed or small) |

Warrior against Captain is the main confusion risk, because both are armoured. Separate them four ways: **outline** (wide block against tall pole and cape), **value** (Warrior dark, Captain the brightest figure), **hue** (crimson and steel against gold, ivory and navy) and **gesture** (braced to fight against calling allies forward).
3. **One light:** key light from the **top left**, about 45 degrees, everywhere (characters, frames, panes, icons). Each box shows 3 values: top = light, front = mid, side or underside = shadow. An optional 1-2 px class-coloured rim light on the lower right separates the figure from the backdrop.
4. **Ramps:** use only palette colours. At most about 5 steps per material and **about 24-28 colours per character**; at most about 64 for a whole panel. **Hue shift:** shadows move toward blue or purple and gain some saturation, highlights toward yellow and lose some. SLYNYRD suggests up to about 20 degrees per step, with saturation peaking mid-ramp ([Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)).
5. **Value structure:** background darkest and least saturated (about value 15-30 %), character mid to high, the strongest contrast at the face, weapon and emblem. The greyscale version must still read.
6. **Clusters:** every pixel belongs to a shape. No orphan pixels except deliberate glints. Prefer a few large planes over texture noise.
7. **Lines:** steady step patterns (1:1, 2:1, 3:1; curve runs change monotonically, like 4,3,2,1,1,2,3,4). No jaggies or accidental L corners.
8. **Outlines (selective):** 2 art px outer outline in a very dark version of the local ramp, lighter or broken on lit edges, solid on shadow edges. We know the backdrop, so shaping against it is safe. Inner lines use the darker step of the nearer material, not black.
9. **Anti-aliasing:** by hand, inner edges and shallow curves only, with 1-2 intermediate ramp colours. None on clean 45-degree, horizontal or vertical edges. Binary alpha (0 or 255) on characters and frames. Partial alpha only for glows.
10. **Dithering:** sparing, only to taper a transition or texture large cloth, stone or backdrop areas, between close values. Never on faces or small parts.
11. **Avoid:** pillow shading (rings that follow the outline), banding (parallel bands with aligned ends, or an outline hugging a shading band), straight ramps, pure `#000000` and large pure white, soft gradients, blur, auto-smoothing, and noisy random texture.

### 6.3 GUI frames
- Layers from outside in: 2 px darkest outline, 4-6 px bevelled metal or wood band (light on top and left, dark on bottom and right), 2 px inner shadow, recessed panel.
- Recesses (sockets, slots) reverse the bevel: dark top and left, light bottom and right.
- Ornament goes on corners, the header crest and the divider pillar only. Quiet areas make the characters stand out. Mirror the ornament shapes but **redo the shading** so light stays top left.
- Name plates: banner or plaque in the class ramp with notched ends; letters in `#eef0ec` or gold with a 2 px dark drop edge.
- Panel backdrop: a dark class-tinted vertical value step (at most 3 values, dithered edges), a faint large emblem, and a ground shadow or plinth.

### 6.4 Proposed palette (dark to light)
These were authored for this note. They have **not been checked visually**; the artist may tune them in the first preview and then freezes them in `design/`.

| Ramp | Hex |
|---|---|
| Warrior crimson | `#2b0f1e` `#561826` `#8a2430` `#bd3a32` `#e06a3c` `#f4a65a` |
| Archer forest | `#0f2228` `#173a33` `#24573a` `#3f7a3c` `#6fa043` `#b4c95a` |
| Mage violet | `#170f33` `#281a5c` `#3d2c8f` `#5a49c4` `#7b7ce8` `#a9b8fa` |
| Mage arcane accent | `#1f6f9e` `#35b5c9` `#8ff0e4` |
| Captain gold | `#33201c` `#5f3d1a` `#956616` `#c8951f` `#eec33c` `#fde98a` |
| Captain ivory (tabard, banner field) | `#6e6a7e` `#aaa5a8` `#ddd6c4` `#f7f1dc` |
| Captain navy (secondary) | `#101433` `#1b2658` `#2b3f82` `#425fae` |
| Shared steel and neutrals | `#12101c` `#232436` `#3b4058` `#5c6580` `#8a94a8` `#bcc4cf` `#eef0ec` |
| Leather and wood | `#26141a` `#45251f` `#6b3d27` `#94603a` `#bd8a55` |
| Skin A | `#4a2430` `#7d3f3a` `#b06a4e` `#d9976b` `#f2c498` |
| UI gold trim | `#3d2415` `#6e4318` `#a8721f` `#dca636` `#f6d86b` `#fff3b8` |
| Parchment | `#8c6a4a` `#b99768` `#dcc291` `#efdcb0` |

Per class, as shares of the figure:

| Class | Identity (about 50-60 %) | Support (about 30 %) | Accent (about 10 %) |
|---|---|---|---|
| Warrior | crimson | dark steel | a little UI gold |
| Archer | forest | leather and wood | pale feather (`#dcc291`, `#efdcb0`) |
| Mage | violet | darker violet and leather | arcane cyan |
| Captain | gold (armour trim, banner, plume) with ivory | navy (cape, under-layer), bright steel | `#eef0ec` glints on the horn and banner finial; no crimson |

Captain uses gold because it is far from violet, forest and crimson in hue and value, and reads as "leader". Its gold overlaps the UI gold trim, so keep the Captain panel frame darker (steps 2-4) than the figure.

Skill states: locked = steel steps 2-4; purchasable = UI gold; owned = arcane accent plus `#eef0ec`; excluded = crimson steps 1-3. In the Captain tree, shape cues keep "purchasable" distinct from decorative gold.

Red against green (and violet against blue) are colour-blindness risks, so silhouette, value and emblem must carry class identity too.

### 6.5 How an AI agent can produce this, honestly
| Approach | How | Quality and limits |
|---|---|---|
| **Python/Pillow pipeline** (recommended; section 7) in `design/scripts/` (`mise run assets`, Pillow 13.0.0) | Slot-derived layout, layered grids, shapes and a box renderer, palette ramps, procedural shading and outlines | Reproducible and exact in size. Good for frames, sockets, panes, plates, lettering and faceted figures. Risk: flat vector shapes or programmer art without pixel-level cleanup |
| **Hand-authored pixel grids** (text rows, one character per palette entry) | For faces, hands, emblems, icons, corner ornaments, letters, AA | Precise up to about 32x32 per piece. A whole 144x180 figure as one grid is error-prone, so compose pieces |
| **Aseprite** (only with a human using it) | A person paints; its [CLI](https://www.aseprite.org/docs/cli/) can batch-export layers and run Lua scripts, then Python slices and places the PNGs | Best editing tool for hand art. The CLI does not make the art. Needs a copy of the program; I did not check whether one is installed |
| **3D model render** (Blockbench or similar) | Pose a blocky model, export a render, clean it up | Natural for faceted figures, but needs a GUI app a person operates. The Python box renderer (7.3) is the agent-usable version |
| **Render, look, revise** (required with either) | Save previews at 8x nearest for detail, plus the full panel at **4x and 3x screen size** (art scaled 2x and 1.5x nearest), a black silhouette strip, a greyscale strip, and a mock with slot grid, label and sample player items. Open with `Read` | The main quality driver. The model's vision is **weak at single-pixel judgement** and images may be downscaled, so inspect crops at 8-12x |
| **CC0 assets** | Parts or reference from [Kenney](https://kenney.nl/support) (CC0, attribution not required [V]) or OpenGameArt filtered to CC0 (check each asset's page [U]). Record URL, author and licence in `design/CREDITS.md` | Rarely matches this style or these sizes; mixed sources look inconsistent. Recolour to our palette and match the pixel density. Palettes such as [Endesga 32](https://lospec.com/palette-list/endesga-32) are useful references; no licence statement was shown on that page |
| AI image generator, then downscale | No generator was available or evaluated for this note | Downscaled output typically has off-grid edges, hundreds of colours and soft shading, so it needs heavy repaint; licence terms vary. Do not plan on it |
| Human pixel artist (user or commission) | Paints or touches up the four figures in Aseprite or similar | Highest quality ceiling |

**Expectation to set with the user:** an agent can reliably deliver clean, consistent GUI frames, sockets, glows, plates and lettering. It can deliver **readable, attractive stylised blocky characters** with several review rounds. It is **unlikely to match a skilled pixel artist** on anatomy, dynamic posing, faces and material rendering. Since art quality is the top priority, plan an approval gate: **one hero panel first** (Warrior at final size), shown to the user, before the other three. Keep PNG layers easy to replace with hand-made art at the same paths and sizes. This project's "one attempt, one review" working rule is probably too tight for the hero art, so the brief should allow iterations explicitly.

Suggested order: palette file, silhouettes of all four, flat colours, light and shadow planes, details, outline and AA, backdrop and frame, composite, review.

### 6.6 Artist review checklist (every preview round)
- [ ] Native canvas sizes exact; one 2x grid; no resampled or rotated parts.
- [ ] Only frozen palette colours (the preview script can print the colours used); alpha binary except glows.
- [ ] Four black silhouettes are distinct and recognisable at 1x GUI size.
- [ ] Greyscale: figure separates from backdrop; focal points have the strongest contrast.
- [ ] Light is top left on every element, including mirrored ornaments.
- [ ] No pillow shading, banding, jaggies, orphan pixels, accidental double lines or noise.
- [ ] Hue-shifted ramps; no pure black; no muddy or neon outlier.
- [ ] Faces and hands read at screen size.
- [ ] The four panels (both pages) look like one set: same head height, ground line, plate position, outline weight, detail level.
- [ ] Captain cannot be mistaken for Warrior in black silhouette or greyscale; the banner and horn read at screen size.
- [ ] Flipping between page 1 and 2 previews shows no shift in frame, header, divider or inventory area; arrows and page pips are obvious.
- [ ] Name plates are centred and readable at the 1.5x (GUI scale 3) preview.
- [ ] Each figure stays in its panel; the panel matches its slot columns; the divider does not read as a choice.
- [ ] Panel fully covers the vanilla shape; overflow within 8 px vertically; no seam between tiles.
- [ ] Slot cells align with section 1.1; the "Inventory" plate is readable; player items stand out against the cells.
- [ ] A hover square on any slot does not hide the face or name badly.
- [ ] Skill states are distinguishable in greyscale and as still frames; lit links align with painted tracks; animation loops cleanly.
- [ ] Final judgement at screen size, not only zoomed: "would this pass as a polished commercial server's menu?" If not, name the weakest element and redo it.

## 7. Production pipeline: Python and Pillow (recommended)
The user has used this before, and it fits the repo: Python 3.12, with `pillow==13.0.0` and `numpy==2.5.4` already in `design/requirements.txt` (no new dependency). Its main strength is that **every size and position is calculated**, so art cannot drift off the slot grid.

### 7.1 Suggested files
`mise run assets` runs every top-level `design/scripts/*.py` in glob (name) order [repo `mise.toml`], so shared code goes in a subfolder, which scripts can import.
```
design/scripts/pixelkit/__init__.py
design/scripts/pixelkit/layout.py      DENSITY = 2; all rects derived from slot (col,row); tile cuts; paths
design/scripts/pixelkit/palette.py     the frozen ramps, by name
design/scripts/pixelkit/grid.py        text rows + legend -> image
design/scripts/pixelkit/shade.py       facet steps, bevels, outlines, dither, glow
design/scripts/pixelkit/boxrig.py      box renderer for figures (7.3)
design/scripts/pixelkit/lettering.py   pixel capitals for plates and header
design/scripts/gui_class_select.py     2 masters -> 4 tile PNGs
design/scripts/gui_items.py            panes, links, tooltips, .mcmeta, JSON
design/scripts/gui_skill_tree.py       tree master -> 2 tile PNGs
design/scripts/zz_gui_preview.py       runs last; writes design/previews/gui/
design/art/                            optional hand-made PNG overrides and grid sources
```
Scripts write final files into `resourcepack/`. `font/gui.json` can be written by the same script from the same constants.

### 7.2 Pillow rules that prevent blurry or off-by-one art
- `Image.resize` **defaults to bicubic** for RGBA [V] ([Image docs](https://pillow.readthedocs.io/en/stable/reference/Image.html)). Always pass `resample=Image.Resampling.NEAREST`, and scale only by integers for assets (1.5x is for previews).
- `rotate` and `transform` default to nearest [V], but rotating finished pixel art still breaks lines. Rotate geometry **before** rasterizing.
- `ImageDraw.rectangle` includes **both** end points [V] ([ImageDraw docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)). Keep half-open rects in `layout.py` and draw `(x0, y0, x1-1, y1-1)` through one helper. `polygon` includes its coordinate pixels too [V], so adjacent facets overlap by one line: set the paint order on purpose.
- Draw at native size. Do **not** draw large and downsample for smoothing; it creates off-palette colours. For text use own pixel letters (or `fontmode = "1"` [V] in preview-only mock text).
- `ImageDraw` shapes come out hard-edged in my knowledge [U: the docs page does not say]. Check the colour list in the preview.
- Composite layers with `alpha_composite` [V]. Use fixed palette RGBA values only; `getcolors` lists what was used [V].
- Seed any randomness, so the same sources give the same PNGs.

### 7.3 Building the art
**Layers (back to front):** backdrop, emblem, rear parts (cape, banner pole, quiver), body, front limbs and weapon, face and detail grids, outline, rim light, panel frame, plate and lettering.

| Technique | How |
|---|---|
| Layout | `slot_rect(col, row)` returns the GUI cell (7+18c, 17+18r, 18x18); `art(rect)` multiplies by DENSITY. No other script contains raw coordinates for slot-bound things |
| Tiling | Draw one 352x444 master; crop `(0,0,352,222)` and `(0,222,352,444)`; force alpha >= 1 in each cell's last column |
| Pixel grids | Small text sprites with a legend that maps characters to ramp names and steps, so a recolour is one change; fail loudly on ragged rows or unknown characters |
| Part masks | Each part is a mask plus material (ramp) plus facet step; colour is looked up last |
| Procedural shading | Step chosen per **facet**: top lighter, front mid, side darker, undersides darkest. Add 1-2 art px lit bevel on top-left edges and a cast-shadow mask where one part overlaps another (shift the upper mask down and right). Never shade by distance to the outline (that is pillow shading) |
| Outline | Dilate the figure mask by 1-2 px (4-neighbour, numpy shifts); colour each outline pixel from the darkest step of the neighbouring material; lighten or drop it on top-left edges |
| Texture and dither | Ordered 2x2 or 4x4 masks, limited to named large regions |
| Glow and animation | Separate partial-alpha layers; frames generated from a phase value and stacked vertically, with the `.mcmeta` written alongside |
| Mirroring | Mirror ornament **masks**, then shade after mirroring |
| Cleanup | A final hand grid overlay per figure for jaggy fixes, glints and face. Automatic cleanup filters tend to damage intent, so do not rely on them |

**Box renderer for the figures (recommended to prototype).** "Chunky faceted blocky" characters suit a very small software renderer in numpy: define head, torso, limbs, pauldrons, shield and so on as boxes or simple prisms with position, size and joint angles; project orthographically at a fixed three-quarter angle straight to the target resolution with a depth buffer and no anti-aliasing; keep per pixel the part, face and material; map the face normal against the top-left light to a ramp step; draw inner lines where part or depth changes. This gives consistent perspective and light across all four classes and cheap pose changes, which hand-placed 2D polygons often get wrong. Its limits: stiff, mannequin-like poses; uneven stair steps on rotated edges (prefer angles that give 1:1 or 2:1 lines); cloth, banners, bows and faces still need hand-shaped 2D layers. It is extra code, so judge it on the **hero prototype**. If direct 2D polygons look as good, skip it.

**Override hook:** if a hand-made figure exists, for example `design/art/hero/captain.png` (144x180, transparent), the script composites it instead of the generated one. A human can then improve one figure without touching layout or code.

### 7.4 Preview compositor
`zz_gui_preview.py` draws what the client should show, from the **real pack files**: it reads `font/gui.json` and the title string and applies section 1.2 (pen x = 8; glyph top = 13 - ascent; scale = height / cell height; advance = trunc(0.5 + ink*scale) + 1; space advances). A wrong ascent, shift or tile cut therefore shows up in the picture.

Draw order: dimmed backdrop, **mock vanilla panel**, glyphs, "Inventory" at (8,128) in `#404040`, highlight mock on one slot, items (items JSON, model, texture; clipped to 16x16 unless oversized), sample player items (own placeholder blocks, some bright and some dark), tooltip mock.

- **Mock the vanilla chest procedurally** (176x221 panel and 18x18 cells from `layout.py`). Do not commit Mojang textures. The script may optionally read `generic_54.png` from a local path outside the repo to confirm the footprint.
- **Leak view:** paint the mock panel magenta. Any magenta inside the footprint is a hole in our art.
- **Slot view:** 1 px slot and click-region lines over the art.
- **Screen sheets:** 1280x720 at GUI scale 3, 1920x1080 at 4, 2560x1440 at 6, plus scales 2 and 5 crops. Panel origin: `left = (ceil(W/s) - 176) // 2`, `top = (ceil(H/s) - 222) // 2` [M]. Scale 2x art by `s / 2` with nearest.
- **Art views:** both class pages side by side, each figure at 8x, black silhouettes, greyscale, animation frames as a strip, colour list.

Limits: this is a **simulation**. At odd scales Pillow may pick different texels from the client by a pixel; mock fonts, highlight and tooltip are approximations. A real client screenshot is the final proof. The overlay of a user's screenshot at 50 % over the preview is the quickest alignment check.

### 7.5 What this pipeline can and cannot do
| Asset | Expected quality |
|---|---|
| Exact fit to slots, tiles, font JSON | Very high |
| Frames, pillars, plates, sockets, tracks, lettering | High |
| Glowing and animated panes | High |
| Emblems, small icons (hand grids) | Medium to high |
| Four full-body character illustrations | **Medium**: readable, consistent, stylised. Dynamic anatomy, expressive faces, cloth and metal rendering are the weak points |

Script output being precise says nothing about whether it **looks good**; only looking at renders does. Keep the 6.6 checklist, the Warrior-first approval gate, and add a **Captain silhouette comparison against Warrior** at that gate. If the hero panel is not good enough after a few rounds, the better route for figures is a human artist through the override hook, with Python still doing layout, frames, slicing and previews.

## 8. Plain vanilla pack or ItemsAdder?

### 8.1 ItemsAdder support for 26.3 (checked 2026-11-25, volatile)
- Latest stable I found: **4.0.18** (21 Aug 2026); the [release list](https://voxel.shop/resource/itemsadder-custom-items-etc.1851/updates) does not mention 26.3. A project collaborator wrote that ["4.0.18 isn't supporting 26.3"](https://github.com/PluginBugs/Issues-ItemsAdder/issues/5607) and pointed to a beta on Discord.
- **5.0.0 betas do run on 26.3:** reports use [beta-4](https://github.com/PluginBugs/Issues-ItemsAdder/issues/5585) (a Paper 26.3 block-break crash, reported fixed by a later update) and [beta-5](https://github.com/PluginBugs/Issues-ItemsAdder/issues/5603) (pack not sent on join after `/iazip`; the collaborator said beta 8 was current and asked for a retest).
- The [26.3 support issue](https://github.com/PluginBugs/Issues-ItemsAdder/issues/5527) is still open (milestone shown as 5.0.0), and the [issue search](https://github.com/PluginBugs/Issues-ItemsAdder/issues?q=26.3) lists several open reports, including pack generation titles (their versions not checked).
- Conflicting evidence: a web search summary said a BuiltByBit listing shows 26.3 as supported. I did not open that listing to confirm it, or which build it refers to.
- I did not find the beta's supported-version statement; it is distributed on Discord. I do not know which version the user has (`/version ItemsAdder`).

### 8.2 Comparison for these two GUIs
| | Plain pack | ItemsAdder |
|---|---|---|
| 26.3 | Native (format 97.1) | Beta only |
| Backgrounds | Our font JSON and title string | [Font images](https://wiki.itemsadder.com/adding-content/font-images/font-images.md): YAML `path`, `scale_ratio` (our `height`), `y_position` (our `ascent`, must be <= `scale_ratio`), `:offset_N:` shifts. [Custom GUIs](https://wiki.itemsadder.com/adding-content/font-images/guis) are this same title technique |
| Limits | 256x256 glyph, no per-slot highlight control, no hover events | **Same**: the 256 limit applies and large images are split. It removes none of the client limits |
| Codepoints | Fixed by us, matching the contract | Auto-assigned unless `symbol` is set |
| Skill panes | Items JSON, models, `.mcmeta`, `oversized_in_gui` fully ours | Defined through IA YAML, which generates models. I did not verify its support for `oversized_in_gui`, composites or `tooltip_style` |
| Pack hosting and sending | We need an HTTPS URL, SHA-1 in config and a small amount of sending code | **Its real advantage:** builds, zips and [hosts](https://wiki.itemsadder.com/plugin-usage/plugin-configuration/resourcepack-hosting.md) (Simple Self-Host, Lobfile, self-hosting) and sends |
| Code | Paper API only | API dependency, load event, reload handling, hook isolation |
| Cost and risk | Free, open, in git, previewable offline | Paid, closed; support lags new Minecraft versions; more moving parts |

### 8.3 Recommendation: **plain vanilla pack**
Both GUIs need only a font, a few item definitions and sprites. ItemsAdder adds nothing visual, and today it would put the project's main priority on beta software.

**Exception, to confirm with the user:** if the server will run ItemsAdder anyway for other content, do not run two competing packs (`docs/integrations.md` rule 6). Then:
1. Keep our art, `font/gui.json`, characters and item JSON unchanged.
2. Copy `resourcepack/assets` into `plugins/ItemsAdder/contents/arkenmmo/resourcepack/assets` and run `/iazip` ([merge guide](https://wiki.itemsadder.com/adding-content/merge-resourcepacks)).
3. Turn the plugin's own pack sending off with a config switch. The plugin still needs no ItemsAdder API.
4. Check in game that the merged pack keeps our files (conflict handling beyond folder priority is not documented on that page) and which vanilla assets ItemsAdder overrides [U]. This also requires an ItemsAdder build that supports 26.3.

## Pitfalls
- One bad provider (ascent > height, missing PNG) **kills the whole font**. Check the client log for `Unable to load font`.
- A tile cell over 256 px shows a missing glyph.
- A forgotten `<white>` makes the art dark grey.
- A transparent right edge on a tile shifts everything after it.
- Item textures outside `textures/item/` are not in the items atlas, giving a missing texture.
- Another server or user pack that overrides the highlight sprites, tooltip sprites or the default font can change the look. Our own font id and namespace avoid most clashes.
- Global overrides (highlight, `generic_54`, lang) leak into every screen.
- `mise run validate-assets` checks item, model and texture references [per `docs/toolchain.md`], not font PNGs or tooltip sprites. Verify those in the client.
- All **[U]** items need a look in a real client. There is no test server in this repo, so the user checks them in game: slot alignment (especially player rows), highlight appearance, oversized links, configure-phase pack send, cursor position on reopen.

## Sources
- https://minecraft.wiki/w/Pack_format
- https://minecraft.wiki/w/Pack.mcmeta
- https://minecraft.wiki/w/Font_definition
- https://minecraft.wiki/w/Items_model_definition
- https://minecraft.wiki/w/Model
- https://minecraft.wiki/w/Resource_pack
- https://minecraft.wiki/w/Data_component_format/tooltip_display
- https://minecraft.wiki/w/Data_component_format/tooltip_style
- https://minecraft.wiki/w/Java_Edition_1.21.11
- https://minecraft.wiki/w/Java_Edition_26.1
- https://minecraft.wiki/w/Java_Edition_26.2
- https://minecraft.wiki/w/Java_Edition_26.3
- https://minecraft.wiki/w/Java_Edition_1.21.6
- https://minecraft.wiki/w/Server.properties
- https://docs.neoforged.net/primer/docs/1.21.6/
- https://raw.githubusercontent.com/xef5000/materione/main/docs/architecture/gui.md
- https://github.com/xef5000/materione/pull/197
- https://github.com/InventivetalentDev/minecraft-assets/tree/26.3/assets/minecraft
- https://jd.papermc.io/paper/26.3/
- https://docs.papermc.io/adventure/resource-pack/
- https://docs.papermc.io/adventure/minimessage/format/
- https://docs.papermc.io/paper/dev/dialogs/
- https://jd.advntr.dev/api/latest/net/kyori/adventure/resource/ResourcePackRequest.Builder.html
- https://github.com/PaperMC/Paper/issues/12865
- https://github.com/PaperMC/Velocity/issues/1164
- https://modrinth.com/resourcepack/guitem
- https://pixeljoint.com/forum/forum_posts.asp?TID=11299
- https://www.derekyu.com/makegames/pixelart.html
- https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes
- https://kenney.nl/support
- https://lospec.com/palette-list/endesga-32
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
- https://www.aseprite.org/docs/cli/
- https://jd.papermc.io/paper/26.3/org/bukkit/event/inventory/InventoryCloseEvent.Reason.html
- https://voxel.shop/resource/itemsadder-custom-items-etc.1851/updates
- https://github.com/PluginBugs/Issues-ItemsAdder/issues/5527 (also /5585, /5603, /5607)
- https://wiki.itemsadder.com/adding-content/font-images/font-images.md
- https://wiki.itemsadder.com/adding-content/font-images/guis
- https://wiki.itemsadder.com/plugin-usage/plugin-configuration/resourcepack-hosting.md
- https://wiki.itemsadder.com/adding-content/merge-resourcepacks

## Hand-off

### Proposed contract IDs (the orchestrator fixes these in the brief)
| Kind | IDs |
|---|---|
| Font | `arkenmmo:gui` |
| Glyphs | class select page 1 `U+E001..E004`, page 2 `U+E005..E008`; skill tree `U+E011..E014` (per-class tree art: `E021..`, `E031..`, `E041..`); shifts `U+F801..F809` = -1..-256, `U+F821..F829` = +1..+256 (powers of two) |
| Item models | `arkenmmo:gui/blank`, `arkenmmo:gui/skill/locked`, `.../purchasable`, `.../owned`, `.../excluded`, `.../link_h`, `.../link_v` |
| Tooltip styles | `arkenmmo:warrior`, `arkenmmo:archer`, `arkenmmo:mage`, `arkenmmo:captain`, `arkenmmo:skill` |
| Sound events (`sounds.yml` names) | `menu_open`, `class_select`, `skill_unlock`, `skill_denied`, `menu_page` (no hover sound: the server cannot detect hover) |
| Effect IDs | `class_chosen`, `skill_unlocked` (optional world effects; GUI glow is texture animation only) |

### Decisions needed before design starts
Already decided: two class pages with two panels each; Captain is the fourth class.

1. Plain pack (recommended, section 8) or ItemsAdder merge; if ItemsAdder stays on the server, which version it is.
2. Hover highlight option A, B or C (section 2.4).
3. Per-skill icons or shared state panes only; one shared tree background or one per class.
4. Art approval gate: Warrior hero panel first, with iterations allowed; whether a human artist will touch up.

### model-designer (plain pack, Python pipeline from section 7)
- `resourcepack/pack.mcmeta` (section 5.1) and `pack.png`.
- Scripts in `design/scripts/` with `pixelkit/`, optional overrides in `design/art/`, style guide with the frozen palette, previews in `design/previews/gui/`.
- Preview compositor (7.4) **before** the final art, so every iteration is judged in context.
- Class backgrounds: two 352x444 masters, exported as `textures/font/gui/class_select_{1,2}_{top,bottom}.png` (352x222 each), per section 4: two 144x216 panels, 144x36 name plates, divider pillar with page arrow and pips, header, player-inventory cells and "Inventory" plate.
- Skill tree background: `skill_tree_top.png` and `_bottom.png`, same sizes, with socket frames and unlit tracks matching the brief's topology.
- `font/gui.json` (section 1.4).
- Panes: `textures/item/gui/skill/{locked,excluded}.png` 32x32; `{purchasable,owned}.png` 32x(32*N) with `.mcmeta`; `link_h.png` and `link_v.png` 32x32 (36x36 if oversized); matching `items/` and `models/item/` JSON; `items/gui/blank.json`.
- Tooltips: five styles, 2 PNGs of 100x100 plus 2 `.mcmeta` each.
- Highlight sprites only if option B or C is chosen.
- Constraints: sections 1.2, 1.5, 3, 6 and 7.2. Binary alpha on hard art. All of section 6.6 before reporting done. Make the Warrior panel first, then compare the Captain silhouette against it before finishing the set.

### sound-designer
`sounds.json`, `.ogg` files, subtitles and `sounds.yml` entries for the five events above (short UI sounds, vanilla fallbacks). No other pack work.

### vfx-designer
Nothing for the GUIs. Only the two optional effect IDs in `effects.yml` if the brief includes them.

### plugin-coder
- Menu holder pattern with page number, slot maps and paging (sections 4.1-4.3), full click and drag cancelling, in-place state updates (section 5.4). No ItemsAdder API.
- A config switch for the plugin's own pack sending only if the brief chooses to support the ItemsAdder merge route.
- Title built from config using section 1.4 (trusted MiniMessage, no player input).
- Item factory with the data components; identical stacks across a class section; `hideTooltip` for links and decoration.
- Pack sending with url, sha1 and id in the first section of `config.yml`, required, preferably in the configure phase with a timeout; track status and gate the menus on it.
- Sounds through `sounds.yml`, effects through `Effects.play(id)`.
