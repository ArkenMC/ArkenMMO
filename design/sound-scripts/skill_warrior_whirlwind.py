"""warrior.whirlwind: one pulse (two blade passes, rising wind, steel ring); the game plays three."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sound-tools"))
from synth import envelope, master, mix, moving_band, noise, steel_ring, write  # noqa: E402

SEED = 4100
SECONDS = 0.52  # the tail is nearly gone by 0.45 s, so pulses 0.5 s apart do not pile up
VARIANT_PITCH = (1.0, 1.04, 0.96)
WIND_HZ = ((0.0, 380), (SECONDS, 1500))
BLADE_PASSES = ((0.0, 1.0), (0.16, 0.65))  # offset seconds, gain
BLADE_HZ = ((0.0, 1200), (0.07, 3600), (0.18, 1500))
RING_HZ = 1620
TARGET_LUFS = -17.0  # a little under the single hits because it repeats

for variant, scale in enumerate(VARIANT_PITCH, 1):
    rng = np.random.default_rng(SEED + variant)
    wind = moving_band(noise(SECONDS, rng), [(t, f * scale) for t, f in WIND_HZ], q=2.8) * envelope(
        SECONDS, [(0, 0), (0.02, 0.35), (0.22, 1), (0.36, 0.4), (0.45, 0.07), (SECONDS, 0)])
    blades = []
    for offset, gain in BLADE_PASSES:
        blade = moving_band(noise(0.2, rng), [(t, f * scale) for t, f in BLADE_HZ], q=3.0) * envelope(
            0.2, [(0, 0), (0.012, 0.5), (0.055, 1), (0.12, 0.2), (0.2, 0)])
        blades.append((blade, 0.8 * gain, offset))
    ring = steel_ring(SECONDS, RING_HZ * scale, 0.11, rng) * envelope(SECONDS, [(0, 1), (0.34, 1), (0.48, 0)])
    signal = mix(SECONDS, (wind, 0.8), *blades, (ring, 0.17, 0.045))
    write(f"skill/warrior/whirlwind_{variant}", master(signal, TARGET_LUFS))
