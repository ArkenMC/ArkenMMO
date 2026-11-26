# VFX style guide

The user wants **few, clean effects**: crisp and readable, not noisy. Vanilla particles, no retextures.

## Warrior colours
Taken from the `crimson` ramp in `design/gui-style-guide.md`, brightened because the client darkens dust at random.

| Use | Colour |
|---|---|
| leading edge, the line that shows reach | `#e8433a` |
| secondary ring | `#bd3a32` |
| trail and depth | `#8a2430` |
| finisher only: hot start fading to dark | `#ff5a3c` to `#561826` |

## Rules
- The brightest line sits exactly at the damage reach. Nothing coloured goes past it.
- One main shape per skill: arc (cleave), column (take-off), shockwave (impact), double blade (whirlwind), single cut (execute), cross (execute below 30%).
- Crimson carries the shape; neutral particles (`sweep_attack`, `crit`, `poof`, ground `block`) only add weight, in small numbers.
- Timing: hits take 2-4 ticks, a channel pulse at most 6, well under its 10-tick interval.
- Density: small cue 45-80 particles, big moment 125-160, hard cap 200. Edge points about 0.1-0.4 blocks apart.
- A stronger variant changes the shape (one cut becomes a cross), not only the amount.
- Keep particles out of the caster's eye line (1.62) where possible: reach lines at 0.15 for ground effects, 0.8-1.4 for blades.
- No `flash`, explosions or smoke clouds: they hide the fight.
