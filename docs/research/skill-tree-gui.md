# Skill tree in a 9x6 chest menu: states, connectors, backdrops, footer

## Target version
**Paper 26.3**, plain vanilla pack (format **97.1**, `min_format [97,1]`, `max_format 97`), namespace `arkenmmo`. No ItemsAdder or ModelEngine. Checked 2026-11-26.

This builds on `docs/research/custom-gui-and-pixel-art.md` ("GUI note"). Glyph maths (section 1), font JSON (1.4), `pack.mcmeta` (5.1) and delivery (5.3) are not repeated. Art rules: `skill-tree-art.md`. This note **replaces** GUI note 3.1-3.2 (pulsing and shimmering panes): the user wants a **soft still** glow.

Tags: **[V]** verified in a cited source, **[R]** read in this repository, **[D]** derived, **[P]** proposal, **[U]** unverified.

## Summary
1. **Title glyph = everything static:** per-class backdrop, empty sockets, unlit grooves, sealed stones, header, footer art, active tab, scroll arrows. Bake **6 backgrounds per class** (3 branches x 2 views).
2. **Slot items = everything that changes:** node state, lit connector pieces, reset button. Update with `setItem`, without reopening.
3. One **baked flat texture per skill and state**. No composite models, tints, glint, animation or oversized models.
4. Lit connectors stay inside 16x16. Paint a stone **clamp** over each 2 px slot gap so the segments look intentional.
5. Tab or scroll click opens a new `Menu` with another title.

## Version notes
- 26.3 uses `item_model` and `assets/<ns>/items/*.json`; older `custom_model_data` override tutorials are obsolete (GUI note).
- `InventoryView#setTitle` is deprecated and documented as broken [V, GUI note], so no title changes in place.
- Fonts do not animate; item textures can, but the owned state is still by user decision.
- The pack already makes the slot highlight sprites transparent in every inventory [R `AGENTS.md`]. **Hover gives no visual feedback except the tooltip**, so every clickable thing must look clickable in the art or item.

## Layering: glyph or item
| Element | Layer | Why |
|---|---|---|
| Backdrop, frame, header with branch name, inventory area | glyph | static per page |
| Empty sockets, unlit grooves, clamps | glyph | static |
| Sealed keystones and ultimate, and all their grooves | glyph | cannot change in this release; add `gui/blank` for a tooltip |
| Active tab highlight, other tabs | glyph (baked) | changes only with the page |
| Back, scroll arrows (enabled or dim), loadout, info | glyph (baked) + `gui/blank` | static per page |
| Skill nodes | item | locked, available, confirm, owned |
| Lit connector pieces | item | appear on purchase |
| Reset button | item over a painted socket | ready, confirm, unavailable |

Items draw above the title art as long as the glyph spans the full 176x222 [GUI note 1.5, measured by a third party on 26.1.2].

**Why not state glyphs in the title?** Overlay glyphs can be positioned with `space` shifts and per-row `ascent`, but every purchase, undo or confirm click would need a new window. Items need one packet per slot.

**Why not `composite` or layered models?** `minecraft:composite` draws its models "in the order they appear in the list" ([NeoForge docs](https://docs.neoforged.net/docs/resources/client/models/items); the wiki states no order [V]). `item/generated` also stacks `layer0`..`layer4`, higher on top ([NeoForge docs](https://docs.neoforged.net/docs/resources/client/models/); the wiki's [Model page](https://minecraft.wiki/w/Model) gives no limit or order). Both work for layering, but the icon ink changes per state, so there is still one definition per skill and state. Flat baked PNGs are simpler and the preview shows exactly what ships. Plates and icons stay separate **in the Python script**.

## How many combinations
Warrior nodes n1-n6 with the connection rule have **17** possible owned sets per branch [D]: 1 empty and 16 containing n1.

| Approach | Needed |
|---|---|
| Whole screen painted per owned set | at least 17 sets per view A, times availability and confirm variants, times 3 branches and 4 classes. Rejected |
| **Backgrounds** (recommended) | 3 x 2 = **6 masters per class**: 12 PNGs, 24 glyph characters. All classes later: 24, 48, 96 |
| **Node items**, Warrior | 18 branch skills x 4 states = 72, plus Cleave owned = **73** |
| **Connector items**, per class colour | **4** shapes: `h`, `v`, `corner_es`, `corner_sw` (lit only) |
| **Reset** | **3** |

Each item is 1 PNG, 1 model JSON and 1 items JSON, all script-generated: **80** for Warrior.

The only difference between the three branches' pages is the header, active tab and optional faint branch emblem. Composing those as small overlay glyphs would cut to 2 masters per class but needs extra shift and ascent maths. Baking is recommended; the files are small and `pixelkit/pack.py` already writes them.

## Screen layout
Virtual 9x9 grid from `mmo-classes-levelling.md` section 6. View A shows virtual rows 0-4, view B rows 4-8. `slot = guiRow * 9 + col`. Footer is GUI row 5.

The draft's `-` marks at columns 2 and 6 in virtual rows 0 and 8 are really **corners**.

### View A (tiers 1-3)
| GUI row | Nodes (slot) | Connector pieces (slot: shape) |
|---|---|---|
| 0 | n1 (4) | 2: `corner_es`, 3: `h` (edge n1-n2); 5: `h`, 6: `corner_sw` (edge n1-n3) |
| 1 | - | 11: `v` (n1-n2); 15: `v` (n1-n3) |
| 2 | n2 (20), n3 (24) | - |
| 3 | - | 29: `v` (n2-n4); 33: `v` (n3-n6) |
| 4 | n4 (38), n5 (40), n6 (42) | 39: `h` (n4-n5); 41: `h` (n5-n6) |

Six nodes and ten connector slots make six edges. **An edge's pieces are all set when both end nodes are owned**; otherwise those slots are empty and the painted groove shows.

**Cleave [P]:** the draft grid has no place for the free core skill, but it needs one of the 19 icons. Proposal: a separate "core" plinth at **slot 0** in view A on all three branches, always owned, no groove to it. Needs confirmation in the A1 preview.

### View B (tiers 3-5)
| GUI row | Content |
|---|---|
| 0 | n4 (slot 2), n5 (4), n6 (6) interactive; connectors 3 and 5: `h` |
| 1 | slots 11, 15: sealed vertical grooves (painted) |
| 2 | slots 20, 24: **sealed** keystones n7, n8 |
| 3 | slots 29, 33: sealed vertical grooves |
| 4 | slot 40: **sealed** ultimate n9; slots 38, 39, 41, 42: sealed grooves |

The edges from n4 and n6 up to tier 2 are off screen in view B; the header covers that area, so no lit stub is possible. Paint a short stub only if it fits inside the socket cell. Sealed slots get `arkenmmo:gui/blank` with a tooltip that names no skill [P: "Sealed. Not yet."].

### Footer (fixed by the brief)
| Slot | Button | Art | Item |
|---|---|---|---|
| 45 | back | glyph | blank + tooltip (what "back" opens is the brief's or coder's choice) |
| 46, 47, 48 | branch tabs in contract order Guardian, Berserker, Duelist | glyph, one sigil each; the active one is raised, joins the frame and has a marker bar | blank + tooltip (name, points spent) |
| **49** | **reset** | glyph socket | `gui/button/reset`, `reset_confirm`, `reset_unavailable` |
| 50, 51 | scroll up, down | glyph; the unusable one is dim | blank; no action when unusable |
| 52 | loadout | glyph | blank + tooltip |
| 53 | info | glyph | blank + tooltip: level, XP, free points, points per branch |

- Footer cells are 36x36 art px side by side with only the 4 px gap. Tab sigils must differ in shape from each other, from skill icons and from reset.
- Reset appears on **both views of all three branches**. The two-click confirm is a [P]; the user decided only the slot, the own texture and the free/cooldown rules. `reset_unavailable` covers combat, cooldown and nothing to refund; lore gives the reason in words. Lore does not tick by itself, so rewrite it on click or on open.
- Free points as a number: an item amount above 1 shows a count, but 1 shows none and 0 is impossible [U for how it looks]. Keep it in the info tooltip unless A1 asks for a badge.
- A dynamic number written as title text would go stale after in-place purchases. Do not do it.

## Node states
| State | Meaning | Item key suffix |
|---|---|---|
| locked | a gate is unmet (level, connection, points) | `locked` |
| available | can be bought now (including enough free points) | `available` |
| confirm | clicked once; click again to buy [P look] | `confirm` |
| owned | bought | `owned` |
| sealed | n7-n9 | none (painted) |

- Not enough free points: show `locked` with the reason in lore [P].
- Owned and bought during this opening ("undoable"): same `owned` art; say it in lore.
- No `excluded` or `blocked` art until keystones exist.
- Lore always names the state in words. Reset `confirm` whenever the player clicks something else or changes page.

## Connectors and the slot gap
Slot item areas are 16x16 GUI on an 18 px pitch, so there are **2 GUI px (4 art px)** between neighbours [D].
- **Recommended:** each lit piece fills its own 32x32 groove segment. In the background, paint a stone clamp or iron staple across the 4 px gap. A lit path then reads as light seen between clamps, with no unsupported rendering.
- **Optional, prototype only:** `"oversized_in_gui": true` (top level of the items JSON) with a 36x36 texture and `gui` scale 1.125 for a gapless line. Mojang does not officially support drawing outside the slot [V] ([wiki](https://minecraft.wiki/w/Items_model_definition)), and overlap order between neighbours is [U].
- Groove geometry in a 32x32 tile [P]: 8 px band at x or y **12..20** (half-open), matching the painted groove exactly. `corner_es` runs from the centre to the east and south edges; `corner_sw` to the south and west edges. Everything outside the band is transparent.
- Connector items have their tooltip hidden.

## Per-class backdrops
- Layout, frame, sockets and grooves come from one shared function; class only changes backdrop layer, accent ramp and emblem. This keeps every page pixel-aligned.
- Build only Warrior now. Class and branch are parameters of the generator.
- Glyph characters [P] (in use: `E001-E008` class select, `E101-E110` confirm [R `titles.json`]):

| Class | Block | Order |
|---|---|---|
| Warrior | `U+E201-E218` | guardian A, guardian B, berserker A, berserker B, duelist A, duelist B; each TL, TR, BL, BR |
| Archer / Mage / Captain (later) | from `U+E221` / `U+E241` / `U+E261` | same order |
| Loadout menu | from `U+E281`, 4 per background | |

Warrior example: guardian A `E201-E204`, guardian B `E205-E208`, berserker A `E209-E20C`, berserker B `E20D-E210`, duelist A `E211-E214`, duelist B `E215-E218`.

- The title string is the same shift pattern as the class menu: `pack.title([TL, TR, BL, BR])` [R `pixelkit/pack.py`]; `titles.json` gives the escaped strings for `messages.yml`.
- A visible branch name is painted into the header.

## Pack file layout
```
resourcepack/assets/arkenmmo/
  font/gui.json                                  + 12 bitmap providers
  textures/font/gui/tree_warrior_<branch>_<a|b>_{top,bottom}.png      352x222
  textures/item/gui/skill/warrior/<skill>/{locked,available,confirm,owned}.png   32x32
  textures/item/gui/skill/warrior/cleave/owned.png
  textures/item/gui/skill/warrior/link/{h,v,corner_es,corner_sw}.png  32x32
  textures/item/gui/button/{reset,reset_confirm,reset_unavailable}.png  32x32
  models/item/gui/...                            same relative paths
  items/gui/...                                  same relative paths
```
`items/gui/skill/warrior/shield_bash/owned.json`:
```json
{ "model": { "type": "minecraft:model", "model": "arkenmmo:item/gui/skill/warrior/shield_bash/owned" } }
```
`models/item/gui/skill/warrior/shield_bash/owned.json`:
```json
{
  "parent": "minecraft:item/generated",
  "gui_light": "front",
  "textures": { "layer0": "arkenmmo:item/gui/skill/warrior/shield_bash/owned" }
}
```
Component value: `arkenmmo:gui/skill/warrior/shield_bash/owned`. Item textures must stay under `textures/item/` (items atlas).

Previews and sources go in `design/` or `target/previews/gui/`, never in `resourcepack/`.

## Plugin side
- Reuse `menu.Menu` and `MenuListener` [R]. `button(...)` already calls `setItem`, so calling it again on the open `Menu` updates a slot in place. For a slot with no action (an empty or lit connector), the class has no method to clear or set an action-free icon yet; a small addition is needed.
- `Menu` actions are `Consumer<Player>` and **do not receive the click type** [R]. The draft's right-click-to-undo would need that changed. The decision only says purchases "can be undone", so clicking a just-bought node twice would also work. Pick one in the brief.
- Page switch (tab or scroll): build a new `Menu` with the other title, fill it, open it. `MenuListener` already runs actions on the next tick. Do not close first. Cursor staying put is [U].
- State change: rewrite the node slot, affected connector slots, other nodes whose availability changed, reset and info. Do not reopen.
- Items as in `ClassMenus.icon` [R]: `PAPER`, `ITEM_MODEL`, `ITEM_NAME`, `LORE` (italic off), `TOOLTIP_STYLE` `arkenmmo:warrior`.
- Connectors: `TOOLTIP_DISPLAY` with `TooltipDisplay.tooltipDisplay().hideTooltip(true).build()`.
- Don't set the enchantment glint for state.
- Re-check eligibility on each click and again on the confirming click.
- Open only with the pack loaded, as for the class menus.

Slot map as data: per view, a list of `(slot, node)` and `(slot, shape, edge)`; branches share it, classes share it.

## Pitfalls
- Missing items JSON shows the missing model; one bad font provider breaks the whole `arkenmmo:gui` font, including class selection.
- Art and slot map drifting apart: derive both preview and sockets from `layout.cell(col,row)`.
- A forgotten `<white>` darkens the art.
- An empty slot beside lit ones is correct for unlit track; don't fill it with an opaque item.
- `mise run validate-assets` may not check font PNGs; inspect the previews.
- The title's "Inventory" label and the player-inventory cells need the same treatment as the class menu.
- Not verified in a 26.3 client: item over glyph draw order, cursor position on reopen, exact player-row positions.

## Sources
- `docs/research/custom-gui-and-pixel-art.md` and its source list
- https://minecraft.wiki/w/Items_model_definition
- https://minecraft.wiki/w/Model
- https://docs.neoforged.net/docs/resources/client/models/items
- https://docs.neoforged.net/docs/resources/client/models/
- https://docs.phoenixdevt.fr/mmocore/features/skill-trees.html (a Minecraft plugin with chest-menu trees: node states, paths lit when both ends are unlocked, arrow scrolling)

## Hand-off

### Proposed contract IDs
| Kind | ID |
|---|---|
| Node item models | `arkenmmo:gui/skill/warrior/<skill>/{locked,available,confirm,owned}` for the 18 branch skills (`<skill>` = contract ID without `warrior.`); `arkenmmo:gui/skill/warrior/cleave/owned` |
| Connectors | `arkenmmo:gui/skill/warrior/link/{h,v,corner_es,corner_sw}` |
| Reset | `arkenmmo:gui/button/{reset,reset_confirm,reset_unavailable}` |
| Invisible | `arkenmmo:gui/blank` (exists) |
| Title keys in `titles.json` | `tree_warrior_{guardian,berserker,duelist}_{a,b}` |
| Glyphs | `U+E201-E218` as above; `U+E281+` loadout |
| Tooltip style | `arkenmmo:warrior` (exists) |

The brief says these are fixed **after the A1 art layout is approved**.

| Who | Next |
|---|---|
| **model-designer** (plain pack) | A1: one view A page (suggest Guardian) with sample icons and all four states, one lit and one unlit edge, plus a view B mock showing sealed stones, Cleave plinth and footer. Preview from real pack files at GUI scales 2, 3, 4. A2: 6 masters, 80 item sets, font providers, `titles.json`, loadout background. Script-generated through `pixelkit/`; do not set `oversized_in_gui` unless a prototype was approved |
| **plugin-coder** | Slot maps above, in-place updates, `Menu` addition for action-free icons, title swap for tabs and scroll, click-twice with the `confirm` model, reset on 49 on every page, title strings in `messages.yml` from `titles.json` |
| **sound-designer** | Contract events only; no hover sound (the server cannot detect hover) |
| **vfx-designer** | Nothing for the GUI |
| **main session / user** | Decide at A1: Cleave placement, confirm step on reset, undo gesture |
