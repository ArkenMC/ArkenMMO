# Emerald item and tooltip

Generator: `design/scripts/items_emerald.py` (run by `mise run assets`). Pipeline: plain vanilla resource pack, Paper 26.2, pack format 88.0.

## Purpose
A custom emerald item, not a vanilla override, with its own hover border.

## IDs (for the code)
| Component | Value |
|---|---|
| `item_model` | `arkenmmo:emerald` |
| `tooltip_style` | `arkenmmo:emerald` |

## Files (`resourcepack/assets/arkenmmo/`)
| File | What |
|---|---|
| `items/emerald.json` | item definition, `minecraft:model` -> `arkenmmo:item/emerald` |
| `models/item/emerald.json` | `minecraft:item/generated`, `layer0` = `arkenmmo:item/emerald` |
| `textures/item/emerald.png` | 16x16, alpha 0 or 255, hand-authored pixel grid |
| `textures/gui/sprites/tooltip/emerald_background.png` (+`.mcmeta`) | 100x100, nine-slice border 9, fill 8..91 with clipped corners, alpha 240 |
| `textures/gui/sprites/tooltip/emerald_frame.png` (+`.mcmeta`) | 100x100, nine-slice border 10, `stretch_inner`, 1 px frame at inset 9 |

The `.mcmeta` values are the same as the class tooltips (vanilla 26.3).

## Look
- Gem: tall step-cut gem (10 x 14 px), pointed top and bottom, lit from the top left with a 1 px near-white glint, bright left facets, darker lower right, dark outline.
- Tooltip: dark emerald background (`emerald` 0 at alpha 240), frame in `emerald` steps 4 -> 2 stepping darker downward, a 2x2 emerald gem on each corner (glint top left, shade bottom right). Text stays readable: the background is near black.

## Palette: `emerald` ramp (dark to light)
`#06261a` `#0b4a2c` `#12803f` `#1fb857` `#4fe07e` `#a8f5b8` `#f2fff4`

## Using it in code
```java
meta.setItemModel(NamespacedKey.fromString("arkenmmo:emerald"));
meta.setTooltipStyle(NamespacedKey.fromString("arkenmmo:emerald"));
```
Previews: `target/previews/emerald/` (not committed).
