---
name: gui-263-verified
description: Verified 26.3 facts for custom GUI backgrounds, fonts, invisible items, pack.mcmeta, pack delivery
metadata:
  type: reference
---
Checked 2026-11-25. Full write-up: docs/research/custom-gui-and-pixel-art.md. URLs: [[gui-sources]].

- Resource pack format 26.3 = 97.1 (26.2 = 88.0, 26.1 = 84.0). mcmeta: min_format/max_format only.
- Glyph cell max 256x256; ascent <= height or whole font fails; advance = ink width*scale + 1.
- Glyph top (panel coords) = 13 - ascent; title pen (8,6), colour 0x404040; label (8,128) drawn over title. Measured on 26.1.2 by a third party (materione), not re-checked on 26.3.
- Slots draw above title art only if inside the title's bounds (keep a full 176x222 glyph).
- Items atlas (1.21.11+): item textures under textures/item/.
- oversized_in_gui: top level of items JSON, not officially supported.
- InventoryView#setTitle deprecated/broken; MenuType.GENERIC_9X6.create(player, Component) exists.
- tooltip_style x -> textures/gui/sprites/tooltip/x_{background,frame}.png; vanilla nine_slice 100x100, border 9 / 10 + stretch_inner.
- ItemsAdder (volatile, 2026-11-25): stable 4.0.18 does not support 26.3; only 5.0.0 betas (Discord). docs/integrations.md says 4.1.0 (outdated).
- Pillow: Image.resize defaults to BICUBIC (pass NEAREST); ImageDraw.rectangle end point inclusive.
- User decisions 2026-11-25: 2 classes per page, 2 pages; classes Warrior, Archer, Mage, Captain; plain pack recommended.
- Unverified: player-inventory slot y (139/197 from own knowledge), per-item highlight disable (none found), configure-phase pack wait.
