"""Shared synthesis and export helpers for the scripts in design/sound-scripts/."""
import io
from pathlib import Path

import numpy as np
import pyloudnorm
import soundfile as sf
from scipy.signal import butter, sosfilt

RATE = 48000
ROOT = Path(__file__).resolve().parents[2]
SOUNDS = ROOT / "resourcepack/assets/arkenmmo/sounds"
PEAK_DBFS = -2.0
DECODED_PEAK_MAX_DBFS = -1.3


def samples(seconds):
    return int(round(seconds * RATE))


def timeline(seconds):
    return np.arange(samples(seconds)) / RATE


def envelope(seconds, points):
    """Piecewise-linear gain from (seconds, level) points."""
    times, levels = zip(*points)
    return np.interp(timeline(seconds), times, levels)


def hit_envelope(seconds, attack, decay):
    """Linear attack, then exponential decay with time constant `decay` (seconds)."""
    t = timeline(seconds)
    return np.minimum(t / attack, 1.0) * np.exp(-np.maximum(t - attack, 0) / decay)


def sweep_sine(seconds, start_hz, end_hz, glide):
    """Sine whose pitch moves from start to end with time constant `glide` (seconds)."""
    hz = end_hz + (start_hz - end_hz) * np.exp(-timeline(seconds) / glide)
    return np.sin(2 * np.pi * np.cumsum(hz) / RATE)


def noise(seconds, rng):
    return rng.uniform(-1, 1, samples(seconds))


def band(signal, low=None, high=None, order=2):
    if low and high:
        sos = butter(order, [low, high], "bandpass", fs=RATE, output="sos")
    elif low:
        sos = butter(order, low, "highpass", fs=RATE, output="sos")
    else:
        sos = butter(order, high, "lowpass", fs=RATE, output="sos")
    return sosfilt(sos, signal)


def moving_band(signal, centre_points, q):
    """State-variable bandpass whose centre follows (seconds, Hz) points."""
    times, freqs = zip(*centre_points)
    centre = np.exp(np.interp(np.arange(len(signal)) / RATE, times, np.log(freqs)))
    g = np.tan(np.pi * centre / RATE)
    k = 1.0 / q
    out = np.empty_like(signal)
    ic1 = ic2 = 0.0
    for i, x in enumerate(signal):
        a1 = 1.0 / (1.0 + g[i] * (g[i] + k))
        v1 = a1 * (ic1 + g[i] * (x - ic2))
        v2 = ic2 + g[i] * v1
        ic1, ic2 = 2 * v1 - ic1, 2 * v2 - ic2
        out[i] = v1 * k
    return out


def steel_ring(seconds, base_hz, decay, rng):
    """The family's blade colour: inharmonic partials, higher ones dying sooner."""
    t = timeline(seconds)
    out = np.zeros_like(t)
    for ratio, level in ((1.0, 1.0), (1.47, 0.6), (2.09, 0.4), (2.56, 0.25)):
        phase = rng.uniform(0, 2 * np.pi)
        out += level * np.sin(2 * np.pi * base_hz * ratio * t + phase) * np.exp(-t * ratio / decay)
    return out * np.minimum(t / 0.003, 1.0) / 2.25


def knock(seconds, start_hz, decay):
    """Saturated mid-range body that keeps a low thud audible on small speakers."""
    tone = sweep_sine(seconds, start_hz, start_hz * 0.45, 0.03) * hit_envelope(seconds, 0.002, decay)
    return np.tanh(2.5 * tone)


def mix(seconds, *layers):
    """Each layer is (signal, gain) or (signal, gain, offset seconds); signals are peak-normalised first."""
    out = np.zeros(samples(seconds))
    for signal, gain, *offset in layers:
        start = samples(offset[0]) if offset else 0
        part = signal[:len(out) - start]
        out[start:start + len(part)] += gain * part / max(np.max(np.abs(signal)), 1e-9)
    return out


def room(signal, rng, wet, decay):
    """Very short diffuse tail, darkened so it never sounds metallic."""
    length = samples(decay * 3)
    impulse = band(rng.standard_normal(length), high=4000) * np.exp(-np.arange(length) / RATE / decay)
    impulse[:samples(0.008)] = 0
    tail = np.convolve(signal, impulse)[:len(signal)]
    return signal + wet * tail * np.max(np.abs(signal)) / max(np.max(np.abs(tail)), 1e-9)


def _level(signal):
    if len(signal) >= samples(0.4):
        return pyloudnorm.Meter(RATE).integrated_loudness(signal)
    audible = np.flatnonzero(np.abs(signal) > 0.01)
    active = signal[audible[0]:audible[-1] + 1]
    return 20 * np.log10(np.sqrt(np.mean(active ** 2)))


def master(signal, target):
    """Rumble cut, edge fades, then gain to `target` (LUFS, or dBFS RMS under 400 ms) under the peak ceiling."""
    signal = band(signal, low=35)
    fade_in, fade_out = samples(0.001), samples(0.012)
    signal[:fade_in] *= np.linspace(0, 1, fade_in)
    signal[-fade_out:] *= np.linspace(1, 0, fade_out) ** 2
    signal = signal / np.max(np.abs(signal))
    ceiling = 10 ** (PEAK_DBFS / 20)
    out = signal * ceiling
    # Soft saturation raises the loudness of peaky material without passing the ceiling.
    for drive in np.linspace(0.1, 12, 120):
        if _level(out) >= target:
            break
        out = ceiling * np.tanh(drive * signal) / np.tanh(drive)
    return out * 10 ** (-max(_level(out) - target, 0) / 20)


def _stable_ogg(data):
    """libsndfile picks a random Ogg stream serial; fix it (and the page CRCs) so reruns are byte-identical."""
    table = []
    for n in range(256):
        value = n << 24
        for _ in range(8):
            value = (value << 1) ^ (0x04C11DB7 if value & 0x80000000 else 0)
        table.append(value & 0xFFFFFFFF)
    data = bytearray(data)
    pos = 0
    while pos < len(data):
        assert data[pos:pos + 4] == b"OggS"
        segments = data[pos + 26]
        size = 27 + segments + sum(data[pos + 27:pos + 27 + segments])
        data[pos + 14:pos + 18] = (1).to_bytes(4, "little")
        data[pos + 22:pos + 26] = bytes(4)
        crc = 0
        for byte in data[pos:pos + size]:
            crc = ((crc << 8) & 0xFFFFFFFF) ^ table[(crc >> 24) ^ byte]
        data[pos + 22:pos + 26] = crc.to_bytes(4, "little")
        pos += size
    return bytes(data)


def write(name, signal):
    """Encode mono Vorbis to sounds/<name>.ogg, lowering the gain if encoding overshoots the peak limit."""
    path = SOUNDS / f"{name}.ogg"
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        buffer = io.BytesIO()
        sf.write(buffer, signal.astype(np.float32), RATE, format="OGG", subtype="VORBIS")
        buffer.seek(0)
        decoded, _ = sf.read(buffer)
        if np.max(np.abs(decoded)) <= 10 ** (DECODED_PEAK_MAX_DBFS / 20):
            break
        signal = signal * 10 ** (-0.3 / 20)
    path.write_bytes(_stable_ogg(buffer.getvalue()))
    print(f"  {path.relative_to(ROOT)}")
