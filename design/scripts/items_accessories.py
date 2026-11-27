"""The four accessory items (ring_1, ring_2, amulet, bracelet): 16x16 textures, item definitions, models and one
shared tooltip style (see design/item-accessories.md).

Same pipeline as the emerald: texture + model + item definition under resourcepack/assets/arkenmmo/. Shapes are
built from small masks (a ring band is a distance ring, gems are hand-written facet rows) so the circles stay
clean at 16 px; every colour is from the frozen palette.
"""
import numpy as np

from pixelkit import layout, pack
from pixelkit.draw import Canvas
from pixelkit.palette import PALETTE, col

import items_emerald

SIZE = 16
IDS = {"ring_1": "Ring", "ring_2": "Signet Ring", "amulet": "Amulet", "bracelet": "Bracelet"}
TOOLTIP = "accessory"
# gui display scale of the item models: 0.5 makes one texel exactly one art px of the 512x512 inventory texture
# (half a GUI px), so the painted placeholders line up with the item's own pixels (design/item-accessories.md)
GUI_SCALE = 0.5
YY, XX = np.mgrid[0:SIZE, 0:SIZE]


def disc(cx, cy, radius):
    return np.hypot(XX + 0.5 - cx, YY + 0.5 - cy) <= radius


def band(cx, cy, outer, inner):
    return disc(cx, cy, outer) & ~disc(cx, cy, inner)


def light(cx, cy):
    """-1..1 per pixel: how much its direction from the centre faces the key light at the top left."""
    vx, vy = XX + 0.5 - cx, YY + 0.5 - cy
    return (-vx - vy) / (np.hypot(vx, vy) * 2 ** 0.5 + 1e-9)


def toned(px, mask, ramp, steps, cx, cy, thresholds=(0.55, 0.05, -0.45)):
    """Paint `mask` with ramp steps (bright to dark, four of them) by facing: 3-D band shading."""
    t = light(cx, cy)
    bright, lit, mid, dark = steps
    px[mask & (t > thresholds[0])] = col(ramp, bright)
    px[mask & (t <= thresholds[0]) & (t > thresholds[1])] = col(ramp, lit)
    px[mask & (t <= thresholds[1]) & (t > thresholds[2])] = col(ramp, mid)
    px[mask & (t <= thresholds[2])] = col(ramp, dark)


def rows_mask(rows):
    """Mask from a list of (y, x0, x1) spans, x1 inclusive."""
    mask = np.zeros((SIZE, SIZE), bool)
    for y, x0, x1 in rows:
        mask[y, x0:x1 + 1] = True
    return mask


def facets(px, rows, legend):
    """Hand-written gem rows: (y, x0, string); one character per pixel."""
    for y, x0, text in rows:
        for dx, ch in enumerate(text):
            px[y, x0 + dx] = col(*legend[ch])


def spans(rows):
    return rows_mask([(y, x0, x0 + len(text) - 1) for y, x0, text in rows])


def neighbours(mask):
    """4-neighbour dilation, as a list of (shifted mask, dx, dy) for the pixel each neighbour came from."""
    out = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        shifted = np.roll(np.roll(mask, dx, axis=1), dy, axis=0)
        out.append((shifted, dx, dy))
    return out


def bezel(px, inner, lit_colour, shade_colour):
    """A 1 px setting round a gem: lit where it lies above or left of the gem, shaded below and right."""
    for shifted, dx, dy in neighbours(inner):
        px[shifted & ~inner] = shade_colour if dx > 0 or dy > 0 else lit_colour


def outline(px, colour):
    """A 1 px dark outline on every transparent pixel next to a drawn one (hole edges too)."""
    solid = px[..., 3] > 0
    edge = np.zeros_like(solid)
    for shifted, _, _ in neighbours(solid):
        edge |= shifted
    edge &= ~solid
    # np.roll wraps round the border: keep the art one pixel inside
    edge[0, :] = edge[-1, :] = False
    edge[:, 0] = edge[:, -1] = False
    px[edge] = colour


def new():
    return np.zeros((SIZE, SIZE, 4), np.uint8)


RUBY = {"w": ("ivory", 4), "A": ("crimson", 4), "B": ("crimson", 3), "C": ("crimson", 2), "D": ("crimson", 1)}
AMETHYST = {"w": ("violet", 5), "A": ("violet", 4), "B": ("violet", 3), "C": ("violet", 2), "D": ("violet", 1)}
AQUA = {"w": ("arcane", 4), "A": ("arcane", 3), "B": ("arcane", 2), "C": ("arcane", 1), "D": ("arcane", 0)}
LEAF = {"w": ("forest", 5), "A": ("forest", 4), "B": ("forest", 3), "C": ("forest", 2), "D": ("forest", 1)}

# a diamond-cut gem, 6 wide and 5 tall, glint at the top left
GEM_ROWS = [(2, 7, "AB"), (3, 6, "wABC"), (4, 5, "AABBCD"), (5, 6, "BBCD"), (6, 7, "CD")]


def ring_1():
    """Gold band with a ruby in a gold setting."""
    px = new()
    cx, cy = 8, 10
    toned(px, band(cx, cy, 5, 3), "gold", (5, 4, 3, 1), cx, cy, (0.8, 0.2, -0.35))
    gem = spans(GEM_ROWS)
    bezel(px, gem, col("gold", 4), col("gold", 2))
    facets(px, GEM_ROWS, RUBY)
    outline(px, col("gold", 0))
    return px


def ring_2():
    """Iron signet ring: a steel band and a flat seal with a gold cross over a navy field and a small aqua gem."""
    px = new()
    cx, cy = 8, 10
    toned(px, band(cx, cy, 5, 3), "steel", (5, 4, 3, 1), cx, cy)
    field = rows_mask([(y, 4, 11) for y in range(2, 6)])
    seal = rows_mask([(y, 3, 12) for y in range(1, 7)])
    px[seal] = col("gold", 3)
    px[rows_mask([(1, 3, 12), (2, 3, 3), (3, 3, 3), (4, 3, 3), (5, 3, 3)])] = col("gold", 4)
    px[rows_mask([(6, 3, 12)]) | rows_mask([(y, 12, 12) for y in range(2, 7)])] = col("gold", 2)
    px[field] = col("navy", 2)
    px[rows_mask([(2, 4, 11)])] = col("navy", 1)
    px[[1, 1, 6, 6], [3, 12, 3, 12]] = 0  # rounded seal corners
    cross = rows_mask([(y, 7, 8) for y in range(2, 6)] + [(y, 5, 10) for y in (3, 4)])
    px[cross] = col("gold", 4)
    px[rows_mask([(y, 8, 8) for y in range(2, 6)] + [(y, 10, 10) for y in (3, 4)])] = col("gold", 3)
    facets(px, [(3, 7, "wA"), (4, 7, "BC")], AQUA)
    outline(px, col("steel", 0))
    return px


AMULET_GEM = [(7, 7, "AB"), (8, 6, "wABB"), (9, 6, "AABC"), (10, 6, "ABCC"), (11, 6, "BCCD"), (12, 7, "CD")]


def amulet():
    """Gold chain and a round gold medallion with a violet gem."""
    px = new()
    cx, cy = 8, 10
    for i in range(5):
        for x in (1 + i, 14 - i):
            px[i, x] = col("gold", 4 if i % 2 == 0 else 2)
    # the chain's last links meet a small bail above the medallion
    px[5, 6] = col("gold", 4)
    px[5, 9] = col("gold", 2)
    for x in (7, 8):
        px[4, x] = col("gold", 3)
        px[5, x] = col("gold", 2)
    ring = band(cx, cy, 4.6, 3.1)
    px[disc(cx, cy, 4.6)] = col("gold", 1)
    toned(px, ring, "gold", (5, 4, 3, 2), cx, cy)
    facets(px, AMULET_GEM, AMETHYST)
    outline(px, col("gold", 0))
    return px


def bracelet():
    """A cuff lying diagonally (long axis from bottom left to top right): a steel back arc and a thick gold front band
    on the lower right with a green gem. Drawn by testing every pixel in the cuff's own rotated frame (geometry, not
    a resampled bitmap); lit from the top left, so the faces turned up and left are bright."""
    px = new()
    sx, sy = XX + 0.5 - 8, YY + 0.5 - 8
    along, across = (sx - sy) / 2 ** 0.5, (sx + sy) / 2 ** 0.5  # across grows towards the front (lower right)
    outer = np.hypot(along / 7.2, across / 5.4) <= 1
    inner = np.hypot(along / 4.1, (across + 1.7) / 2.1) <= 1
    cuff = outer & ~inner
    edge = cuff.copy()
    for shifted, _, _ in neighbours(~cuff):
        edge &= ~shifted
    px[cuff & ~edge] = col("steel", 0)
    back = edge & (across < 1.0)
    toned(px, back, "steel", (5, 4, 3, 2), 8, 8, thresholds=(0.3, -0.2, -0.7))
    # the near band is gold, brightest on the edge facing up and left, darker towards the outside
    front = edge & (across >= 1.0)
    for limit, step in ((1.9, 5), (3.0, 4), (4.0, 3), (4.7, 2), (99, 1)):
        px[front & (across < limit) & (px[..., 3] == 0)] = col("gold", step)
    gem = (np.abs(along) <= 2.2) & (np.abs(across - 3.1) <= 1.0)
    tones = "wABC"
    ys, xs = np.nonzero(gem)
    rank = np.argsort(np.argsort((sx + sy)[ys, xs], kind="stable"), kind="stable")
    bezel(px, gem, col("gold", 4), col("gold", 2))
    for r, y, x in zip(rank, ys, xs):
        px[y, x] = col(*LEAF[tones[min(3, r * 4 // len(ys))]])
    return px


DRAW = {"ring_1": ring_1, "ring_2": ring_2, "amulet": amulet, "bracelet": bracelet}


def textures():
    folder = layout.ASSETS / "textures" / "item"
    folder.mkdir(parents=True, exist_ok=True)
    for name, draw in DRAW.items():
        canvas = Canvas(SIZE, SIZE)
        canvas.px[:] = draw()
        canvas.image().save(folder / f"{name}.png", optimize=True)


def definitions():
    for name in IDS:
        pack.write_json(layout.ASSETS / "items" / f"{name}.json",
                        {"model": {"type": "minecraft:model", "model": f"arkenmmo:item/{name}"}})
        # item/generated has no gui display of its own, so this entry is the whole gui transform; the other contexts
        # (ground, hands, item frame, head) are inherited from the parent per context
        pack.write_json(layout.ASSETS / "models" / "item" / f"{name}.json",
                        {"parent": "minecraft:item/generated", "textures": {"layer0": f"arkenmmo:item/{name}"},
                         "display": {"gui": {"rotation": [0, 0, 0], "translation": [0, 0, 0],
                                             "scale": [GUI_SCALE] * 3}}})


def check():
    known = {c[:3] for ramp in PALETTE.values() for c in ramp}
    errors = []
    for name, draw in DRAW.items():
        px = draw()
        if not set(px[..., 3].flatten().tolist()) <= {0, 255}:
            errors.append(f"{name} alpha is not binary")
        colours = {tuple(int(v) for v in p[:3]) for p in px[px[..., 3] > 0]}
        if colours - known:
            errors.append(f"{name} has colours outside the palette")
        ys, xs = np.nonzero(px[..., 3])
        if xs.min() < 1 or ys.min() < 0 or xs.max() > 14 or ys.max() > 15:
            errors.append(f"{name} touches the border (art must stay 1 px off the left and right)")
        if not 70 < len(xs) < 200:
            errors.append(f"{name} has {len(xs)} opaque pixels (70..200 expected)")
        if len(colours) > 20:
            errors.append(f"{name} uses {len(colours)} colours")
    if errors:
        raise ValueError("accessories: " + "; ".join(errors))


def main():
    check()
    textures()
    definitions()
    items_emerald.tooltip(TOOLTIP, "gold", (5, 4, 2, 1))
    print(f"accessory textures, definitions and models written for {', '.join(IDS)}; tooltip style arkenmmo:{TOOLTIP}")


if __name__ == "__main__":
    main()
