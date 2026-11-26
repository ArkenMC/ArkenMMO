"""Every skill and tab sigil, one 24x24 mask each. All node states are generated from that mask.

Rules: one bold shape, strokes at least 3 px, no real runic letters, no rotating hooks.
"""
from . import icons_archer, icons_captain, icons_mage, icons_warrior, icons_warrior_a1

ICONS = {name: mask for module in (icons_warrior_a1, icons_warrior, icons_archer, icons_mage, icons_captain)
         for name, mask in module.ICONS.items()}
