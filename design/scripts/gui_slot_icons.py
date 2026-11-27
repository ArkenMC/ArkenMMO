"""Accessory placeholder silhouettes for the survival inventory, and the clear shield sprite.

The four empty-armour ghosts are Minecraft's own (we ship no helmet/chestplate/leggings/boots sprites). The accessory
slots (ring, ring, amulet, bracelet) are ordinary storage slots, so a resource pack cannot give them a ghost icon:
`accessory_icons()` gives silhouettes that gui_inventory.py paints into inventory.png under the four panel-row cells.
They copy the vanilla ghosts' visual language only: one flat tone, no outline, no shading, drawn on the 16x16 GUI
pixel grid (doubled to 32x32), faint on the panel fill. The shapes are our own.
The items are 32x32 textures (one texel = one art px), so each placeholder is the item's own pixels at 1 art px,
on the item area's own grid, and not in whole 2x2 GUI-pixel blocks.

Writes resourcepack/assets/minecraft/textures/gui/sprites/container/slot/shield.png, fully clear, so the game's grey
shield ghost does not show on the plain shell where the offhand slot used to be. Spec: design/gui-inventory.md.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

import items_accessories
from pixelkit import layout
from pixelkit.palette import PALETTE, col

SPRITES = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "container" / "slot"
GRID = 16
SIZE = (32, 32)
TONE = col("iron", 1)  # the one flat tone: darker than the panel fill (iron 3), like vanilla's dark grey on light grey
PANEL = col("iron", 3)

# Each placeholder lies under the opaque pixels of the item(s) that belong in its cell, so the item hides it completely.
# The game draws an item's 32x32 texture over the cell's 16x16 GUI px item area, 1 texel = 1 art px, so the placeholder
# is built from the item textures themselves: the texels they all cover, less the 1 texel next to the outside and (except for the
# bracelet, whose thin cuff would break up) next to any opening; the amulet's gem is cut out. The ring placeholder is shared by both ring items.
COVERS = {"ring": ("ring_1", "ring_2"), "amulet": ("amulet",), "bracelet": ("bracelet",)}


def item_masks():
    """Opaque texels (32x32 booleans) of every accessory item, from the generator's own drawing."""
    return {name: draw()[..., 3] > 0 for name, draw in items_accessories.DRAW.items()}


def _inset(mask, along_holes=True):
    """The mask less every texel next to the outside (the background connected to the border), keeping hole edges."""
    labels, count = ndimage.label(~mask)
    outside = np.zeros_like(mask)
    for number in range(1, count + 1):
        part = labels == number
        if part[0].any() or part[-1].any() or part[:, 0].any() or part[:, -1].any():
            outside |= part
    kept = mask.copy()
    for shifted, _, _ in items_accessories.neighbours(outside):
        kept &= ~shifted
    # and, where the item has an opening, the texels along it, so the opening is as wide as the item's own
    if along_holes:
        for shifted, _, _ in items_accessories.neighbours(~mask & ~outside):
            kept &= ~shifted
    return kept


def placeholder_texels():
    masks = item_masks()
    texels = {name: _inset(np.logical_and.reduce([masks[item] for item in items]), name != "bracelet")
              for name, items in COVERS.items()}
    texels["amulet"] &= ~items_accessories.amulet_gem()  # the gem socket stays open
    return texels


ITEM_AT = 0  # art px: the 32x32 item texture covers the 32x32 item area exactly, one texel per art px


def on_item_area(mask):
    """A 32x32 texel mask as it lies in the 32x32 art-px item area (the same grid)."""
    out = np.zeros(SIZE[::-1], bool)
    out[ITEM_AT:ITEM_AT + 32, ITEM_AT:ITEM_AT + 32] = mask
    return out


def _icon(texels):
    # the items are 32x32 textures: one texel is one art px (half a GUI px), no 2x2 blocks
    mask = on_item_area(texels)
    image = np.zeros(SIZE[::-1] + (4,), np.uint8)
    image[mask] = TONE
    return Image.fromarray(image, "RGBA")


def accessory_icons():
    return {name: _icon(texels) for name, texels in placeholder_texels().items()}


def clear():
    return Image.new("RGBA", SIZE, (0, 0, 0, 0))


def check(sprites, hidden):
    known = {c for ramp in PALETTE.values() for c in ramp}
    errors = []
    shapes = set()
    for name, image in sprites.items():
        px = np.asarray(image)
        if image.size != SIZE:
            errors.append(f"{name} is {image.size}, not {SIZE}")
        if not set(px[..., 3].flatten().tolist()) <= {0, 255}:
            errors.append(f"{name} alpha is not binary")
        colours = {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]}
        if colours != {tuple(TONE[:3])} or not colours <= known:
            errors.append(f"{name} must be one flat palette tone ({tuple(TONE[:3])}), found {sorted(colours)}")
        if tuple(PANEL[:3]) in colours:
            errors.append(f"{name} uses the panel colour, so it would vanish")
        ys, xs = np.nonzero(px[..., 3])
        if not len(xs) or xs.min() < 2 or ys.min() < 2 or xs.max() > 29 or ys.max() > 29 or not 40 < len(xs) < 500:
            errors.append(f"{name} must lie inside 2 px margins (40..500 opaque px)")
        # one art px steps are intended: the items have texels of one art px
        shapes.add(px[..., 3].tobytes())
    masks = item_masks()
    for name, texels in placeholder_texels().items():
        for item in COVERS[name]:
            if (texels & ~masks[item]).any():
                errors.append(f"{name} placeholder shows beside the {item} item: some texels are not under its opaque pixels")
    if len(shapes) != len(sprites):
        errors.append("two icons share a silhouette")
    for name, image in hidden.items():
        if image.size != SIZE or np.asarray(image)[..., 3].any():
            errors.append(f"{name} must be {SIZE} and fully transparent")
    if errors:
        raise ValueError("slot icons: " + "; ".join(errors))
    print(f"slot icons: {len(sprites)} flat accessory silhouettes and {len(hidden)} clear sprite, 32x32, palette, binary alpha")


def main():
    sprites, hidden = accessory_icons(), {"shield": clear()}
    check(sprites, hidden)
    SPRITES.mkdir(parents=True, exist_ok=True)
    for name, image in hidden.items():
        image.save(SPRITES / f"{name}.png")
    print(f"wrote {len(hidden)} sprite to {SPRITES}")


if __name__ == "__main__":
    main()
