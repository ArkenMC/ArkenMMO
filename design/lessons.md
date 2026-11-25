# Art lessons

- 2026-11-25: Convex-hull parts in a small renderer (`hullrig.py`) gave faceted, consistently lit armour on the first render. Hand-placing 2D polygons was not needed for the figure.
- 2026-11-25: A hilt hidden behind the fist and shoulder made the sword look stuck into the pauldron. Move the grip well in front, keep the crossguard and pommel clear, and check that the weapon reads as held.
- 2026-11-25: Faces and hands need hand-placed pixel grids. Ember eyes turned an empty visor into a character, and a 22x17 gauntlet grid replaced a grey blob.
- 2026-11-25: Eyes that read at x8 disappeared at GUI scale 3. Make the bright core at least 2 rows thick and always judge the 1280x720 sheet.
- 2026-11-25: A base step of 3 on crimson made large lit faces orange. Use base 2 with highlights capped, and keep steps 4-5 for top faces and trim.
- 2026-11-25: A smooth crest and a plain blade gave a blob in solid black. Swept crest teeth, a back hook on the cleaver and a shoulder horn fixed most of it. The torso is still one mass; plan negative space in the pose first for the next figures.
- 2026-11-25: A red-brown sky behind a crimson hero was muddy. A cool plum sky fading to a warm horizon separates better.
- 2026-11-25: Bright tower windows on walls with the same value as the sky looked like floating red bars. Get the silhouette to read first, then keep windows tiny and dim.
- 2026-11-25: A part group of its own gets separation lines; a cheek plate in its own group drew a "moustache". Give flush sub-plates the same group as their parent, and close gaps in the geometry.
- 2026-11-25: Parts that are almost fully covered (the horn under the blade) leave stray nubs. Remove them.
- 2026-11-25: `despeckle()` after the render took the figure from 85 lone texels to about 11, all deliberate eye and gauntlet highlights.
- 2026-11-25: Name plate lettering with its ring and drop needs one clear field row before the trim; fill enclosed holes in the ring.
- 2026-11-25: Passes: about 17 render, look and fix rounds for page 1.
