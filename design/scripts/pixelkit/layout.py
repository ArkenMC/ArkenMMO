"""Every GUI position, derived from the 9x6 chest slot grid.

Rects are half-open (x0, y0, x1, y1). GUI coordinates are GUI pixels with the origin at the
panel's top left; `art()` converts them to art pixels (2 per GUI pixel).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "resourcepack"
ASSETS = PACK / "assets" / "arkenmmo"
PREVIEWS = ROOT / "target" / "previews" / "gui"
TITLES = ROOT / "design" / "scripts" / "titles.json"

DENSITY = 2
SLOT = 18
CHEST_ROWS = 6
PANEL_W = 176
PANEL_H = 222
VANILLA_H = 114 + CHEST_ROWS * SLOT - 1  # rows the vanilla texture paints
TITLE_X, TITLE_Y = 8, 6
LABEL_X, LABEL_Y = 8, 128
# glyph top on screen = 13 - ascent
FONT_ORIGIN_ASCENT = 13


def cell(col, row):
    """18x18 cell of a chest slot."""
    x, y = 7 + SLOT * col, 17 + SLOT * row
    return (x, y, x + SLOT, y + SLOT)


def player_cell(col, row):
    """18x18 cell of the player inventory; rows 0-2 are storage, row 3 the hotbar."""
    first = 17 + CHEST_ROWS * SLOT + 13
    x = 7 + SLOT * col
    y = first + SLOT * row if row < 3 else first + SLOT * 3 + 4
    return (x, y, x + SLOT, y + SLOT)


def union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def art(rect):
    return tuple(v * DENSITY for v in rect)


CANVAS = (PANEL_W * DENSITY, PANEL_H * DENSITY)
GRID = art(union(cell(0, 0), cell(8, CHEST_ROWS - 1)))
HEADER = (0, 0, CANVAS[0], GRID[1])
LEFT_PANEL = art(union(cell(0, 0), cell(3, 5)))
DIVIDER = art(union(cell(4, 0), cell(4, 5)))
RIGHT_PANEL = art(union(cell(5, 0), cell(8, 5)))
ARROW = art(union(cell(4, 4), cell(4, 5)))
PLATE_H = SLOT * DENSITY
INVENTORY_PLATE = art((5, 126, 90, 137))
# Panel frames may reach this far outward on the outer edges; click areas stay the same.
OUTER_OVERHANG = 3 * DENSITY


def panel_frame_rect(panel):
    x0, y0, x1, y1 = panel
    if panel == LEFT_PANEL:
        x0 -= OUTER_OVERHANG
    else:
        x1 += OUTER_OVERHANG
    return (x0, y0, x1, y1)


def plate_rect(panel):
    """Name plate: the bottom slot row of a panel."""
    x0, _, x1, y1 = panel_frame_rect(panel)
    return (x0, y1 - PLATE_H, x1, y1)
