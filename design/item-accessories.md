# Accessory items

Generator: `design/scripts/items_accessories.py` (run by `mise run assets`; the tooltip is drawn by `items_emerald.tooltip`, which takes a ramp). Pipeline: ItemsAdder content `arkenmmo` over the plain pack, Paper 26.2, pack format 88.0. Same pattern as the emerald (`design/item-emerald.md`): texture, model and item definition live in `resourcepack/assets/arkenmmo/`, the ItemsAdder config in `itemsadder/contents/arkenmmo/configs/accessories.yml`, and `mise run itemsadder` copies the assets into the content zip.

## Purpose
Four real accessories the player owns and wears in the inventory's four accessory slots (ring, ring, amulet, bracelet; `design/gui-inventory.md`). They are detailed coloured icons, not grey ghosts. The flat slot placeholders in the inventory texture and the items match in motif: ring and ring (gem on a band), amulet (chain and medallion), bracelet (wide flat oval cuff).

## IDs (for the code)
| ItemsAdder id | Display name | Material | `item_model` | `tooltip_style` |
|---|---|---|---|---|
| `arkenmmo:ring_1` | Ring | PAPER | `arkenmmo:ring_1` | `arkenmmo:accessory` |
| `arkenmmo:ring_2` | Signet Ring | PAPER | `arkenmmo:ring_2` | `arkenmmo:accessory` |
| `arkenmmo:amulet` | Amulet | PAPER | `arkenmmo:amulet` | `arkenmmo:accessory` |
| `arkenmmo:bracelet` | Bracelet | PAPER | `arkenmmo:bracelet` | `arkenmmo:accessory` |

Config keys are exactly the emerald's (`resource.material`, `generate: false`, `model_path: arkenmmo:item/<id>`, `tooltip_style`). Its in-game result for the emerald is the user's report; the accessories were not loaded in game.

## Files (`resourcepack/assets/arkenmmo/`)
| File | What |
|---|---|
| `items/<id>.json` | item definition, `minecraft:model` -> `arkenmmo:item/<id>` |
| `models/item/<id>.json` | `minecraft:item/generated`, `layer0` = `arkenmmo:item/<id>`, no `display` (plain model; the size is painted into the texture) |
| `textures/item/<id>.png` | **32x32**, alpha 0 or 255, palette colours only |
| `textures/gui/sprites/tooltip/accessory_background.png` (+`.mcmeta`), `accessory_frame.png` (+`.mcmeta`) | shared tooltip style, same geometry and `.mcmeta` as the class and emerald styles |

## Look (all in the frozen palette, no new ramp)
- **Ring** (`ring_1`): gold band lit from the top left (`gold` 1..5), a diamond-cut ruby (`crimson` 1..4, `ivory` 4 glint) in a one-pixel gold setting, `gold` 0 outline.
- **Signet Ring** (`ring_2`): steel band (`steel` 1..5) under a flat rounded seal with a gold frame, a gold cross on a `navy` field and a small `arcane` gem at the cross's centre; `steel` 0 outline.
- **Amulet**: a V of gold chain links (alternating `gold` 4 and 2) meeting a small bail over a round medallion with a bevelled gold rim (`gold` 2..5) and an `violet` amethyst; `gold` 0 outline.
- **Bracelet**: a cuff lying diagonally (long axis from bottom left to top right, about 13 px across, an elongated oval unlike the rings' round bands): a `steel` back arc on the upper left and a `gold` front band on the lower right, brightest on its inner edge and darker outwards, with a green `forest` gem in a gold setting in the band. Drawn by testing each pixel in the cuff's rotated frame, not by resampling a bitmap. No top gem and a lying oval, so it is not read as a ring. (A horseshoe, then a rune-stone charm, were dropped on the user's requests; the item is now `bracelet`.)
- Each icon uses at most about 24 colours. The gems are different colours so the four tell apart at hotbar size (ruby, aqua, amethyst, green). The class ramps are used for gems only, not as class identity.
- Tooltip `arkenmmo:accessory`: the emerald tooltip's geometry in the `gold` ramp: `gold` 0 (`#3d2415`) background at alpha 240, frame `gold` 4 -> 2 stepping darker downward, a 2x2 gold gem on each corner (`gold` 5, 4, 2, 1). The background is a warm near-black brown, so white text stays readable.

## Size in slots (32x32 textures, no display transform)
History: the textures were 16x16 art about 12 px wide shown at the full 16 GUI px (too big); commit df80e3a shrank them with `display.gui.scale` 0.5 (art about 6 GUI px, too small). Now the **texture** is 32x32 and the art is about 24 texels across (22..26 checked, 11..13 GUI px), at least 3 texels from every edge, centred; the model is plain `item/generated`. A generated model always spans the slot's 16 GUI px whatever the texture size, so a 32x32 texture has 0.5 GUI px texels = exactly 1 art px of the 512x512 inventory texture: the item's pixels sit on the same grid as all the GUI art (clean at GUI scale 2 and 4, alternating at 3 like the existing art) and the painted placeholders are the items' own pixels 1:1 (`gui_slot_icons.ITEM_AT` is 0). Ground, held and item-frame renders are not shrunk any more (they use the same 16 units, so they look like a normal item there). Redrawn with more detail (bigger gems with facets, a table and glint, a chain of 2x2 links, a 2 px cross on the seal), not upscaled.
- Sizes: ring 20x25 texels, signet ring 22x25, amulet 26x25, bracelet 24x24 (outlines included).
- If it still feels off in game: the art box is set by the `check()` limits in `items_accessories.py` and the shapes' radii; shrinking or growing needs a redraw, not a number.

## Using it in code
With ItemsAdder: `CustomStack.getInstance("arkenmmo:ring_1")` and so on. Without it, an item built from PAPER needs `meta.setItemModel(NamespacedKey.fromString("arkenmmo:ring_1"))` and `setTooltipStyle(NamespacedKey.fromString("arkenmmo:accessory"))`.

Previews: `target/previews/accessories/` (not committed): `items_x16.png`, `items_with_emerald_x6.png`, `items_hotbar_scale2.png`, `_scale3.png` and `_scale4.png` (top row the new size, bottom row the previous half-size look), `tooltip_accessory_x3.png`, `panel_accessory_row_x4.png`.

## Checks
`items_accessories.py` fails when a texture has non-binary alpha, a colour outside the palette, more than 24 colours, comes within 3 texels of an edge, has a longer side outside 22..26 texels, or has fewer than 250 or more than 700 opaque pixels. `tools/validate_assets.py` resolves each item definition to its model and texture.

## Not verified
- How the 32x32 art reads in game at GUI scale 2, 3 and 4 (judged from mock-ups only).
- ItemsAdder 4.0.18 loading these four configs and a `PAPER` item with its own `model_path`: the keys are the emerald's, which the user runs, but a different material was not tried.
- How the shared tooltip looks in game (only a mock-up).
