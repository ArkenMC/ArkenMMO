# Asset: skill tree menus

**Status:** A1 preview, waiting for the user's approval. **Nothing is wired into the pack yet**: no PNGs, models, item definitions, glyphs or title strings. All art is placeholder.
**Brief:** `docs/briefs/skills.md` · **Style:** `design/gui-style-guide.md` · **References:** `design/skill-tree-visual-research.md`
**Pipeline:** plain vanilla resource pack, Paper 26.3 (pack 97.1, unchanged).

## Purpose
One tree page per branch and view in a 9x6 chest. Warrior first; the preview is the Berserker page (upper and lower view).

## Files
| File | What |
|---|---|
| `design/scripts/pixelkit/treeicons.py` | 24x24 master masks: Cleave, the 6 Berserker skills, 3 tab sigils |
| `design/scripts/pixelkit/treenodes.py` | 32x32 item art: node states, lit connectors, reset button |
| `design/scripts/pixelkit/treestone.py` | the painted page: slab, carvings, grooves, sockets, seals, footer, slot maps |
| `design/scripts/zz_skill_tree_preview.py` | previews in `target/previews/skills/` (`mise run assets`; not committed) |

## Dimensions
Master 352x444 art px (176x222 GUI). Item tile 32x32 (16x16 GUI) at slot cell + 2 art px. Icon 24x24 at tile offset 4. Groove 8 px, tile px 12..20. Clamp 8x14 across each slot gap; lit pieces leave 2 px clear at each end so the clamp shows whole. No 3D models, pivots or animations.

## Slot maps
| View | Nodes | Connectors | Sealed (painted) |
|---|---|---|---|
| A (upper) | Cleave 0, n1 4, n2 20, n3 24, n4 38, n5 40, n6 42 | 2 `corner_es`, 3 5 `h`, 6 `corner_sw`, 11 15 29 33 `v`, 39 41 `h` | none |
| B (lower) | n4 2, n5 4, n6 6 | 3 5 `h` | 20, 24 (keystones), 40 (ultimate); grooves 11 15 29 33 38 39 41 42 |

Edges to connector slots: n1-n2 = 2, 3, 11; n1-n3 = 5, 6, 15; n2-n4 = 29; n3-n6 = 33; n4-n5 = 39; n5-n6 = 41. A piece is set only when both ends are owned.

Footer: 45 back, 46 Guardian, 47 Berserker, 48 Duelist, **49 reset (item)**, 50 scroll up, 51 scroll down, 52 loadout, 53 info. All but 49 are painted; the unusable scroll arrow is flush and dark.

## States
| State | Look | Cue besides colour |
|---|---|---|
| locked | dull cut in a dark stone, no ring | no ring |
| available | thin steel ring, slate-filled rune | ring |
| confirm | pale rune, four gold corner brackets | brackets |
| owned | crimson ring and halo, ember-filled rune, still | four rivets, lit connectors |
| sealed | rough plug, one askew iron band; the ultimate is wider with two bands and blank red wax | irregular outline |

Actives are square, passives octagonal. Cleave is a square with two gold bars, always owned, on its own stepped plinth at **slot 0** with no groove.

Reset: `ready` (bronze ring, pale returning arrow), `confirm` (gold with corner brackets), `unavailable` (cold, flat, cracked).

## Proposals that need approval
1. **Cleave** at slot 0 on view A of all three branches. View B does not show it.
2. **Reset confirm:** the first click swaps slot 49 to `confirm`; lore says how many points come back and "Click again to reset". Any other click, a page change or closing reverts. It resets what the brief says reset does; this proposal changes no rules.
3. **Undo:** clicking a stone bought during this opening shows the `confirm` art with lore "Click again to undo"; the second click refunds it. It is refused, with the reason in lore, if another owned node would lose its connection or a gate. Same gesture as buying, no new textures, no right-click change to `Menu`. Such stones look like any owned stone; lore says they can be undone.
4. The backdrop (helm over crossed axes, two grave swords, stave bands) is the **Warrior** backdrop, shared by all three branches. Header and tab change per branch.
5. The "Inventory" plate is one parchment step darker than on the class menu.
6. **Palette: no additions.** Only existing ramps are used; the preview script fails on any other colour or partial alpha.

## Palette used
`iron`, `ember_stone`, `steel`, `crimson`, `gold`, `parchment`, `leather` (hex in `pixelkit/palette.py`).

## For the coder (planned; fixed only after approval)
Item keys, title keys and glyph block as proposed in `docs/research/skill-tree-gui.md`. Nothing exists in the pack yet.

## Left for A2
12 other Warrior icons; Guardian and Duelist pages (lettering still needs `D` and `V`); loadout menu; 6 glyph masters, item PNGs, models, definitions, font providers, title strings; Warrior starter sword.

## Not verified
Only simulated: no 26.3 client. Item-over-glyph draw order, exact alignment, player rows and the look at the user's own GUI scale are unchecked. GUI scale 3 samples the 2x art unevenly (1.5 px per art px), as on the class menu.
