"""warrior.cleave: one quick, sharp blade swoosh."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sound-tools"))
from synth import band, envelope, master, mix, moving_band, noise, steel_ring, write  # noqa: E402

SEED = 2100
SECONDS = 0.34
VARIANT_PITCH = (1.0, 1.05, 0.95)
SWOOSH_HZ = ((0.0, 900), (0.075, 4200), (0.30, 1100))
RING_HZ = 2150
TARGET_RMS = -18.0

for variant, scale in enumerate(VARIANT_PITCH, 1):
    rng = np.random.default_rng(SEED + variant)
    air = moving_band(noise(SECONDS, rng), [(t, f * scale) for t, f in SWOOSH_HZ], q=2.2) * envelope(
        SECONDS, [(0, 0), (0.012, 0.45), (0.07, 1), (0.14, 0.4), (0.24, 0.09), (SECONDS, 0)])
    weight = band(noise(SECONDS, rng), 180, 700) * envelope(
        SECONDS, [(0, 0), (0.02, 0.5), (0.08, 1), (0.2, 0.08), (SECONDS, 0)])
    ring = steel_ring(SECONDS, RING_HZ * scale, 0.09, rng)
    signal = mix(SECONDS, (air, 1.0), (weight, 0.45), (ring, 0.2, 0.055))
    write(f"skill/warrior/cleave_{variant}", master(signal, TARGET_RMS))
