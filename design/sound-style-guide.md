# Sound style guide

**Character: clean, punchy, dry.** Readable in a fight; nothing long, boomy or shrill. All sounds are synthesized; helpers are in `sound-tools/synth.py`.

## Layers
- **Interface** (caster only): soft pitched tocks and muted buzzes, mostly under 2 kHz. Left click 760 Hz, right click 1140 Hz (a fifth apart). Failure: two falling notes, 233 to 175 Hz.
- **Blade:** band-passed noise with a moving centre (`moving_band`) plus a quiet `steel_ring` (inharmonic 1 : 1.47 : 2.09 : 2.56). The ring ties the Warrior skills together.
- **Weight:** a falling sine thud, always with a mid-range layer (`knock`, chop or earth noise) so small speakers still play the hit.
- **Danger / finisher:** a quiet low tritone toll and a longer tail.
- **Space:** only impacts get `room`, short and dark. Swooshes stay dry.

## Rules
- Mono, 48 kHz. Edge fades 1 ms in, 12 ms out; no leading silence.
- 400 ms or longer: -16 LUFS. Repeating pulses -17, the biggest finisher -15 to -16. Shorter: -18 dBFS RMS; clicks and failure -19.
- Peak ceiling -2 dBFS before encoding, at most -1.3 dBFS decoded.
- Keep energy below 150 Hz at about half or less on heavy hits.
- Interface volumes in `sounds.yml` are low (clicks 0.35).
- A repeated pulse must have faded by the next one, and gets a narrow pitch range.
- 2-3 variants for repeated sounds; fixed seeds.
