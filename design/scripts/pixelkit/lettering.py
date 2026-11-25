"""Custom pixel capitals, 12x16 art px with 3 px strokes and clipped corners."""
import numpy as np
from scipy.ndimage import binary_fill_holes

from .draw import Canvas, dilate
from .palette import col

HEIGHT = 16
GAP = 2
SPACE = 10

GLYPHS = {
    "A": """
..########..
.##########.
############
###......###
###......###
###......###
###......###
############
############
############
###......###
###......###
###......###
###......###
###......###
###......###""",
    "C": """
..########..
.##########.
############
###......###
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###......###
############
.##########.
..########..""",
    "E": """
############
############
############
###.........
###.........
###.........
###.........
##########..
##########..
##########..
###.........
###.........
###.........
############
############
############""",
    "H": """
###......###
###......###
###......###
###......###
###......###
###......###
###......###
############
############
############
###......###
###......###
###......###
###......###
###......###
###......###""",
    "I": """
########
########
########
..###...
..###...
..###...
..###...
..###...
..###...
..###...
..###...
..###...
..###...
########
########
########""",
    "L": """
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
###.........
############
############
############""",
    "O": """
..########..
.##########.
############
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
############
.##########.
..########..""",
    "R": """
##########..
###########.
############
###......###
###......###
###......###
############
###########.
##########..
###..###....
###..####...
###...###...
###...####..
###....###..
###....####.
###.....###.""",
    "S": """
..########..
.##########.
############
###......###
###.........
###.........
####........
.#########..
..#########.
........####
.........###
.........###
###......###
############
.##########.
..########..""",
    "U": """
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
###......###
############
.##########.
..########..""",
    "W": """
###......###
###......###
###......###
###......###
###......###
###......###
###..##..###
###..##..###
###..##..###
###.####.###
###.####.###
############
############
#####..#####
.###....###.
.###....###.""",
    "Y": """
###......###
###......###
###......###
###......###
####....####
.###....###.
..###..###..
...######...
....####....
....####....
....###.....
....###.....
....###.....
....###.....
....###.....
....###.....""",
}


def _rows(letter):
    rows = GLYPHS[letter].strip("\n").split("\n")
    if len(rows) != HEIGHT or len({len(r) for r in rows}) != 1:
        raise ValueError(f"glyph {letter!r} must be {HEIGHT} equal-width rows")
    return rows


def width(text):
    total = 0
    for i, ch in enumerate(text):
        if ch == " ":
            total += SPACE
            continue
        total += len(_rows(ch)[0])
        if i + 1 < len(text) and text[i + 1] != " ":
            total += GAP
    return total


def _stamp(canvas, text, x, y, colour_of_row):
    for i, ch in enumerate(text):
        if ch == " ":
            x += SPACE
            continue
        rows = _rows(ch)
        for dy, row in enumerate(rows):
            for dx, pixel in enumerate(row):
                if pixel == "#":
                    canvas.dot(x + dx, y + dy, colour_of_row(dy))
        x += len(rows[0]) + (GAP if i + 1 < len(text) and text[i + 1] != " " else 0)


def draw(canvas, text, centre_x, y, faces, edge, drop=1):
    """`faces` is (upper, lower, bevel) as (ramp, step); `edge` outlines the letters and forms the drop."""
    upper, lower, bevel = (col(*f) for f in faces)
    x = centre_x - width(text) // 2
    ink = Canvas(*canvas.size)
    _stamp(ink, text, x, y, lambda row: upper if row < 9 else lower)
    mask = ink.px[..., 3] > 0
    # two rings around the letters, then extended downward for the drop edge
    backing = dilate(dilate(mask))
    ringed = backing.copy()
    for d in range(1, drop + 1):
        shifted = ringed.copy()
        shifted[d:] = ringed[:-d]
        backing = backing | shifted
    # close slots up to 3 px wide, so no specks of the field show between letters
    for _ in range(2):
        pinched = np.zeros_like(backing)
        for left, right in ((1, 1), (1, 2), (2, 1)):
            pinched[:, left:-right] |= backing[:, :-left - right] & backing[:, left + right:]
        backing |= pinched
    canvas.mask(binary_fill_holes(backing), col(*edge))
    canvas.paste(ink)
    # one lit row along every top edge
    top = mask.copy()
    top[1:] &= ~mask[:-1]
    canvas.mask(top, bevel)
