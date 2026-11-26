# GUI style guide

Rules for every class panel and menu screen. The Warrior panel is the reference. The palette is frozen: `design/scripts/pixelkit/palette.py` is the source, and art may use no other colour.

**Status:** the Warrior panel and page frame (A1, commit `2ff9e7c`) were **approved by the user** on 2026-11-25. The user then asked for the style to be "a bit more minecraft ish" (a subtle shift, same artwork). On the next round the user asked to combine both: the stone bricks, square sparks and boxier helm and plates stay, while the **A1 cleaver and eyes are restored**. The same round asked for a readable Archer draw and a polished Mage beard and Captain moustache. All of that, and the other three classes, **waits for the user's approval**. The approved A1 render is kept in `design/scripts/reference/page1_approved_a1.png`; `target/previews/gui/warrior_before_after.png` compares it with the current Warrior. The page frame is unchanged.

## Direction
Chunky, faceted blocky heroes, like painted miniatures: flat planes with 3-4 tones per surface, bright trim, big head, oversized prop, three-quarter pose facing the centre of the menu. Original designs only. No Mojang textures are copied or traced.

## Minecraft touches (subtle: they season the faceted style, they do not replace it)
- **Boxy heads and plates:** chamfers are 1-2.5 units, helms and hoods are near-cubes, limbs are near-cuboids with a little taper. No plain player-skin mannequins, and the faceted shading stays.
- **Square eyes:** two squares per eye, white outside and iris inside, 4-5 art px each (`block_eye`), with a dark lid row under pale brows. Exceptions: the Warrior keeps his slanted A1 eyes, and the Captain's eyes have lid and brow as one stroke with bare skin around them (a frame all round reads as spectacles).
- **Stair-stepped item edges:** groups listed in `Figure(blocky=...)` are snapped to a screen-aligned 4 px grid: bows, crests, hat tips, flags, cloth hems and plumes. Do not snap the Warrior's cleaver (the user chose its smooth A1 edge), faces, armour, hands or anything whose shape needs a curve (the pauldron horn and war horn stay smooth).
- **Square effects:** flames, sparks, notes and motes are drawn in square blocks.
- **Block backdrops:** stone-brick courses, block trees, stepped hills and tents, rectangular clouds, a stair-stepped halo disc, a dais with block joints.

## Grid and light
- All our art is on the 2x grid (2 art px per GUI px). No scaled, rotated or smoothed bitmaps. Rotate geometry before it is rasterised.
- One key light from the **top left**. Faces get ramp steps from their normal: top +2, lit flank +1, front 0, turned away -1 or -2.
- **A hero is never a flipped image.** Every hero is posed facing right; `build(-1)` mirrors the geometry and camera before lighting. Hand grids mirror with the pose; symbols with a reading direction (music notes) use `flip=False`.
- Alpha is 0 or 255 (tooltip backgrounds are the exception, at 240).
- Anything important must survive GUI scale 3 (1.5 screen px per art px): glows, eyes and lettering are at least 2 art px thick.

## Frozen palette (dark to light)
| Ramp | Hex | Use |
|---|---|---|
| `crimson` | `#2b0f1e` `#561826` `#8a2430` `#bd3a32` `#e06a3c` `#f4a65a` | Warrior identity, rim light |
| `forest` | `#0f2228` `#173a33` `#24573a` `#3f7a3c` `#6fa043` `#b4c95a` | Archer identity |
| `violet` | `#170f33` `#281a5c` `#3d2c8f` `#5a49c4` `#7b7ce8` `#a9b8fa` | Mage identity |
| `arcane` | `#12374f` `#1f6f9e` `#35b5c9` `#8ff0e4` `#e4fffa` | Mage magic and rim |
| `ivory` | `#4a465e` `#6e6a7e` `#aaa5a8` `#ddd6c4` `#f7f1dc` | Captain cloth and horn, white hair, eye whites |
| `navy` | `#101433` `#1b2658` `#2b3f82` `#425fae` `#6a8ad0` | Captain second colour |
| `skin` | `#4a2430` `#7d3f3a` `#b06a4e` `#d9976b` `#f2c498` | faces and hands |
| `steel` | `#12101c` `#232436` `#3b4058` `#5c6580` `#8a94a8` `#bcc4cf` `#eef0ec` | armour, blades, arrow |
| `leather` | `#26141a` `#45251f` `#6b3d27` `#94603a` `#bd8a55` | belts, boots, wood, beards |
| `gold` | `#3d2415` `#6e4318` `#a8721f` `#dca636` `#f6d86b` `#fff3b8` | trim, frames, lettering, Captain armour |
| `parchment` | `#8c6a4a` `#b99768` `#dcc291` `#efdcb0` | note plates, feathers |
| `ember_sky` / `ember_stone` | `#141019` `#1d1828` `#292138` `#3d2840` `#572e3e` `#763a3a` / `#18131d` `#251d29` `#342833` `#47363e` `#5d474a` | Warrior backdrop |
| `dusk_sky` / `dusk_forest` | `#0f1220` `#171d32` `#212b45` `#323c55` `#4c4a56` `#6d5a4c` / `#0e1517` `#131f20` `#1a2a29` `#233733` `#2f473d` | Archer backdrop |
| `night_teal` | `#0a0f18` `#0f1a26` `#142735` `#1a3643` `#214752` `#2d5e66` | Mage backdrop |
| `dawn_sky` / `dawn_stone` | `#10122a` `#191b3a` `#26254a` `#3a2f55` `#55395a` `#77485a` / `#171726` `#232338` `#33334a` `#46455a` `#5e5a68` | Captain backdrop |
| `iron` | `#0d0b14` `#1a1925` `#282a39` `#3a3e50` `#525869` `#747b8a` | page frame, inventory cells |

## Colour budget
At most 64 per panel (Warrior 39, Archer 50, Mage 45, Captain 44). Per figure the research note suggests 24-28; the Warrior has 22, but the Archer (33), Mage (32) and Captain (31) are over it, because each mixes more materials. Do not add ramps to a figure without removing one. Per figure: identity about half, support about 30 %, accent about 10 %.

## Figure rules
- Built with `pixelkit/hullrig.py` and painted through `pixelkit/figure.py`. Every part is the **convex hull** of its points: build stars, forks and notches from several convex pieces.
- Camera yaw 24 degrees (mirrored for left-facing), pitch 10 degrees, orthographic.
- Size: 120-136 art px wide, 150-160 tall, inside the panel interior (`check_inside` fails the build otherwise).
- Head about a third of the height; helm and head centres within about 10 px of each other, ignoring hats.
- Ground line: feet about `interior bottom - 10`, on the dais with hard-edged contact shadows.
- Pose: a lean, a staggered stance and a prop that breaks the outline. Keep **open sky between prop, limbs and body**, and keep a prop off the face and other key shapes (route a bowstring behind the head).
- Outline: 2 px in step 0 of the neighbouring material, the outer ring lifted to step 1 on lit edges. Inner separation lines are 1 px in the farther material's darker step. Contact shadows are one step down. No distance-based shading.
- Large faces stay at mid steps; the top steps are for top faces and trim.
- Rim light: 1 px of bounce on right-facing edges, never on blades, bows, strings or banners.
- Clean-up order: render, rim light, `despeckle()`, then the hand-placed details (eyes, brows, hands, flame, notes, hair).
- **Beards and moustaches** are not boxes. Draw them with `facet_art`: overlapping hand-shaped locks, each one flat tone with a darker inner rim, 1 px strand lines, lighter on the top left, and an outline against robe or skin. A moustache must differ from the beard in shape and value (the Captain's is two steps darker) and leave the mouth visible below it.
- **A drawn bow:** one string runs from each limb tip to the nock, and the draw hand hooks it. Pose it so the whole string lies in open sky between body and bow; it never passes behind the head or across the torso. The bow hand wraps the grip with the arrow resting above it, a gap of sky separates the bow arm from the arrow, and the arrowhead stands clear of the limb.

| Class | Silhouette | Identity | Prop | Rim |
|---|---|---|---|---|
| Warrior | wide, low, square | crimson + steel | hooked cleaver, tower shield | crimson |
| Archer | slim lunge, open bow arc, pointed hood | forest + leather | recurve bow at full draw, quiver | forest and leather highlights |
| Mage | tall triangle, bent block hat | violet + arcane | orb staff, square-pixel flame | arcane |
| Captain | pole above the head, swallowtail, cape sweep | gold + ivory + navy | banner, war horn, notes | gold and navy highlights |

Captain against Warrior is the confusion risk. Keep the Captain's open face, banner, cape and raised horn; he gets no tower shield, horn pauldron or raised blade, and he stays the brightest figure while the Warrior is among the darkest.

## Backdrop rules
Layers, all darker and quieter than the figure: a vertical sky with 8 px dithered transitions; faint rays and a stepped halo disc behind the head; one or two block clouds where they fit; a far and a nearer, darker silhouette, each with a lit 1 px crest; a floor with seams and the octagonal dais (top step 4, front 2, shadow side 0); a few square sparks. Hue should contrast with the figure (the Warrior's red stands on cool plum, the Mage's violet on teal). The floor must contrast too: the Archer stands on slate, not on green.

## Screen chrome
- Every screen: iron shell opaque over the whole vanilla panel (one GUI px per corner clear), header plaque with pixel capitals and gem ornaments, recessed inventory cells on the slot grid, parchment plate under the vanilla label.
- Class panel frame: 7 px with gold corner brackets on top; it may reach 3 GUI px outward on the outer edge.
- Class pages: crossed-swords crest, fluted shaft, two pips (large lit gold = current), gold button with a steel arrow over slots 40 and 49.
- Confirm screens: the chosen panel on the left, facing the buttons; the same pillar without pips or arrow; a parchment note "THIS CHOICE / IS FINAL"; a gold **Confirm** button (check icon and word) over rows 1-2; an iron **Back** button (arrow icon and word) over rows 3-4; a seal with a gem in the class colour. The buttons never rely on colour alone.

## Lettering and name plates
- `pixelkit/lettering.py`: 12x16 capitals with 3 px strokes, 2 px gap, a lit top row, a 2 px dark ring and a 1 px drop. `small()` is an 8x10 set with 2 px strokes, for dark-on-parchment notes only.
- Plate: the bottom slot row, a notched banner with a gold trim line and a field in the class ramp. Letters are gold 5/4; the Captain uses ivory.

## Tooltips
1x art, 100x100, nine-slice with vanilla's 26.3 `.mcmeta` values. Background pixels 8..91 with clipped corners, alpha 240, in the class's darkest colour (navy for the Captain). A 1 px frame at inset 9 in the class ramp, stepping darker downward (gold for the Captain), with a square 2x2 gold stud on each corner.

## Checks every round
`mise run assets`, then look in `target/previews/gui/`: each panel at x8, the contact sheet, the silhouettes (including Warrior against Captain), greyscale, every screen at GUI scales 2, 3 and 4, the slot views, tooltips and the printed colour counts. Work through section 6.6 of the research note, and judge at screen size, not only zoomed in.

## Skill menus
Spec: `design/gui-skill-tree.md`. References: `design/skill-tree-visual-research.md`. The user approved the Warrior preview on 2026-11-26; what came after it (other classes, off-page paths, loadout) still needs approval.
- **Mood:** dark, ancient, mysterious. One dim class carving behind the tree; no sky, no figures, no bright props.
- **Slab:** three close tones of the class stone sinking into `iron`, sparse pit clusters, a few hand-routed cracks. Weathering stays clear of grooves and seats.
- **Sunken cut:** shadow inside the top and left wall, light on the lip below and right. Raised things (clamps, buttons) are lit the other way.
- **Faint carvings:** unpainted, about one ramp step from the slab, partly worn away; no ring or button shapes, no real runic letters. No carving where many seats would cut it into fragments (loadout).
- **One mask per icon** (24x24 in the 32x32 stone), one bold shape, strokes 3 px or more, unique within its class. All states come from that mask.
- **State by value and shape:** locked slate rune 1 px thinner, no ring; available thin steel ring; confirm corner brackets; owned class glow plus rivets. Class colour only on owned things (and quiet traces in frame and backdrop).
- **Lit paths** stay one ramp step quieter than owned stones.
- **Shapes:** actives square, passives octagon, sealed stones rough plugs with blank iron bands.
- **Off-page paths:** a groove that leaves the view breaks the frame and ends in a head shaped like that direction's scroll arrow.
- **Hover text:** the class's tooltip style on every item; name in the class menu's name colour, archetype line under it in parchment, numbers in white. No `dark_gray` (unreadable on the class backgrounds). Lore lines at most 34 characters. Spec: `design/gui-skill-tooltips.md`.
- **Archetype names:** the three paths of a class are archetypes. Each tree page paints the full display name in capitals (`ARCHETYPE_NAMES`) in the large lettering, the same size everywhere.
- **Footer:** every clickable thing looks like a button (the slot highlight is invisible); the open tab stands taller with a class bar.
- **One layout for every class:** only stone ramp, glow ramp, gem and carving change (`pixelkit/treetheme.py`).
- The palette stays frozen; the skill menus needed no additions.
