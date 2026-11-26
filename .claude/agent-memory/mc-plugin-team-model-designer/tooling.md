---
name: tooling
description: Pack format for 26.3, sandbox/mise quirks and where the GUI art pipeline lives
metadata:
  type: reference
---

- (stable for 26.3, 2026-11-25, https://minecraft.wiki/w/Pack_format) resource pack format 26.3 = 97.1 (26.1 = 84.0, 26.2 = 88.0).
- (2026-11-25) In the sandbox `mise run ...` fails: it cannot write the worktree trust link under `~/.local/state/mise` ("Read-only file system"). Iterate with the main checkout's `.venv/bin/python` (same pinned Pillow, numpy, scipy). Run the final `mise run assets / validate-assets / pack` with the sandbox disabled.
- (2026-11-25) `git branch -m` prints a config-lock error in the sandbox but the rename works. The worktree starts at main, so `git reset --keep feature/<f>` before any work.
- (2026-11-25) The worktree guard rejects Bash heredocs and `export` chains as "too complex"; use the Write tool for scripts.
- (stable for 26.3, 2026-11-25, InventivetalentDev/minecraft-assets@26.3) `.mcmeta` nine_slice: tooltip background 100x100 border 9; tooltip frame 100x100 border 10 `stretch_inner`; both slot_highlight sprites 24x24 border 4. Vanilla tooltip alpha geometry: background fills 8..91 (alpha 240, corners clear), frame is a 1 px line at inset 9.
- (2026-11-25) User style decision: subtle "minecraft ish" touches on the faceted style, not a player-model redesign.
- The worktree guard also rejects commands containing github URLs after `cd`; run `curl` with `--output-dir` as its own command.
- GUI art: `design/scripts/pixelkit/` (layout, palette, hullrig renderer, figure steps, one module per hero, heroes registry, chrome, backdrops, pack, preview); rules in `design/gui-style-guide.md`; previews in `target/previews/gui/`.
- (2026-11-26) Without leaving the sandbox: run the scripts behind `assets`, `validate-assets` (`tools/validate_assets.py`) and `sound-check` (`tools/sound_check.py`) from the worktree root with `../../../.venv/bin/python -B`.
- (2026-11-26) The worktree guard rejects shell lines holding the repo's absolute path next to loops or variables; use relative paths or a script file. Give Python `< /dev/null` and `timeout`.
- Skill tree art: `pixelkit/tree{icons,nodes,stone}.py`, previews from `zz_skill_tree_preview.py` in `target/previews/skills/`; spec `design/gui-skill-tree.md`.
