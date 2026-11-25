"""Frozen GUI palette. Each ramp runs dark to light; art may use only these colours."""

RAMPS = {
    # class identities
    "crimson": "#2b0f1e #561826 #8a2430 #bd3a32 #e06a3c #f4a65a",
    "forest": "#0f2228 #173a33 #24573a #3f7a3c #6fa043 #b4c95a",
    "violet": "#170f33 #281a5c #3d2c8f #5a49c4 #7b7ce8 #a9b8fa",
    "arcane": "#12374f #1f6f9e #35b5c9 #8ff0e4 #e4fffa",
    "ivory": "#4a465e #6e6a7e #aaa5a8 #ddd6c4 #f7f1dc",
    "navy": "#101433 #1b2658 #2b3f82 #425fae #6a8ad0",
    # shared materials
    "skin": "#4a2430 #7d3f3a #b06a4e #d9976b #f2c498",
    "steel": "#12101c #232436 #3b4058 #5c6580 #8a94a8 #bcc4cf #eef0ec",
    "leather": "#26141a #45251f #6b3d27 #94603a #bd8a55",
    "gold": "#3d2415 #6e4318 #a8721f #dca636 #f6d86b #fff3b8",
    "parchment": "#8c6a4a #b99768 #dcc291 #efdcb0",
    # backdrops: darker and less saturated than any figure
    "ember_sky": "#141019 #1d1828 #292138 #3d2840 #572e3e #763a3a",
    "ember_stone": "#18131d #251d29 #342833 #47363e #5d474a",
    "dusk_forest": "#0e1517 #131f20 #1a2a29 #233733 #2f473d",
    "dusk_sky": "#0f1220 #171d32 #212b45 #323c55 #4c4a56 #6d5a4c",
    "night_teal": "#0a0f18 #0f1a26 #142735 #1a3643 #214752 #2d5e66",
    "dawn_sky": "#10122a #191b3a #26254a #3a2f55 #55395a #77485a",
    "dawn_stone": "#171726 #232338 #33334a #46455a #5e5a68",
    # GUI chrome
    "iron": "#0d0b14 #1a1925 #282a39 #3a3e50 #525869 #747b8a",
}


def _rgb(code):
    return tuple(int(code[i:i + 2], 16) for i in (1, 3, 5))


PALETTE = {name: [_rgb(c) for c in ramp.split()] for name, ramp in RAMPS.items()}


def col(ramp, step, alpha=255):
    colours = PALETTE[ramp]
    return colours[max(0, min(step, len(colours) - 1))] + (alpha,)
