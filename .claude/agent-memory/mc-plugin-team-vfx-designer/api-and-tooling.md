---
name: vfx-api-and-tooling
description: Verified Paper 26.2 particle data types and how to run previews and checks in the sandbox
metadata:
  type: reference
---

Stable for 26.2 (2026-11-26; https://jd.papermc.io/paper/26.2/org/bukkit/Particle.html and a probe of `getDataType()` on paper-api 26.2.build.135):
- `DUST` = `Particle.DustOptions`, `DUST_COLOR_TRANSITION` = `Particle.DustTransition`, `BLOCK`/`DUST_PILLAR` = `BlockData`, `ITEM` = `ItemStack`, `ENTITY_EFFECT`/`FLASH` = `Color`, `TRAIL` = `Particle.Trail`.
- `SWEEP_ATTACK`, `CRIT`, `POOF`, `DUST_PLUME` = `Void`.
- `Particle` and `LayerParser` work in a plain JUnit run; `Bukkit.createBlockData` does not (no server).
- `spawnParticle(..., offsetX, offsetY, offsetZ, extra, data)` compiles on both `World` and `Player`.

Sandbox (2026-11-26):
- Set `MISE_STATE_DIR`, `MISE_CACHE_DIR` under `$TMPDIR`; `MPLCONFIGDIR=$TMPDIR/mpl` for matplotlib.
- `mise run assets-deps` fails in the sandbox on a fresh worktree: reading `*.pem` is denied and pip loads certifi's CA bundle. It needed one unsandboxed run; afterwards validate-assets and vfx-previews work sandboxed.
- Surefire can't create `/tmp/surefire-*`, so test stdout is lost: use `MAVEN_OPTS=-Djava.io.tmpdir=$TMPDIR` plus `-DargLine=-Djava.io.tmpdir=$TMPDIR`.

Previews: `mise run vfx-previews` runs `design/vfx-scripts/plot_previews.py`, which feeds `ExportPoints.java` (real `Shapes`).
