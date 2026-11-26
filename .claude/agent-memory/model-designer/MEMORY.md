# model-designer memory

Verified facts only, one dated line each with its source. Rules: `AGENTS.md`.

- Earlier facts: `../mc-plugin-team-model-designer/MEMORY.md`
- (2026-11-26) `mise` was not on PATH in the Bash tool. A venv outside the repo with pillow 13.0.0, numpy, pyyaml and scipy runs `design/scripts/*.py`, `tools/validate_assets.py` and `tools/pack.py` directly. Numpy 2.5.5 instead of the pinned 2.5.4 re-encodes the existing GUI PNGs and pack.png differently (bytes change); restore them with `git checkout`. Source: local run.
- (2026-11-26) Emerald item: generator `design/scripts/items_emerald.py`, spec `design/item-emerald.md`, ramp `emerald` added to `palette.py`; IDs `arkenmmo:emerald` for item_model and tooltip_style.
