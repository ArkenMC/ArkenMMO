"""Frozen GUI palette. Each ramp runs dark to light; art may use only these colours."""

RAMPS = {
    # class identities
    "crimson": "#2b0f1e #561826 #8a2430 #bd3a32 #e06a3c #f4a65a",
    # shared materials
    "steel": "#12101c #232436 #3b4058 #5c6580 #8a94a8 #bcc4cf #eef0ec",
    "leather": "#26141a #45251f #6b3d27 #94603a #bd8a55",
    "gold": "#3d2415 #6e4318 #a8721f #dca636 #f6d86b #fff3b8",
    "parchment": "#8c6a4a #b99768 #dcc291 #efdcb0",
    # backdrops: darker and less saturated than any figure
    "ember_sky": "#141019 #1d1828 #292138 #3d2840 #572e3e #763a3a",
    "ember_stone": "#18131d #251d29 #342833 #47363e #5d474a",
    "dusk_forest": "#0e1517 #131f20 #1a2a29 #233733 #2f473d",
    # GUI chrome
    "iron": "#0d0b14 #1a1925 #282a39 #3a3e50 #525869 #747b8a",
}


def _rgb(code):
    return tuple(int(code[i:i + 2], 16) for i in (1, 3, 5))


PALETTE = {name: [_rgb(c) for c in ramp.split()] for name, ramp in RAMPS.items()}


def col(ramp, step, alpha=255):
    colours = PALETTE[ramp]
    return colours[max(0, min(step, len(colours) - 1))] + (alpha,)
