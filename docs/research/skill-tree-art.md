# Skill tree and skill icon art: readability, states and ancient carving

## Target version
**Paper 26.3**, plain vanilla pack. Art rules here sit **inside** `design/gui-style-guide.md`, which wins on any conflict: frozen palette, 2x grid, top-left light, binary alpha, important detail at least 2 art px. Layout, IDs and files: `skill-tree-gui.md`. Checked 2026-11-26.

**How far to trust this:** I read text pages only and **looked at no reference images**. I found no authoritative MMO skill-icon guide. Sources support the principles in "What the sources say"; the pixel numbers, motifs and colour steps are **proposals [P]** that have not been rendered. Learn technique only; copy or trace no artwork, symbol or layout art.

## Summary
1. One icon is one bold carved symbol: unique **silhouette**, at most 3 parts, strokes at least 3 art px, in a 22x22 area of the 32x32 node.
2. Actives are **square** stones, passives **octagonal**.
3. State is carried by **value and shape**, then colour. Class colour appears only on owned things.
4. Carving is **sunken**: shadow on the top and left inner wall, light on the lower and right lip. Glow is pigment filling the groove.
5. The backdrop stays quieter than every socket. Invent all runes; use no real runic letters.

## Version notes
Nothing here is version-specific, apart from the 2x grid behaviour in the GUI note (exact at GUI scales 2 and 4, uneven at 3).

## What the sources say
| Finding | Source and strength |
|---|---|
| An ability icon must be understood at a glance and be clearly unlike the others, with enough contrast, without distracting | [N. Inman](https://nathanielinman.com/ability-icon-user-experience/): a short personal article |
| Design the silhouette first; limited palette and high contrast keep small pixel icons readable | [Pathbits](https://app.pathbits.com/articles/designing-readable-item-icons-in-top-down-pixel-art): blog, seen in a search summary only |
| World of Warcraft's trees use squares for actives, circles for passives and octagons for choices | [Icy Veins and others](https://icy-veins.com/wow/dragonflight-talent-system-guide): search summary only (the page returned 403). The shape **principle** is what we take |
| A Minecraft chest-menu tree (MMOCore) has distinct locked, unlockable and unlocked node states; a path lights when both ends are unlocked | [MMOCore docs](https://docs.phoenixdevt.fr/mmocore/features/skill-trees.html) |
| Locked: faded and quiet. Available: full strength with a subtle highlight. Done: an accent fill. Lines into locked nodes are dimmer | [Tree Wiki](https://treeapp.io/wiki/how-nodes-are-rendered/): a project-tool wiki, not a game |
| Never rely on colour alone; add shape, symbol or text | [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/) |
| Visual cues for state and needed parts of graphics: 3:1 contrast; inactive controls are exempt | [WCAG 2.2, 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): a web standard used as a yardstick |
| Many runes are built from vertical staves and angled branches; the wood-grain explanation says horizontal cuts were avoided. Not absolute | [Wikipedia: Runes](https://en.wikipedia.org/wiki/Runes) (first part of page read) |
| Runestones were often painted, mainly red (and black, white), with colour on the cut runes; inscriptions sit inside bands, often serpent-shaped | [Wikipedia: Runestone](https://en.wikipedia.org/wiki/Runestone) (first part of page read) |
| With upper-left light, relief drawing puts shadow lines lower right for raised relief and **reverses** this for sunk relief | [Digital Epigraphy](https://www.digital-epigraphy.com/tutorials/lets-talk-about-sun-and-shadow-a-fundamental-update-on-drawing-drop-shadow-transitions-in-photoshop): Chicago House method |
| Runes such as Othala, Tyr and the doubled "SS" bolts are catalogued as appropriated hate symbols (context matters) | [ADL Othala](https://www.adl.org/resources/hate-symbol/othala-rune); Tyr and SS bolts from a search summary of the same database |

Not found: a skill-icon guide from a game studio, Wynncraft's node and connector art rules, and a pixel-art stone-carving tutorial with usable rules in readable text.

## Node tile (32x32 art = 16x16 GUI) [P]
| Zone (inset from the tile edge) | Use |
|---|---|
| 0-1 | state ring, 2 px |
| 2-3 | inner halo (owned only), otherwise plate bevel |
| 4 | plate, one quiet pixel |
| 5-26 (22x22) | **glyph safe area** |

- **Active:** square with 2 px stepped corners. **Passive:** octagon with about 7 px stepped 45-degree corners. The outline must differ in solid black. **Cleave** (core): square with a second thin ring or four rivets.
- The painted socket in the background (36x36) is neutral for both shapes, or follows the node's shape if baked per page. It must not make the octagon read as a square: keep transparent tile corners over dark socket stone.
- Only 16x16 GUI is available. The glow stays **inside** the tile; no halo outside it.

### Icon rules
1. One idea per icon: one primary shape plus at most one secondary cue (impact, motion, drop).
2. Primary strokes **3-5 px**, secondary at least **2 px**, gaps between strokes at least **3 px**. No 1 px detail that carries meaning.
3. The primary shape spans at least 18 px in one direction.
4. Angles: vertical, 45 degrees and 2:1 steps. Use arcs only where the idea needs them (cleave, spiral, shout), with clean monotonic pixel steps.
5. Carved look: filled cut shapes, not thin outline drawings. No perspective, no painted objects, no text, numbers or faces.
6. **One master mask per icon.** All four states are generated from it, so a locked rune is recognisably the same rune when lit.
7. Design in flat black and white first. Approve the 19 silhouettes together before any shading.
8. No two icons may be mirror images, rotations or recolours of each other.
9. Weapons appear in only a few icons; five similar swords would be unreadable. Reuse no primary shape.
10. The class colour is the same on all Warrior icons, so branch and skill identity come from shape alone.

### Original motif suggestions [P]
Starting ideas only; the model-designer may change them after the silhouette sheet.

| Skill | Type | Primary shape | Secondary |
|---|---|---|---|
| Cleave | core | one wide crescent sweep | straight cut across it |
| Shield Bash | A | pointed shield, left of centre | two impact wedges right |
| Iron Hide | P | three overlapping scale plates | - |
| Stalwart | P | broad trapezoid standing stone, wider at the base | ground bar with two roots |
| Challenging Shout | A | open horn or maw wedge | three angular sound bars |
| Second Wind | P | rising double hook (updraft) | one drop at its core |
| Bulwark | A | crenellated wall block with three merlons | - |
| Leaping Strike | A | high arc ending in a downward point | ground split under it |
| Bloodthirst | P | large drop | two fangs notched out of it |
| Fury | P | three rising claw cuts | - |
| Whirlwind | A | square-stepped spiral with blade tip | - |
| Relentless | P | two stacked forward chevrons | third, broken one behind |
| Execute | A | broad headsman's blade falling vertically | block bar below |
| Lunge | A | long diagonal thrust point | two trailing speed cuts |
| Footwork | P | two staggered angular bootprints | - |
| Focus | P | angular eye | diamond pupil |
| Riposte | A | vertical blade | hooked return arrow around one side |
| Opportunist | P | short dagger striking from upper right | half-ring showing a turned back |
| Hamstring | A | bent leg silhouette | diagonal cut gap through it |

Watch these confusion pairs side by side: Cleave / Whirlwind / Second Wind (curves); Execute / Riposte / Lunge / Opportunist (blades); Leaping Strike / Lunge (movement); Shield Bash / Bulwark / Iron Hide (defence); Fury / Relentless (repeated strokes).

## States [P], using only frozen ramps
Step numbers are 0-based indices, as in `palette.col(ramp, step)`. Plate: `iron` 2. Socket and gaps: `iron` 0-1. Ratios are my own arithmetic from the hex values (approximate).

| State | Ring (outer 2 px) | Groove floor of the glyph | Extra shape cue | Reads as |
|---|---|---|---|---|
| locked | none; stone edge only | `steel` 3 (about 2.4:1 on the plate: dull but identifiable) | none | dull rune |
| available | continuous `steel` 3 (about 3:1 on `iron` 1) | `steel` 5 (about 8:1) | the ring itself | faint edge |
| confirm | as available | `steel` 6 | four `gold` 4 corner brackets, at least 2 px thick and 6 px long | "click again" |
| owned (Warrior) | `crimson` 3 (about 3:1 on `iron` 1) | `crimson` 4 with a `crimson` 5 core (about 7:1 on `iron` 2) | 2 px inner halo (`crimson` 2 fading to 1) and four corner studs | soft still glow |

- **Glow without partial alpha:** tiles are baked on a known plate, so paint the glow as opaque palette steps: bright core, groove edge one or two steps down, halo darker again. One or two px of ordered dither at the outer edge is acceptable.
- Soft means: no white-hot core, no step 5 in the ring, no animation. Owned must be obvious next to available, not next to the window frame.
- **Greyscale risk:** owned crimson ink and available pale steel are close in value, and `crimson` 1 is close to `iron` 2. The studs, halo and lit connectors must separate them. Test in greyscale and strengthen the **shape**, not only the colour.
- Later ramps [P]: Archer `forest`, Mage `violet` or `arcane`, Captain `gold` with `navy`. Measure each. For Captain, gold also marks `confirm`, so the brackets must work by shape.

## Tree layout and connectors
- **Hierarchy, loudest first:** confirm, owned, available, lit paths (no louder than owned nodes), locked, sockets, grooves, sealed stones, backdrop.
- **Unlit groove:** an 8 art px sunken channel: floor `iron` 0, 2 px shadow side, 1-2 px lit lower lip. Visible enough to trace the tree before buying anything.
- **Lit piece:** 4 px centre in `crimson` 4 (occasional `crimson` 5 pixel clusters), 2 px each side `crimson` 2. Same still glow as the nodes.
- **Clamps:** every 4 px slot gap on a groove gets the same stone key or iron staple. Make it look structural, with identical spacing on unlit and lit paths.
- Corners are chamfered 45-degree steps, mirrored in geometry but shaded for top-left light.
- Tier reading: faint horizontal strata or worn tally notches in the side margins (columns 0-1 and 7-8), without numbers.
- **Cleave plinth:** its own base, clearly not part of the path network.
- **Footer:** one stone or iron ledge separates it from the tree. Active tab differs by shape (raised, joined to the ledge, marker bar), not just brightness. Reset: a broken or returning ring symbol, in neutral steel when ready, gold brackets in confirm, flat and dim when unavailable. It must not look like Whirlwind or any tab sigil.

## Sealed stones (n7, n8, n9)
- A rough plug set **into** the socket, with an irregular outline unlike both node shapes.
- No symbol that hints at a skill: weathered scratches that stop mid-stroke, a crack, two crossing iron bands or a clay-like seal.
- Dark values (`iron` 1-3, `ember_stone` low steps), no ring, no class glow.
- The ultimate seal may be larger in the **painted** art, reaching into free margins but not onto another slot's item area.
- Their grooves look filled with grit, so players read "not yet", not "locked by level".

## Dark ancient stone: construction rules
1. **Big forms first:** 2-4 large slabs per page with chipped, stepped edges. No uniform tiny brick noise behind the tree.
2. **3 tones per surface**, with a 1-2 px lit top and left arris and a shadow lower right. Reuse the guide's facet logic.
3. **Sunken cut** (rune, groove, socket), light from top left: 1 px dark wall on the **top and left inside**, darker floor, 1 px lit lip along the **bottom and right**. This matches the guide's "recesses reverse the bevel". Raised things (clamps, active tab) do the opposite. Test: a rune that seems to pop out has its light on the wrong side.
4. **Weathering:** a few long cracks that branch at angles, each with a 1 px lit lower edge; corner chips; sparse clustered pits. No single-pixel speckle, no pillow shading. Dither only to move between close values.
5. Weathering stays **out of** glyph areas and off grooves. A crack must never look like a connector.
6. **Faint carvings:** within about one palette step of the slab (roughly 1.3:1 or less). Visible when looked for, gone at a glance. Never class-glow, never ring-, square- or octagon-framed (false buttons), at least 4 art px clear of sockets and grooves.
7. **Ancient composition:** winding carved bands around the page margins (from the inscription-band idea), made of original interlace or stepped geometry; worn edges; fragments of larger carvings cut off by the frame.
8. **Mystery** comes from incompleteness and darkness: partial carvings, one dim half-buried shape behind the tree, no bright props or skies.
9. Warrior backdrop: `ember_stone` and `iron`, with `ember_sky` low steps for depth. Per class later: `dusk_forest`, `night_teal`, `dawn_stone`. One shared slab layout and frame; change ramp, emblem and carving motif only.
10. Use only frozen ramps. If a stone value is truly missing, ask for a palette change instead of adding a colour.

## Rune safety
- Do **not** use real Futhark letters as decoration or icons, and no real words. Invent stave-like marks from vertical and diagonal cuts that spell nothing.
- Avoid in particular: the Othala shape (diamond with two feet, with or without wings), single or paired lightning bolts, the up-arrow Tyr shape, the Y-with-centre-stroke shape and its inverse, sunwheels, swastika-like rotating hooks and round multi-bolt "sun" designs. Only Othala was checked on its ADL page; the rest are precaution.
- Check this explicitly for random generated scratches and for square spirals (Whirlwind): no four-armed rotation.

## Review checklist (add to the style guide's checks)
- [ ] 19 solid-black silhouettes on one sheet: each nameable and no two confusable, active and passive outlines distinct.
- [ ] Sheet at 1:1 art (what GUI scale 2 shows) and at 1.5x nearest (GUI scale 3). GUI scale 4 also.
- [ ] Squint or blur sheet: primary shapes still differ.
- [ ] All 19 in locked state are still identifiable.
- [ ] Greyscale: locked, available, confirm and owned are told apart in a mixed row **without** lore; lit paths stand out from unlit.
- [ ] An empty tree is traceable; a full branch is not loud.
- [ ] Squinting at a page shows nodes and paths first; no backdrop mark looks clickable.
- [ ] All cuts are lit consistently as sunken.
- [ ] Sealed stones reveal nothing.
- [ ] No real or risky rune shapes.
- [ ] Only frozen colours, alpha 0 or 255, no resampled parts.
- [ ] Nothing copied or traced from a reference.

## Pack file layout
See `skill-tree-gui.md`. Hand-drawn icon masks (text grids for `pixelkit/grid` style input) belong under `design/`, not `resourcepack/`.

## Plugin side
None, beyond naming the state in lore and using the `confirm` model.

## Pitfalls
- Judging only at x8 zoom (lesson of 2026-11-25: eyes vanished at GUI scale 3).
- 1 px carving walls vary in width at GUI scale 3; meaning must live in the 3 px floor.
- Shading each state by hand lets icons drift; generate states from one mask.
- Heavy stone texture destroys 32 px icons.
- With the transparent slot highlight, nothing reacts to hover: buttons must look like buttons.

## Sources
- https://nathanielinman.com/ability-icon-user-experience/
- https://app.pathbits.com/articles/designing-readable-item-icons-in-top-down-pixel-art
- https://icy-veins.com/wow/dragonflight-talent-system-guide
- https://docs.phoenixdevt.fr/mmocore/features/skill-trees.html
- https://treeapp.io/wiki/how-nodes-are-rendered/
- https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- https://en.wikipedia.org/wiki/Runes
- https://en.wikipedia.org/wiki/Runestone
- https://www.digital-epigraphy.com/tutorials/lets-talk-about-sun-and-shadow-a-fundamental-update-on-drawing-drop-shadow-transitions-in-photoshop
- https://www.adl.org/resources/hate-symbol/othala-rune
- Pixel art basics already cited in `custom-gui-and-pixel-art.md` section 6

## Hand-off
**Contract IDs:** as in `skill-tree-gui.md`.

| Who | Next |
|---|---|
| **model-designer** | A1 in this order: (1) 19 black-and-white silhouettes on one sheet; (2) state recipe on 4-6 sample icons including one active, one passive and one confusion pair, with greyscale; (3) stone page with grooves, clamps, one lit path; (4) view B mock with sealed stones and footer. Show previews for approval. A2: all states from one mask each. Record approved rules in `design/gui-style-guide.md`, replacing its "Skill tree (next GUI, not started)" notes |
| **vfx-designer, sound-designer** | Nothing from this note. If world effects echo icons, reuse the idea, not the GUI textures |
| **plugin-coder** | State names in lore; nothing else |
| **main session / user** | A1 approval gate |
