---
name: audio-tooling
description: How to run the sound tasks in the sandbox and verify vanilla sound keys
metadata:
  type: reference
---
All checked 2026-11-26.
- Stable: `MISE_STATE_DIR=$TMPDIR/mise-state MISE_CACHE_DIR=$TMPDIR/mise-cache mise run <task>` works; first venv install needs pypi.org and files.pythonhosted.org. A "failed to rebuild user shims" error from `mise install` is harmless.
- Stable: `design/sound-tools/synth.py` has the helpers; `write()` makes mono Vorbis reproducible (libsndfile's random Ogg serial is rewritten).
- Stable (26.2): vanilla keys: download paper-api jar from repo.papermc.io into $TMPDIR, `javap -c -cp jar org.bukkit.Sound`, grep `// String <key>$`. SoundCategory has UI. `World.playSound(Location,String,SoundCategory,float,float)` and `Player.playSound(Entity,String,SoundCategory,float,float)` exist.
- The worktree guard refuses long compound Bash commands and heredocs; use Write for files and short commands.
