---
name: gui-sources
description: URL cache for GUI / font / item model / pixel art research, with dead ends
metadata:
  type: reference
---
Format: URL | confirmed | checked | stable/volatile. All checked 2026-11-25.

- https://minecraft.wiki/w/Pack_format | rp 26.3=97.1, 26.2=88.0, 26.1=84.0, 1.21.11=75.0 | volatile
- https://minecraft.wiki/w/Pack.mcmeta | min/max_format rules, no supported_formats from 65 | stable
- https://minecraft.wiki/w/Font_definition | bitmap/space/reference/ttf fields, 256 limit (use this, not /w/Font) | stable
- https://minecraft.wiki/w/Items_model_definition | oversized_in_gui, empty/composite/select, cmd tint | stable
- https://minecraft.wiki/w/Model | gui scale<=4, translation +-80, elements -16..32 | stable
- https://minecraft.wiki/w/Resource_pack | .png.mcmeta animation, gui nine_slice | stable
- https://minecraft.wiki/w/Data_component_format/tooltip_style (+ /tooltip_display) | sprite paths, fields | stable
- https://minecraft.wiki/w/Java_Edition_1.21.11 offset=100000 | items atlas | stable
- https://minecraft.wiki/w/Java_Edition_26.3 offset=200000 | rp changes (shaders, trims, shade removed) | stable
- https://minecraft.wiki/w/Java_Edition_26.2 | text shaders renamed | stable
- https://docs.neoforged.net/primer/docs/1.21.6/ | GUI render strata, oversized items | stable
- https://raw.githubusercontent.com/xef5000/materione/main/docs/architecture/gui.md | best source: measured 26.1.2 draw order, ascent math, 256 limit (offset=100000 for tiles) | stable
- https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/ | vanilla jsons/mcmeta (tooltip, atlases/items.json, highlight sprites exist) | stable
- https://jd.papermc.io/paper/26.3/io/papermc/paper/datacomponent/DataComponentTypes.html | component constants | stable
- https://jd.papermc.io/paper/26.3/org/bukkit/inventory/InventoryView.html | setTitle deprecated | stable
- https://docs.papermc.io/adventure/resource-pack/ and https://jd.advntr.dev/api/latest/net/kyori/adventure/resource/ResourcePackRequest.Builder.html | request API | stable
- https://github.com/PaperMC/Paper/issues/12865 | config-phase pack status bug, closed by PR 12866 (2025-07) | stable
- https://pixeljoint.com/forum/forum_posts.asp?TID=11299 , https://www.derekyu.com/makegames/pixelart.html , https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes | pixel art rules | stable
- https://kenney.nl/support | CC0, no attribution | stable

- https://github.com/PluginBugs/Issues-ItemsAdder/issues/5607 , /5585 , /5603 , /5527 | 4.0.18 no 26.3; 5.0.0 betas on 26.3 | volatile
- https://voxel.shop/resource/itemsadder-custom-items-etc.1851/updates | latest stable 4.0.18 (2026-08-21) | volatile
- https://wiki.itemsadder.com/llms.txt | index of IA wiki URLs (itemsadder.devs.beer redirects here) | stable
- https://pillow.readthedocs.io/en/stable/reference/Image.html (resize at offset=100000), ImageDraw.html | defaults | stable
- https://www.aseprite.org/docs/cli/ | batch export + Lua | stable

Dead ends: wiki.itemsadder.com/plugin-usage/resourcepack-hosting and .../font-images-advanced (404);
minecraft.net 26.3 article (timeout); docs.neoforged.net/docs/gui/screens/ (404, use /docs/rendering/screens, no slot order there);
raw.githubusercontent.com/misode/technical-changes README (404); docs.nexomc.com/mechanics/gui-title-and-glyphs (404); minecraft.wiki/w/Font (no schema).
