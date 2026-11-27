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
| `models/item/<id>.json` | `minecraft:item/generated`, `layer0` = `arkenmmo:item/<id>`, `display.gui` = rotation 0, translation 0, **scale 0.5** (`items_accessories.GUI_SCALE`) |
| `textures/item/<id>.png` | 16x16, alpha 0 or 255, palette colours only |
| `textures/gui/sprites/tooltip/accessory_background.png` (+`.mcmeta`), `accessory_frame.png` (+`.mcmeta`) | shared tooltip style, same geometry and `.mcmeta` as the class and emerald styles |

## Look (all in the frozen palette, no new ramp)
- **Ring** (`ring_1`): gold band lit from the top left (`gold` 1..5), a diamond-cut ruby (`crimson` 1..4, `ivory` 4 glint) in a one-pixel gold setting, `gold` 0 outline.
- **Signet Ring** (`ring_2`): steel band (`steel` 1..5) under a flat rounded seal with a gold frame, a gold cross on a `navy` field and a small `arcane` gem at the cross's centre; `steel` 0 outline.
- **Amulet**: a V of gold chain links (alternating `gold` 4 and 2) meeting a small bail over a round medallion with a bevelled gold rim (`gold` 2..5) and an `violet` amethyst; `gold` 0 outline.
- **Bracelet**: a cuff lying diagonally (long axis from bottom left to top right, about 13 px across, an elongated oval unlike the rings' round bands): a `steel` back arc on the upper left and a `gold` front band on the lower right, brightest on its inner edge and darker outwards, with a green `forest` gem in a gold setting in the band. Drawn by testing each pixel in the cuff's rotated frame, not by resampling a bitmap. No top gem and a lying oval, so it is not read as a ring. (A horseshoe, then a rune-stone charm, were dropped on the user's requests; the item is now `bracelet`.)
- Each icon uses at most about 20 colours. The gems are different colours so the four tell apart at hotbar size (ruby, aqua, amethyst, green). The class ramps are used for gems only, not as class identity.
- Tooltip `arkenmmo:accessory`: the emerald tooltip's geometry in the `gold` ramp: `gold` 0 (`#3d2415`) background at alpha 240, frame `gold` 4 -> 2 stepping darker downward, a 2x2 gold gem on each corner (`gold` 5, 4, 2, 1). The background is a warm near-black brown, so white text stays readable.

## Size in slots (gui display scale 0.5)
The textures are unchanged; the models shrink them in every GUI slot (inventory, hotbar, chests) by `display.gui.scale` 0.5, so a 16x16 texture draws 8x8 GUI px, centred in the slot's item area (scale is about the model centre, so no translation is needed). Only `gui` is overridden: `minecraft:item/generated` (26.2) defines `ground`, `head`, the third and first person hands and `fixed` but **no** `gui` (its gui transform is the identity), and a child's `display` entry replaces the parent's per context (vanilla's `item/handheld` defines only the hand contexts and its children keep `generated`'s ground and head transforms). So ground, held and item-frame renders are unchanged. Scale values may be 4 at most; there is no lower limit.
- Why 0.5: one texel then equals exactly one art px of the 512x512 inventory texture (half a GUI px), so the painted placeholders are the item's own pixels and line up exactly, and the item's pixel edges fall on the same grid as all the GUI art at every GUI scale (clean at 2 and 4; at 3 both the art and the item alternate 1 and 2 device px, as the existing art already does). Compared with other values: 0.75 gives 1.5 art px per texel (every second texel row/column uneven at any GUI scale, and placeholders could not match the pixels); 2/3 is clean at GUI scale 3 only; 0.5 is the only value whose texels match the texture grid.
- If 8x8 turns out too small in game, the next step is 0.75 with the placeholders rebuilt conservatively; the trade-off is uneven texels.
- The placeholders under the slots were rebuilt to match (`design/gui-inventory.md`): same derivation, now 1 art px per texel, centred 8 art px in from each side of the item area.

## Using it in code
With ItemsAdder: `CustomStack.getInstance("arkenmmo:ring_1")` and so on. Without it, an item built from PAPER needs `meta.setItemModel(NamespacedKey.fromString("arkenmmo:ring_1"))` and `setTooltipStyle(NamespacedKey.fromString("arkenmmo:accessory"))`.

Previews: `target/previews/accessories/` (not committed): `items_x16.png`, `items_with_emerald_x6.png`, `items_hotbar_scale2.png`, `_scale3.png` and `_scale4.png` (top row at the shrunken size, bottom row the old size), `tooltip_accessory_x3.png`, `panel_accessory_row_x4.png`.

## Checks
`items_accessories.py` fails when a texture has non-binary alpha, a colour outside the palette, more than 20 colours, touches the left or right border, or has fewer than 70 or more than 200 opaque pixels. `tools/validate_assets.py` resolves each item definition to its model and texture.

## Not verified
- Gui scale 0.5 in game: the display transform is verified from the model docs and vanilla files, not seen in the game; ItemsAdder 4.0.18 should keep it (it points at our model with `model_path`), unconfirmed.
- ItemsAdder 4.0.18 loading these four configs and a `PAPER` item with its own `model_path`: the keys are the emerald's, which the user runs, but a different material was not tried.
- How the shared tooltip looks in game (only a mock-up).
