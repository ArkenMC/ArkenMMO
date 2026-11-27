"""Ornaments of the player inventory screen: the model alcove, the fluted pillar, the crest medallion and the
corner studs of the gridless regions. Drawn in art px on the 2x grid; shapes stay on the GUI pixel grid."""
import numpy as np

from . import rounded
from .chrome import DARK, _crossed_swords, gem
from .draw import dilate, frame, poly_mask, shift
from .palette import col

# Arch over the alcove, in GUI px: columns lost at each top corner, row by row (a round arch of radius 12)
ARCH = (7, 5, 3, 2, 2, 1, 1, 1)
BRICK = (8, 4)  # GUI px, running bond


def _arched(size, box):
    mask = rounded.rect(size, box)
    x0, y0, x1, _ = box
    for row, inset in enumerate(ARCH):
        mask[y0 + row, x0:x0 + inset] = False
        mask[y0 + row, x1 - inset:x1] = False
    return mask


def alcove(canvas, gui_size, box, floor_y):
    """A dark, arched stone-brick niche behind the player model, with a stepped dais and two gold sconces.
    `box` and `floor_y` (top of the dais) are in GUI px; returns the alcove's art-px mask."""
    mask = rounded.upscale(_arched(gui_size, box))
    x0, y0, x1, y1 = (v * 2 for v in box)
    # spandrels: the corners above the arch are solid stone, a step darker than the panel
    canvas.mask(_rect_like(mask, (x0, y0, x1, y0 + len(ARCH) * 2)) & ~mask, col("iron", 2))
    canvas.mask(mask, col("iron", 1))
    # bricks: mortar on the bottom and right of each brick, a lit top edge, a few chipped corners
    bw, bh = BRICK[0] * 2, BRICK[1] * 2
    for row, top in enumerate(range(y0, y1, bh)):
        offset = (row % 2) * bw // 2
        for left in range(x0 - bw + offset, x1, bw):
            brick = np.zeros_like(mask)
            brick[top:top + bh - 1, max(left, 0):left + bw - 1] = True
            brick &= mask
            canvas.mask(mask & _rect_like(mask, (left, top + bh - 1, left + bw, top + bh)), DARK)
            canvas.mask(mask & _rect_like(mask, (left + bw - 1, top, left + bw, top + bh)), DARK)
            canvas.mask(brick & _rect_like(mask, (left, top, left + bw - 1, top + 1)), col("iron", 2))
            if (row * 7 + left // bw * 3) % 6 == 0:
                canvas.mask(brick & _rect_like(mask, (left + bw - 4, top + bh - 3, left + bw - 1, top + bh - 1)), DARK)
    _dais(canvas, mask, x0, x1, floor_y * 2, y1)
    for sx in (x0 + 10, x1 - 14):
        _sconce(canvas, sx, y0 + 34)
    number, lit = rounded.rings(mask, inside=True)
    canvas.mask((number == 1) & lit, DARK)
    canvas.mask((number == 2) & lit, DARK)
    canvas.mask((number == 1) & ~lit, col("iron", 4))
    canvas.mask((number == 2) & ~lit, col("iron", 2))
    _keystone(canvas, (x0 + x1) // 2, y0)
    return mask


def _keystone(canvas, cx, top):
    """A wedge stone at the crown of the arch, raised (lit top left), with a small gold stud."""
    shape = [(cx - 7, top), (cx + 7, top), (cx + 5, top + 12), (cx - 5, top + 12)]
    mask = poly_mask(shape, canvas.size)
    canvas.mask(dilate(mask), DARK)
    canvas.mask(mask, col("iron", 3))
    canvas.mask(mask & ~shift(mask, 0, 2), col("iron", 4))
    canvas.mask(mask & ~shift(mask, 2, 0), col("iron", 4))
    canvas.mask(mask & ~shift(mask, 0, -2), col("iron", 2))
    gem(canvas, cx, top + 6, 2)


def _rect_like(mask, r):
    out = np.zeros_like(mask)
    x0, y0, x1, y1 = r
    out[max(y0, 0):max(y1, 0), max(x0, 0):max(x1, 0)] = True
    return out


def _dais(canvas, mask, x0, x1, top, bottom):
    """Floor flags across the niche and a two-step dais the model stands on."""
    canvas.mask(mask & _rect_like(mask, (x0, top + 6, x1, bottom)), col("iron", 2))
    canvas.mask(mask & _rect_like(mask, (x0, top + 6, x1, top + 7)), col("iron", 3))
    for jx in range(x0 + 6, x1, 14):
        canvas.mask(mask & _rect_like(mask, (jx, top + 7, jx + 1, bottom)), col("iron", 1))
    cx = (x0 + x1) // 2
    for half, step_top, face in ((30, top, 3), (22, top - 4, 4)):
        canvas.rect((cx - half, step_top, cx + half, step_top + 6), col("iron", face - 1))
        canvas.rect((cx - half, step_top, cx + half, step_top + 2), col("iron", face))
        canvas.rect((cx - half, step_top, cx + half, step_top + 1), col("iron", min(face + 1, 5)))
        canvas.rect((cx - half, step_top + 6, cx + half, step_top + 7), DARK)
        canvas.rect((cx - half - 1, step_top, cx - half, step_top + 7), DARK)
        canvas.rect((cx + half, step_top, cx + half + 1, step_top + 7), DARK)


def _sconce(canvas, x, y):
    """A small iron wall cup with a gold flame, 4 GUI px wide."""
    canvas.rect((x - 1, y + 7, x + 9, y + 13), DARK)
    canvas.rect((x, y + 8, x + 8, y + 10), col("iron", 5))
    canvas.rect((x + 2, y + 10, x + 6, y + 12), col("iron", 4))
    canvas.rect((x + 3, y + 12, x + 5, y + 16), col("iron", 3))
    flame = [(x + 2, y + 7), (x + 1, y + 4), (x + 3, y), (x + 4, y - 2), (x + 6, y + 2), (x + 7, y + 5), (x + 6, y + 7)]
    mask = poly_mask(flame, canvas.size)
    canvas.mask(dilate(mask), DARK)
    canvas.mask(mask, col("gold", 3))
    canvas.rect((x + 3, y + 3, x + 5, y + 7), col("gold", 5))
    canvas.rect((x + 3, y + 5, x + 5, y + 7), col("gold", 4))


def pillar(canvas, x0, y0, x1, y1):
    """A free-standing fluted iron column with gold capital and base bands (the class menu's divider)."""
    cx = (x0 + x1) // 2
    shaft = (x0 + 3, y0 + 7, x1 - 3, y1 - 7)
    frame(canvas, shaft, [(DARK, DARK), (col("iron", 5), col("iron", 1)), (col("iron", 4), col("iron", 2))])
    canvas.rect((shaft[0] + 3, shaft[1] + 3, shaft[2] - 3, shaft[3] - 3), col("iron", 3))
    for fx in (cx - 5, cx + 3):
        canvas.rect((fx, shaft[1] + 4, fx + 1, shaft[3] - 4), col("iron", 1))
        canvas.rect((fx + 1, shaft[1] + 4, fx + 2, shaft[3] - 4), col("iron", 5))
    for band_y in (y0, y1 - 9):
        band = (x0, band_y, x1, band_y + 9)
        frame(canvas, band, [(DARK, DARK), (col("gold", 4), col("gold", 1))])
        canvas.rect((band[0] + 2, band[1] + 2, band[2] - 2, band[3] - 2), col("gold", 2))
        canvas.rect((band[0] + 2, band[1] + 4, band[2] - 2, band[1] + 5), col("gold", 3))


def crest(canvas, cx, cy):
    """Octagonal iron medallion with the crossed swords, flanked by tapering gold blades ending in gems."""
    r, c = 18, 7
    octagon = [(cx - r + c, cy - r), (cx + r - c, cy - r), (cx + r, cy - r + c), (cx + r, cy + r - c),
               (cx + r - c, cy + r), (cx - r + c, cy + r), (cx - r, cy + r - c), (cx - r, cy - r + c)]
    for direction in (1, -1):
        root, tip = cx + direction * (r - 2), cx + direction * 58
        canvas.poly([(root, cy - 5), (tip, cy), (root, cy + 5)], DARK)
        canvas.poly([(root, cy - 3), (tip - direction * 4, cy), (root, cy)], col("gold", 3))
        canvas.poly([(root, cy), (tip - direction * 4, cy), (root, cy + 3)], col("gold", 1))
        gem(canvas, cx + direction * 44, cy, 3)
        gem(canvas, tip + direction * 2, cy, 2)
    mask = poly_mask(octagon, canvas.size)
    canvas.mask(dilate(dilate(mask)), DARK)
    canvas.mask(mask, col("gold", 1))
    inner = mask & shift(mask, 1, 1) & shift(mask, -1, -1) & shift(mask, 1, -1) & shift(mask, -1, 1)
    canvas.mask(mask & ~shift(mask, 0, 1) | mask & ~shift(mask, 1, 0), col("gold", 4))
    face = inner & shift(inner, 2, 2) & shift(inner, -2, -2) & shift(inner, 2, -2) & shift(inner, -2, 2)
    canvas.mask(face, col("iron", 1))
    canvas.mask(face & ~shift(face, 0, 1), DARK)
    canvas.mask(face & ~shift(face, 0, 2) & shift(face, 0, 1), DARK)
    _crossed_swords(canvas, cx, cy + 1)


def grid(canvas, cell_groups, region_masks, size=18, colour=None):
    """A 1 art px line in the margin between every two neighbouring gridless cells of one region (the margin is
    the 2 GUI px between their item areas), clipped to the region's fill. It never enters an item area."""
    colour = colour if colour is not None else col("iron", 4)
    for name, group in cell_groups.items():
        fill = region_masks[name]
        cells = set(group)
        line = np.zeros_like(fill)
        for x, y in group:
            if (x + size, y) in cells:
                line[y * 2:(y + size) * 2, (x + size) * 2 - 1] = True
            if (x, y + size) in cells:
                line[(y + size) * 2 - 1, x * 2:(x + size) * 2] = True
        canvas.mask(line & fill, colour)


def studs(canvas, cell_groups, region_masks, size=18):
    """A small gold stud (2x2 GUI px: gold body, lit top-left, shaded bottom-right) on every corner shared by four
    gridless cells of one region, where it lies inside that region's fill. `cell_groups` maps a region name to
    its cells."""
    placed = []
    for name, group in cell_groups.items():
        fill = region_masks[name]
        corners = {}
        for x, y in group:
            for corner in ((x, y), (x + size, y), (x, y + size), (x + size, y + size)):
                corners[corner] = corners.get(corner, 0) + 1
        for (gx, gy), count in corners.items():
            ax, ay = (gx - 1) * 2, (gy - 1) * 2
            if count < 4 or not fill[ay:ay + 4, ax:ax + 4].all():
                continue
            canvas.rect((ax, ay, ax + 4, ay + 4), col("gold", 3))
            canvas.rect((ax + 3, ay, ax + 4, ay + 4), col("gold", 2))
            canvas.rect((ax, ay + 3, ax + 4, ay + 4), col("gold", 2))
            canvas.rect((ax, ay, ax + 2, ay + 2), col("gold", 4))
            placed.append((gx, gy))
    return placed
