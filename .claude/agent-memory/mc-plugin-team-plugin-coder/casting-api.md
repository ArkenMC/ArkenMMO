---
name: casting-api
description: Paper 26.2 API checked for skill casting, and what only a game client can verify
metadata:
  type: reference
---

2026-11-26, paper-api 26.2.build.135-stable (stable). Source: `mvn clean compile -Dmaven.compiler.showDeprecation=true`, no warnings.

- Not deprecated and compile: `Player#getResourcePackStatus`, `Player#playSound(Location, String, SoundCategory, float, float)`, `World#rayTrace(..., Predicate)`, `World#hasCollisionsIn(BoundingBox)`, `World#getNearbyLivingEntities(Location, double, Predicate)`, `LivingEntity#isClimbing`, `setNoDamageTicks`, `damage(double, Entity)`, `org.bukkit.entity.Mannequin`.
- `Player#isOnGround` is deprecated (client-reported).
- Unverified without a client: leap distance (drag formula in `LeapingStrike`), fall protection timing, whether one tick of delay catches the drop swing.
- 2026-11-26: sounds play `key`; `fallback` only for a blank or invalid key (user-facing rule in `design/sounds.md`), not by pack status.
- 2026-11-26 (volatile, sandbox): `mise run validate-assets` and `sound-check` fail in `assets-deps` (pip can't load its CA bundle). `python3 tools/validate_assets.py` and `python3 tools/sound_check.py` work when `python3` on PATH is the main checkout's `.venv`.
- The existing server's saved `messages.yml` keeps old text for keys it already has; bundled defaults only fill missing keys.
- 2026-11-26: the isolation guard refuses long multi-file heredoc commands; use the Write tool, and short Python edit scripts in `$TMPDIR` run with `python3 -I`.
