"""Caster-only interface sounds: combo clicks and the failed-cast buzz."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sound-tools"))
from synth import band, envelope, hit_envelope, master, mix, noise, sweep_sine, timeline, write  # noqa: E402

SEED = 1100
CLICK_SECONDS = 0.06
CLICK_HZ = {"left": 760, "right": 1140}  # a fifth apart, so L and R are told apart by ear
CLICK_VARIANT_PITCH = (1.0, 1.025, 0.976)
CLICK_TARGET_RMS = -19.0
FAIL_SECONDS = 0.24
FAIL_NOTES = ((0.0, 0.085, 233), (0.095, 0.145, 175))  # start, length, Hz
FAIL_TARGET_RMS = -19.0

for index, (side, hz) in enumerate(CLICK_HZ.items()):
    for variant, scale in enumerate(CLICK_VARIANT_PITCH, 1):
        rng = np.random.default_rng(SEED + 10 * index + variant)
        body = sweep_sine(CLICK_SECONDS, hz * scale * 1.5, hz * scale, 0.004) * hit_envelope(CLICK_SECONDS, 0.001, 0.012)
        tick = band(noise(CLICK_SECONDS, rng), 2500, 7000) * hit_envelope(CLICK_SECONDS, 0.001, 0.002)
        write(f"ui/combo_click_{side}_{variant}",
              master(mix(CLICK_SECONDS, (body, 1.0), (tick, 0.18)), CLICK_TARGET_RMS))

notes = []
for start, length, hz in FAIL_NOTES:
    tone = sum(np.sin(2 * np.pi * hz * n * timeline(length)) / n for n in (1, 3, 5, 7))
    gate = envelope(length, [(0, 0), (0.004, 1), (length * 0.55, 0.7), (length, 0)])
    notes.append((band(tone, high=1400) * gate, 1.0, start))
write("ui/cast_fail", master(mix(FAIL_SECONDS, *notes), FAIL_TARGET_RMS))
