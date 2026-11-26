"""warrior.execute: steel strike with a deep thud; the low-health version is deeper, longer and darker."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sound-tools"))
from synth import (band, envelope, hit_envelope, knock, master, mix, moving_band, noise, room, steel_ring,  # noqa: E402
                   sweep_sine, timeline, write)

SEED = 5100
VARIANT_PITCH = (1.0, 0.95)
SECONDS = 0.55
LOW_SECONDS = 1.0
LOW_PITCH = 0.9
HIT_AT = 0.028  # the thud lands just after the swish starts
SWISH_HZ = ((0.0, 5200), (0.09, 900))
THUD_HZ = (150, 55)
LOW_THUD_HZ = (125, 41)
RING_HZ = 1180
KNOCK_HZ = 460
TOLL_HZ = (110, 155.6, 220, 311.1)  # tritone pairs: the finishing-blow colour
TARGET_LUFS = -16.0
LOW_TARGET_LUFS = -15.0


def strike(seconds, scale, rng, thud_hz, thud_decay, ring_decay):
    """Layers shared by both versions."""
    swish = moving_band(noise(seconds, rng), [(t, f * scale) for t, f in SWISH_HZ], q=2.0) * envelope(
        seconds, [(0, 0), (0.006, 1), (0.05, 0.6), (0.13, 0), (seconds, 0)])
    thud = sweep_sine(seconds, thud_hz[0] * scale, thud_hz[1] * scale, 0.04) * hit_envelope(seconds, 0.003, thud_decay)
    chop = band(noise(seconds, rng), 220, 1600) * hit_envelope(seconds, 0.002, 0.035)
    ring = steel_ring(seconds, RING_HZ * scale, ring_decay, rng)
    body = knock(seconds, KNOCK_HZ * scale, thud_decay * 0.55)
    return [(swish, 0.75), (thud, 0.75, HIT_AT), (body, 0.6, HIT_AT), (chop, 0.85, HIT_AT), (ring, 0.32, HIT_AT)]


for variant, scale in enumerate(VARIANT_PITCH, 1):
    rng = np.random.default_rng(SEED + variant)
    signal = mix(SECONDS, *strike(SECONDS, scale, rng, THUD_HZ, 0.095, 0.12))
    write(f"skill/warrior/execute_{variant}", master(room(signal, rng, 0.09, 0.06), TARGET_LUFS))

    rng = np.random.default_rng(SEED + 100 + variant)
    layers = strike(LOW_SECONDS, scale * LOW_PITCH, rng, LOW_THUD_HZ, 0.22, 0.2)
    crack = band(noise(LOW_SECONDS, rng), 1400, 6000) * hit_envelope(LOW_SECONDS, 0.001, 0.018)
    second = sweep_sine(LOW_SECONDS, 95 * scale, 38 * scale, 0.07) * hit_envelope(LOW_SECONDS, 0.004, 0.2)
    toll = sum(np.sin(2 * np.pi * hz * scale * timeline(LOW_SECONDS)) for hz in TOLL_HZ)
    toll *= hit_envelope(LOW_SECONDS, 0.012, 0.25)
    signal = mix(LOW_SECONDS, *layers, (crack, 0.5, HIT_AT), (second, 0.5, 0.12), (toll, 0.45, HIT_AT))
    write(f"skill/warrior/execute_low_{variant}", master(room(signal, rng, 0.17, 0.12), LOW_TARGET_LUFS))
