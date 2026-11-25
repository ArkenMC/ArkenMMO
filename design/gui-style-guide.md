# GUI style guide

Rules for every class panel. The Warrior panel is the reference. The palette is frozen: `design/scripts/pixelkit/palette.py` is the source, and art may use no other colour.

**Status:** waiting for the user's approval of the Warrior panel (task A1). Changes asked for at that gate update this file first.

## Direction
Chunky, faceted blocky heroes, like painted miniatures: flat planes with 3-4 tones per surface, bright trim, big head, oversized weapon, three-quarter pose turned toward the centre of the menu. Original designs only.

## Grid and light
- All our art is on the 2x grid (2 art px per GUI px). No scaled, rotated or smoothed bitmaps. Rotate geometry before it is rasterised.
- One key light from the **top left**. Faces get ramp steps from their normal: top +2, lit flank +1, front 0, turned away -1 or -2.
- Alpha is 0 or 255.
- Anything important must survive GUI scale 3 (1.5 screen px per art px): glows, eyes and lettering are at least 2 art px thick.

## Frozen palette (dark to light)
| Ramp | Hex | Use |
|---|---|---|
| `crimson` | `#2b0f1e` `#561826` `#8a2430` `#bd3a32` `#e06a3c` `#f4a65a` | Warrior identity, eyes, rim light |
| `steel` | `#12101c` `#232436` `#3b4058` `#5c6580` `#8a94a8` `#bcc4cf` `#eef0ec` | armour, blades, arrow |
| `leather` | `#26141a` `#45251f` `#6b3d27` `#94603a` `#bd8a55` | belts, grips, wood |
| `gold` | `#3d2415` `#6e4318` `#a8721f` `#dca636` `#f6d86b` `#fff3b8` | trim, frames, lettering |
| `parchment` | `#8c6a4a` `#b99768` `#dcc291` `#efdcb0` | "Inventory" plate |
| `ember_sky` | `#141019` `#1d1828` `#292138` `#3d2840` `#572e3e` `#763a3a` | Warrior sky and fortress |
| `ember_stone` | `#18131d` `#251d29` `#342833` `#47363e` `#5d474a` | Warrior floor and dais |
| `dusk_forest` | `#0e1517` `#131f20` `#1a2a29` `#233733` `#2f473d` | placeholder panel, Archer backdrop base |
| `iron` | `#0d0b14` `#1a1925` `#282a39` `#3a3e50` `#525869` `#747b8a` | page frame, inventory cells |

Changed from the research proposal: the sky ramp was re-cut from wine-red to **cool plum at the top and warm ember at the horizon**, because red on red lost the crimson figure's hue contrast. `iron` and the backdrop ramps are new.

The other classes add their identity ramps from section 6.4 of `docs/research/custom-gui-and-pixel-art.md` (forest, violet, arcane, ivory, navy, skin) plus one sky and one ground ramp each. Check them in a render, tune once, then add them to this table and freeze them.

## Colour budget
At most 28 colours per figure (Warrior: 22) and 64 per panel (Warrior: 39). Per figure: identity about half, support about 30 %, accent about 10 %.

## Figure rules (shared so the four panels look like one set)
- Built with `pixelkit/hullrig.py`: every part is a convex hull, so plates are chamfered or tapered blocks and the light is consistent. Camera yaw 24 degrees, pitch 10 degrees, orthographic. The right-hand panels use **negative yaw** so their heroes face left; the light stays top left (do not mirror a rendered image).
- Size: 110-132 art px wide and 145-165 tall, at least 4 px inside the panel interior (`check_inside` fails the build if it is clipped).
- Head about 1/3 of the height. The Warrior's helm centre is about 100 px above the ground line; keep the other heads within 10 px of that, except for hats and banners.
- Ground line: feet about `interior bottom - 10`, standing on a dais with a hard-edged contact shadow.
- Pose: lean the upper body about 4-5 degrees toward the centre (`_lean` in `warrior.py`), feet staggered in depth, weapon breaking the outline on a diagonal or vertical.
- Outline: 2 px in step 0 of the neighbouring material, with the outer ring lifted to step 1 on lit edges. Inner separation lines are 1 px in the farther material's darker step. Contact shadows are one step down, offset down and right. No distance-based shading.
- Large faces stay at mid steps. Steps 4-5 of a colour ramp are for top faces and trim, otherwise crimson turns orange.
- Rim light: 1 px bounce in the backdrop's warm or cool colour on right-facing edges, never on blades or horns.
- Clean-up order: render, rim light, `despeckle()`, then hand-placed pixel grids (eyes, hand, faces, emblems). Grids come last, so their glints survive.
- Faces and hands are hand-placed grids. The renderer alone cannot make them read.
- Silhouette: one dominant shape per class (research table 6.2) with at least two features that show in solid black. Warrior: wide and low, hooked cleaver, swept crest teeth, shoulder horn, tower shield. **Captain must differ from this** with a tall banner pole, a swallowtail flag and a cape sweep, with no tower shield, horn pauldron or raised blade.

## Backdrop rules
Five layers, all darker and quieter than the figure:
1. Vertical sky of one ramp, with 8 px dithered transitions only.
2. Faint rays and a halo disc with one ring, centred behind the head.
3. A far silhouette and a near silhouette (the near one darker), each with a 1 px lit crest.
4. Floor with perspective seams, then the low octagonal dais (top step 4, front 2, shadow side 0).
5. A few embers or motes. Lit windows stay 2x4 px and dim.

## Page chrome (identical on every page; only panels, pips and arrow change)
- Outer shell: iron, 2 px dark outline and a bevelled rim, opaque over the whole vanilla panel. Only one GUI px per corner is clear.
- Header: recessed plaque with a double gold line, `CHOOSE YOUR CLASS` in pixel capitals, gem ornaments.
- Panel frame: 7 px (2 dark, gold, 2 iron, inner gold, dark) with gold corner brackets on the top corners. It reaches 3 GUI px outward on the outer edge.
- Divider: crossed-swords crest, fluted shaft, two page pips (large lit gold = current), and a raised gold button with a steel block arrow over slots 40 and 49.
- Inventory: recessed iron cells on the exact slot grid; parchment plate under the vanilla label; nothing busy.

## Lettering and name plates
- `pixelkit/lettering.py`: 12x16 capitals with 3 px strokes, 2 px gap, a lit top row, a 2 px dark ring and a 1 px drop. Only the letters in use are defined; add M, G, P, T, N and the rest to the same grid in A2.
- Plate: the bottom slot row, a notched banner with a trim line (light above, dark below) and a field in the class ramp (step 2 above, 1 below, 0 at the bottom). Letters are `gold` 5/4 with a `steel` 6 bevel; the Captain may use ivory.
- A plate in dim iron lettering means "not available yet".

## Checks every round
`mise run assets`, then look in `target/previews/gui/`: the x8 panel, the menu at GUI scales 2, 3 and 4, silhouette and greyscale, leak and slot views, and the printed colour counts. Work through section 6.6 of the research note. Judge the result at screen size, not only zoomed in: the first eyes looked fine at x8 and vanished at scale 3.
