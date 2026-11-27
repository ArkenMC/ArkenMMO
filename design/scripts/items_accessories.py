"""The four accessory items (ring_1, ring_2, amulet, bracelet): 32x32 textures, item definitions, models and one
shared tooltip style (see design/item-accessories.md).

Same pipeline as the emerald: texture + model + item definition under resourcepack/assets/arkenmmo/. Shapes are
built from small masks (a ring band is a distance ring, gems are hand-written facet rows) so the circles stay
clean at this size; every colour is from the frozen palette.
"""
import numpy as np

from pixelkit import layout, pack
from pixelkit.draw import Canvas
from pixelkit.palette import PALETTE, col

import items_emerald

SIZE = 32
IDS = {"ring_1": "Ring", "ring_2": "Signet Ring", "amulet": "Amulet", "bracelet": "Bracelet"}
TOOLTIP = "accessory"
# 32x32 textures: the model draws them over the slot's 16 GUI px, so one texel is exactly one art px of the 512x512
# inventory texture (half a GUI px). The art is about 24 texels (12 GUI px) across and 4 texels in from the edge, so
# the item reads medium-sized with no display transform (design/item-accessories.md)
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


def gem_mask(cx, cy, hw, hh):
    """A cut gem: a diamond with its four tips cut off (an octagon), hw/hh half width and height."""
    dx, dy = XX + 0.5 - cx, YY + 0.5 - cy
    return (np.abs(dx) / hw + np.abs(dy) / hh <= 1.4) & (np.abs(dx) <= hw) & (np.abs(dy) <= hh)


def paint_gem(px, cx, cy, hw, hh, legend):
    """Facets by direction to the key light (bright top left, dark bottom right), a lighter table in the middle and a
    two pixel glint."""
    mask = gem_mask(cx, cy, hw, hh)
    dx, dy = XX + 0.5 - cx, YY + 0.5 - cy
    u = (dx / hw + dy / hh) / 2
    tone = np.select([u < -0.45, u < 0.0, u < 0.45], [1, 2, 3], 4)
    table = np.abs(dx) / hw + np.abs(dy) / hh <= 0.55
    tone = np.where(table, np.maximum(tone - 1, 1), tone)
    keys = "?ABCD"
    for y, x in zip(*np.nonzero(mask)):
        px[y, x] = col(*legend[keys[tone[y, x]]])
    ys, xs = np.nonzero(table)
    first = np.argmin((dx + dy)[ys, xs])
    y, x = ys[first], xs[first]
    px[y, x] = px[y + 1, x] = col(*legend["w"])
    return mask


def ring_1():
    """Gold band with a ruby in a gold setting."""
    px = new()
    cx, cy = 16, 18
    toned(px, band(cx, cy, 9.5, 5.5), "gold", (5, 4, 3, 1), cx, cy, (0.8, 0.2, -0.35))
    gem = gem_mask(16, 10, 6, 5)
    bezel(px, gem, col("gold", 4), col("gold", 2))
    paint_gem(px, 16, 10, 6, 5, RUBY)
    outline(px, col("gold", 0))
    return px


def ring_2():
    """Iron signet ring: a steel band and a flat seal with a gold cross over a navy field and a small aqua gem."""
    px = new()
    cx, cy = 16, 18
    toned(px, band(cx, cy, 9.5, 5.5), "steel", (5, 4, 3, 1), cx, cy)
    px[rows_mask([(y, 6, 25) for y in range(4, 16)])] = col("gold", 3)
    px[rows_mask([(4, 6, 25)] + [(y, 6, 7) for y in range(5, 15)])] = col("gold", 4)
    px[rows_mask([(15, 6, 25)] + [(y, 24, 25) for y in range(5, 16)])] = col("gold", 2)
    px[rows_mask([(y, 8, 23) for y in range(6, 14)])] = col("navy", 2)
    px[rows_mask([(6, 8, 23), (7, 8, 23)])] = col("navy", 1)
    px[[4, 4, 5, 4, 4, 5, 15, 15, 14, 15, 15, 14], [6, 7, 6, 25, 24, 25, 6, 7, 6, 25, 24, 25]] = 0  # rounded corners
    cross = rows_mask([(y, 15, 16) for y in range(6, 14)] + [(y, 10, 21) for y in (9, 10)])
    px[cross] = col("gold", 4)
    px[rows_mask([(y, 16, 16) for y in range(6, 14)] + [(y, 10, 21) for y in (10,)])] = col("gold", 3)
    facets(px, [(9, 15, "wA"), (10, 15, "BC")], AQUA)
    outline(px, col("steel", 0))
    return px


def amulet_gem():
    return gem_mask(16, 20, 4, 5)


def amulet():
    """Gold chain and a round gold medallion with a violet gem."""
    px = new()
    cx, cy = 16, 20
    for i in range(5):
        lit, dim = (("gold", 5), ("gold", 4)), (("gold", 4), ("gold", 3))
        top, bottom = (lit, ("gold", 2)) if i % 2 == 0 else (dim, ("gold", 1))
        for x0 in (4 + 2 * i, 26 - 2 * i):
            y0 = 4 + 2 * i
            px[y0, x0], px[y0, x0 + 1] = col(*top[0]), col(*top[1])
            px[y0 + 1, x0], px[y0 + 1, x0 + 1] = col(*top[1]), col(*bottom)
    # the last links meet a small bail above the medallion
    px[rows_mask([(9, 14, 17), (10, 14, 14), (11, 14, 14)])] = col("gold", 4)
    px[rows_mask([(10, 17, 17), (11, 17, 17)])] = col("gold", 2)
    px[rows_mask([(10, 15, 16), (11, 15, 16)])] = 0
    px[disc(cx, cy, 7.5)] = col("gold", 1)
    toned(px, band(cx, cy, 7.5, 5.0), "gold", (5, 4, 3, 2), cx, cy)
    paint_gem(px, cx, cy, 4, 5, AMETHYST)
    outline(px, col("gold", 0))
    return px


def bracelet():
    """A cuff lying diagonally (long axis from bottom left to top right): a steel back arc and a thick gold front band
    on the lower right with a green gem. Drawn by testing every pixel in the cuff's own rotated frame (geometry, not
    a resampled bitmap); lit from the top left, so the faces turned up and left are bright."""
    px = new()
    sx, sy = XX + 0.5 - 16, YY + 0.5 - 16
    along, across = (sx - sy) / 2 ** 0.5, (sx + sy) / 2 ** 0.5  # across grows towards the front (lower right)
    outer = np.hypot(along / 13.3, across / 10.0) <= 1
    inner = np.hypot(along / 7.6, (across + 3.2) / 3.9) <= 1
    cuff = outer & ~inner
    edge = cuff.copy()
    for shifted, _, _ in neighbours(~cuff):
        edge &= ~shifted
    px[cuff & ~edge] = col("steel", 0)
    back = edge & (across < 1.8)
    toned(px, back, "steel", (5, 4, 3, 2), 16, 16, thresholds=(0.3, -0.2, -0.7))
    # the near band is gold, brightest on the edge facing up and left, darker towards the outside
    front = edge & (across >= 1.8)
    for limit, step in ((3.6, 5), (5.6, 4), (7.4, 3), (8.7, 2), (99, 1)):
        px[front & (across < limit) & (px[..., 3] == 0)] = col("gold", step)
    gem = (np.abs(along) <= 4.1) & (np.abs(across - 5.8) <= 1.9)
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
        # plain item/generated: the 32x32 texture is the whole size; the medium look is painted, not transformed
        pack.write_json(layout.ASSETS / "models" / "item" / f"{name}.json",
                        {"parent": "minecraft:item/generated", "textures": {"layer0": f"arkenmmo:item/{name}"}})


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
        if min(xs.min(), ys.min()) < 3 or max(xs.max(), ys.max()) > 28:
            errors.append(f"{name} leaves the 3 px margin")
        width, height = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if not 22 <= max(width, height) <= 26:
            errors.append(f"{name} is {width}x{height} texels, its longer side must be 22..26 (11..13 GUI px)")
        if not 250 < len(xs) < 700:
            errors.append(f"{name} has {len(xs)} opaque pixels (250..700 expected)")
        if len(colours) > 24:
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
