"""warrior.leaping_strike: launch whoosh, and the ground slam with settling grit."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sound-tools"))
from synth import (band, envelope, hit_envelope, knock, master, mix, moving_band, noise, room, samples,  # noqa: E402
                   sweep_sine, write)

SEED = 3100
LAUNCH_SECONDS = 0.5
IMPACT_SECONDS = 0.8
VARIANT_PITCH = (1.0, 0.94)
LAUNCH_HZ = ((0.0, 260), (0.30, 1900), (0.5, 2600))
THUD_HZ = (170, 52)
KNOCK_HZ = 420
GRIT_COUNT = 70
TARGET_LUFS = -16.0

for variant, scale in enumerate(VARIANT_PITCH, 1):
    rng = np.random.default_rng(SEED + variant)
    air = moving_band(noise(LAUNCH_SECONDS, rng), [(t, f * scale) for t, f in LAUNCH_HZ], q=1.7) * envelope(
        LAUNCH_SECONDS, [(0, 0), (0.04, 0.35), (0.22, 1), (0.34, 0.55), (LAUNCH_SECONDS, 0)])
    push = sweep_sine(LAUNCH_SECONDS, 190 * scale, 70 * scale, 0.05) * hit_envelope(LAUNCH_SECONDS, 0.003, 0.055)
    kick = band(noise(LAUNCH_SECONDS, rng), 300, 1800) * hit_envelope(LAUNCH_SECONDS, 0.002, 0.025)
    write(f"skill/warrior/leaping_strike_{variant}",
          master(mix(LAUNCH_SECONDS, (air, 1.0), (push, 0.6), (kick, 0.35)), TARGET_LUFS))

    rng = np.random.default_rng(SEED + 100 + variant)
    thud = sweep_sine(IMPACT_SECONDS, THUD_HZ[0] * scale, THUD_HZ[1] * scale, 0.045) * hit_envelope(
        IMPACT_SECONDS, 0.003, 0.15)
    crack = band(noise(IMPACT_SECONDS, rng), 500, 3800) * hit_envelope(IMPACT_SECONDS, 0.001, 0.028)
    earth = band(noise(IMPACT_SECONDS, rng), 90, 520) * hit_envelope(IMPACT_SECONDS, 0.004, 0.13)
    grit = np.zeros(samples(IMPACT_SECONDS))
    for _ in range(GRIT_COUNT):
        at = 0.03 + rng.exponential(0.13)
        if at < IMPACT_SECONDS - 0.08:
            grain = noise(0.012, rng) * hit_envelope(0.012, 0.0005, 0.0025)
            start = samples(at)
            grit[start:start + len(grain)] += grain * rng.uniform(0.3, 1.0) * np.exp(-at / 0.22)
    grit = band(grit, 900, 5200)
    dust = band(noise(IMPACT_SECONDS, rng), 600, 2400) * envelope(
        IMPACT_SECONDS, [(0, 0), (0.05, 1), (0.25, 0.35), (IMPACT_SECONDS, 0)])
    body = knock(IMPACT_SECONDS, KNOCK_HZ * scale, 0.07)
    signal = mix(IMPACT_SECONDS, (thud, 0.8), (body, 0.6), (crack, 0.65), (earth, 0.85), (grit, 0.3), (dust, 0.16))
    write(f"skill/warrior/leaping_strike_impact_{variant}", master(room(signal, rng, 0.12, 0.07), TARGET_LUFS))
