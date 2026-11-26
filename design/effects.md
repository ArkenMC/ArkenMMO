# Effects

Presets: `src/main/resources/effects.yml`. Engine: `src/main/java/dev/casperrs/arkenMMO/vfx/`. Style: `vfx-style-guide.md`.
**Not yet seen in game.** Everything here is judged from shape previews only.

## Using the service

`Effects.play(String effectId, Location location, @Nullable Player viewer)`, main thread only.

- The location is the effect's origin; its **yaw** turns the shape, pitch is ignored. It is copied.
- `viewer == null`: shown to nearby players. Particles are not forced, so the client's particle setting applies and, by the server default, only players within about 32 blocks get them.
- A viewer: only that player sees it.
- Unknown IDs are logged once per load and skipped.
- No effect takes placeholders. There are no text or display-entity layers yet, so there is no placeholder overload and no display limits. Add both with the first effect that needs them.
- Wiring: `Effects.load(plugin)` in `onEnable`, `effects.shutdown()` in `onDisable`, `effects.reload()` on a config reload (there is no reload command yet).

## Layer format

The full field list is the comment block at the top of `effects.yml`; `LayerParser` is the loader. Keep the two and `vfx-scripts/plot_previews.py` (same defaults) in step.

| Key | Meaning | Default |
|---|---|---|
| `type` | `particle` | required |
| `particle` | `Particle` name, lower case | required |
| `shape` | `arc` or `line` | required |
| `points` | particles, 1-500 | 1 |
| `delay-ticks` / `duration-ticks` | start delay 0-100 / ticks the points are spread over 1-100 | 0 / 1 |
| `motion`, `lift`, `speed` | `none`, `outward`, `up`, `spin`; upward part -4 to 4; speed 0-4 | none, 0, 0 |
| `jitter` | random shift in blocks, 0-2 | 0 |
| arc: `radius`, `end-radius`, `y`, `end-y`, `start-angle`, `sweep` | blocks and degrees; 0 = forward, positive = right; 360 = ring | 1, radius, 0, y, 0, 360 |
| line: `from`, `to` | `[right, up, forward]` in blocks | required |
| `color`, `to-color`, `size` | `dust` and `dust_color_transition`; size 0.1-4 | size 1 |
| `block` | `block` / `dust_pillar`: a block, or `ground` (block under the origin, else coarse dirt) | required |

A bad layer (unknown particle, shape, motion, type or key, bad value, unsupported particle data) is logged and skipped. An effect missing from the server's file uses the bundled preset.

## Limits

| Key | Value | Over the limit |
|---|---|---|
| `max-particles-per-effect` | 200 | the preset is thinned evenly at load, with a warning |
| `max-active-effects` | 64 | a new animated effect shows all its particles at once |

Points are computed at load. One shared 1-tick task runs only while an animation is running. No entities are spawned.

## Effects

"Particles" is the total per play (client-side lifetime comes on top of the ticks).

| ID | Origin | Looks like | When | Particles, ticks |
|---|---|---|---|---|
| `skill_warrior_cleave` | caster's feet, caster's yaw | one diagonal crimson slash, right to left, high to low (1.4 to 0.8): bright edge at 3.5 m over 120 degrees, dark trail inside, 3 sweeps, forward sparks | cast | 69, 4 |
| `skill_warrior_leaping_strike` | take-off feet | tight 0.8 m ring, white puff, ground chips, two crimson streaks twisting up to 1.9 m | take-off | 56, 4 |
| `skill_warrior_leaping_strike_impact` | landing feet | flat shockwave in three rings (1.2, 2.1, 3.0 m) ending bright at the damage radius, ground-block debris, dust plumes | landing | 154, 3 |
| `skill_warrior_whirlwind` | caster's feet, once per pulse | two crimson blades half a turn apart sweeping a 4 m circle at waist height, 4 sweeps inside, rising wind spiral | each of 3 pulses | 76 per pulse, 6 |
| `skill_warrior_execute` | target's feet, caster's yaw | one steep two-tone cut across the target's near side, 1 sweep, small spark pop | hit, target at 30% or more | 47, 3 |
| `skill_warrior_execute_low` | target's feet, caster's yaw | larger X, orange fading to dark crimson, second stroke 3 ticks later, then red shards, sparks and a 1.3 m ground ring | hit below 30%; replaces the normal one | 128, 5 |

The effects don't follow anything: each stays where it was played.

## Check in game
- Reach: cleave against 3.5 m and 120 degrees (also mirrored correctly while turning), impact 3 m, whirlwind 4 m.
- First person: cleave and whirlwind must not block the view; `sweep_attack` is large and white and may need fewer points.
- Dust lingers for a random time on the client: check that three whirlwind pulses don't merge into a solid ring.
- Execute on small mobs (the cut reaches 2.3-2.8 m high) and on wide ones (the cut sits 0.55-0.65 m from the centre and can be hidden inside the model).
- Leaping strike impact on slabs, snow layers, water and in mid-air (debris falls back to coarse dirt).
- Leap, `poof` and `crit` motion: speed and spread can't be previewed.
- With "Particles: Decreased/Minimal", and as a second player watching.
