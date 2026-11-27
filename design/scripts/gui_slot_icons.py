"""Empty-slot icons for the survival inventory's armour column, in the iron of the character panel.

Writes resourcepack/assets/minecraft/textures/gui/sprites/container/slot/{helmet,chestplate,leggings,boots}.png
(32x32 = vanilla 16x16 on the 2x grid; the game draws them in an empty armour slot and hides them under worn
armour) and a fully clear shield.png, so the game's grey shield ghost does not show on the plain shell where the
offhand slot used to be. The silhouettes are our own shapes. Spec: design/gui-inventory.md.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

from pixelkit import layout
from pixelkit.chrome import DARK
from pixelkit.draw import poly_mask
from pixelkit.palette import PALETTE, col

SPRITES = layout.PACK / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "container" / "slot"
SIZE = (32, 32)
FILL = col("iron", 4)
SHADE = col("iron", 3)
PANEL = col("iron", 1)

# silhouettes on the 32x32 grid; extra masks are painted over the body in the shade or outline colour
HELMET = [(7, 26), (7, 14), (9, 9), (13, 6), (19, 6), (23, 9), (25, 14), (25, 26), (20, 26), (20, 19), (12, 19), (12, 26)]
CHESTPLATE = [(3, 10), (9, 6), (12, 6), (16, 11), (20, 6), (23, 6), (29, 10), (29, 16), (25, 16), (25, 27), (7, 27),
              (7, 16), (3, 16)]
LEGGINGS = [(8, 5), (24, 5), (25, 27), (18, 27), (16, 15), (14, 27), (7, 27)]
BOOT = [(6, 6), (14, 6), (14, 26), (3, 26), (3, 21), (6, 19)]
BOOTS = [BOOT, [(32 - x, y) for x, y in BOOT]]


def _mask(polygons):
    mask = np.zeros(SIZE[::-1], bool)
    for points in polygons:
        mask |= poly_mask(points, SIZE)
    return mask


def _rect(x0, y0, x1, y1):
    mask = np.zeros(SIZE[::-1], bool)
    mask[y0:y1, x0:x1] = True
    return mask


def _icon(polygons, shade=None, outline=None):
    """Outline ring, quiet iron body, shade along the bottom and right, then any detail masks."""
    body = _mask(polygons)
    inner = ndimage.binary_erosion(body)
    ring = body & ~inner
    image = np.zeros(SIZE[::-1] + (4,), np.uint8)
    image[inner] = FILL
    below_or_right = np.roll(ring, -1, axis=0) | np.roll(ring, -1, axis=1)
    image[inner & below_or_right] = SHADE
    image[ring] = DARK
    if shade is not None:
        image[shade & inner] = SHADE
    if outline is not None:
        image[outline & inner] = DARK
    return Image.fromarray(image, "RGBA")


def icons():
    return {
        "helmet": _icon([HELMET], outline=_rect(10, 14, 22, 17)),
        "chestplate": _icon([CHESTPLATE], shade=_rect(15, 12, 17, 27)),
        "leggings": _icon([LEGGINGS], shade=_rect(0, 5, 32, 9)),
        "boots": _icon(BOOTS, shade=_rect(0, 6, 32, 9)),
    }


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
        stray = {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]} - known
        if stray:
            errors.append(f"{name} has colours outside the palette: {sorted(stray)}")
        ys, xs = np.nonzero(px[..., 3])
        if not len(xs) or xs.min() < 2 or ys.min() < 2 or xs.max() > 29 or ys.max() > 29 or not 200 < len(xs) < 600:
            errors.append(f"{name} must be a solid silhouette inside 2 px margins (200..600 opaque texels)")
        if tuple(PANEL[:3]) in {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]}:
            errors.append(f"{name} uses the panel colour, so it would vanish")
        shapes.add(px[..., 3].tobytes())
    if len(shapes) != len(sprites):
        errors.append("two icons share a silhouette")
    for name, image in hidden.items():
        if image.size != SIZE or np.asarray(image)[..., 3].any():
            errors.append(f"{name} must be {SIZE} and fully transparent")
    if errors:
        raise ValueError("slot icons: " + "; ".join(errors))
    print(f"slot icons: {len(sprites)} silhouettes and {len(hidden)} clear sprite, 32x32, palette, binary alpha")


def main():
    sprites, hidden = icons(), {"shield": clear()}
    check(sprites, hidden)
    SPRITES.mkdir(parents=True, exist_ok=True)
    for name, image in {**sprites, **hidden}.items():
        image.save(SPRITES / f"{name}.png")
    print(f"wrote {len(sprites) + len(hidden)} sprites to {SPRITES}")


if __name__ == "__main__":
    main()
