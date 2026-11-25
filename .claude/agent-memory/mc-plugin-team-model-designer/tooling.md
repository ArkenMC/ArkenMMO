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
- GUI art: `design/scripts/pixelkit/` (layout, palette, hullrig renderer, chrome, backdrops, warrior, pack, preview); rules in `design/gui-style-guide.md`; previews in `target/previews/gui/`.
