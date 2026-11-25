"""The page frame shared by every class page: header, panel frames, divider, name plates, inventory."""
import numpy as np

from . import layout, lettering
from .draw import dilate, frame, poly_mask, shift
from .layout import art, cell, player_cell
from .palette import col

DARK = col("iron", 0)


def _diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


def gem(canvas, cx, cy, radius, ramp="gold", lit=True):
    """Four-facet stud lit from the top left, with a dark setting."""
    canvas.poly(_diamond(cx, cy, radius + 2, radius + 2), DARK)
    steps = (4, 3, 1, 2) if lit else (3, 2, 1, 2)
    top, right, bottom, left = (cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)
    for (a, b), step in zip(((left, top), (top, right), (right, bottom), (bottom, left)), steps):
        canvas.poly([(cx, cy), a, b], col(ramp, step))
    if lit:
        canvas.rect((cx - radius // 2, cy - radius // 2, cx - radius // 2 + 2, cy - radius // 2 + 1), col(ramp, 5))


def corner_bracket(canvas, x, y, dx, dy, length=14):
    """L-shaped gold fitting; the mask is mirrored by (dx, dy) but always shaded from the top left."""
    def span(a0, a1, b0, b1):
        xs, ys = sorted((x + dx * a0, x + dx * a1)), sorted((y + dy * b0, y + dy * b1))
        return (xs[0], ys[0], xs[1], ys[1])

    arms = [span(0, length, 0, 5), span(0, 5, 0, length)]
    for x0, y0, x1, y1 in arms:
        canvas.rect((x0 - 1, y0 - 1, x1 + 1, y1 + 1), DARK)
    for x0, y0, x1, y1 in arms:
        canvas.rect((x0, y0, x1, y1), col("gold", 2))
        canvas.rect((x0, y0, x1, y0 + 1), col("gold", 4))
        canvas.rect((x0, y0, x0 + 1, y1), col("gold", 4))
        canvas.rect((x0, y1 - 1, x1, y1), col("gold", 1))
        canvas.rect((x1 - 1, y0 + 1, x1, y1), col("gold", 1))
    rivet = span(1, 4, 1, 4)
    canvas.rect(rivet, col("gold", 4))
    canvas.rect((rivet[0], rivet[1], rivet[0] + 1, rivet[1] + 1), col("gold", 5))


def shell(canvas):
    """Opaque iron body covering the whole vanilla panel, with its bevelled outer rim."""
    width, height = layout.CANVAS
    bottom = layout.VANILLA_H * layout.DENSITY
    body = (0, 0, width, bottom)
    canvas.rect(body, col("iron", 2))
    rim = [(DARK, DARK), (DARK, DARK),
           (col("iron", 5), col("iron", 1)), (col("iron", 4), col("iron", 1)),
           (col("iron", 3), col("iron", 2)), (col("iron", 3), col("iron", 2)),
           (DARK, col("iron", 4))]
    frame(canvas, body, rim)
    # one GUI pixel off each corner, which the vanilla texture also leaves clear
    for x in (0, width - 2):
        for y in (0, bottom - 2):
            canvas.rect((x, y, x + 2, y + 2), (0, 0, 0, 0))


def header(canvas, title="CHOOSE YOUR CLASS"):
    x0, y0, x1, y1 = layout.HEADER
    plaque = (x0 + 38, y0 + 4, x1 - 38, y1 - 2)
    frame(canvas, plaque, [(DARK, DARK), (col("gold", 3), col("gold", 1)), (col("gold", 1), col("gold", 2))])
    inner = (plaque[0] + 3, plaque[1] + 3, plaque[2] - 3, plaque[3] - 3)
    canvas.rect(inner, col("iron", 1))
    canvas.rect((inner[0], inner[1], inner[2], inner[1] + 2), DARK)
    lettering.draw(canvas, title, (x0 + x1) // 2, plaque[1] + 4,
                   (("gold", 4), ("gold", 3), ("gold", 5)), ("iron", 0))
    # side ornaments: a gem on a tapering blade of light, mirrored in shape, lit from the top left
    middle = (plaque[1] + plaque[3]) // 2
    for centre, direction in ((22, 1), (x1 - 22, -1)):
        canvas.poly([(centre, middle - 4), (centre + direction * 17, middle), (centre, middle + 4)], DARK)
        canvas.poly([(centre, middle - 2), (centre + direction * 13, middle), (centre, middle)], col("gold", 3))
        canvas.poly([(centre, middle), (centre + direction * 13, middle), (centre, middle + 2)], col("gold", 1))
        gem(canvas, centre, middle, 7)
        gem(canvas, centre - direction * 12, middle, 3)
    for x, dx in ((4, 1), (x1 - 4, -1)):
        corner_bracket(canvas, x, 4, dx, 1, 11)


def panel_frame(canvas, panel):
    """Frame around one class panel's art; returns the interior rect left for the backdrop."""
    x0, y0, x1, y1 = layout.panel_frame_rect(panel)
    y1 -= layout.PLATE_H
    frame(canvas, (x0, y0, x1, y1), [
        (DARK, DARK), (DARK, DARK),
        (col("gold", 3), col("gold", 1)), (col("iron", 5), col("iron", 2)),
        (col("iron", 4), col("iron", 3)), (col("gold", 1), col("gold", 3)),
        (DARK, DARK)])
    return (x0 + 7, y0 + 7, x1 - 7, y1 - 7)


def panel_corners(canvas, panel):
    x0, y0, x1, y1 = layout.panel_frame_rect(panel)
    y1 -= layout.PLATE_H
    corner_bracket(canvas, x0 + 2, y0 + 2, 1, 1)
    corner_bracket(canvas, x1 - 2, y0 + 2, -1, 1)


def name_plate(canvas, panel, text, ramp, letters, trim="gold", trim_step=0):
    """Notched banner across the bottom slot row. `letters` is the lettering face triple."""
    x0, y0, x1, y1 = layout.plate_rect(panel)
    canvas.rect((x0, y0, x1, y1), DARK)
    canvas.rect((x0 + 2, y0 + 2, x1 - 2, y1 - 2), col("iron", 1))
    mid = (y0 + y1) // 2

    def banner(inset_x, top, bottom, notch):
        left, right = x0 + inset_x, x1 - inset_x
        return [(left, top), (right, top), (right - notch, mid), (right, bottom), (left, bottom), (left + notch, mid)]

    def fill(points, colour, rows=None):
        mask = poly_mask(points, canvas.size)
        if rows:
            mask[:rows[0]] = False
            mask[rows[1]:] = False
        canvas.mask(mask, colour)

    fill(banner(2, y0 + 3, y1 - 3, 11), DARK)
    fill(banner(5, y0 + 5, y1 - 5, 10), col(trim, 3 + trim_step))
    fill(banner(5, y0 + 5, y1 - 5, 10), col(trim, 1 + trim_step), (mid, y1))
    fill(banner(9, y0 + 7, y1 - 7, 9), col(ramp, 1))
    fill(banner(9, y0 + 7, y1 - 7, 9), col(ramp, 2), (y0, mid + 1))
    fill(banner(9, y0 + 7, y1 - 7, 9), col(ramp, 0), (y1 - 9, y1))
    lettering.draw(canvas, text, (x0 + x1) // 2, y0 + 10, letters, ("iron", 0))


# Half of the divider crest: a sword pointing up-left. Mirrored for the other, shaded after mirroring.
CREST_SWORD = ["###.................",
               "####................",
               "#####...............",
               ".#####..............",
               "..#####.............",
               "...#####............",
               "....#####...........",
               ".....#####..........",
               "......#####.........",
               ".......#####........",
               "........#####.......",
               ".........#####......",
               "..........#####.##..",
               "...........#######..",
               "............#####...",
               "...........#####....",
               "..........###.####..",
               "..........##...####.",
               "................###.",
               "....................",
               ]


def _crossed_swords(canvas, cx, cy):
    size = len(CREST_SWORD[0])
    for mirrored in (True, False):
        mask = np.zeros(canvas.px.shape[:2], bool)
        for dy, row in enumerate(CREST_SWORD):
            for dx, pixel in enumerate(row[::-1] if mirrored else row):
                if pixel == "#":
                    mask[cy - len(CREST_SWORD) // 2 + dy, cx - size // 2 + dx] = True
        canvas.mask(dilate(dilate(mask)), DARK)
        canvas.mask(mask, col("gold", 3))
        canvas.mask(mask & ~shift(mask, 0, 1), col("gold", 5))
        canvas.mask(mask & ~shift(mask, 0, -1), col("gold", 2))


def _pillar(canvas, bottom):
    """The divider column from the grid's top down to `bottom`, with the crest in its first slot row."""
    x0, y0, x1, y1 = layout.DIVIDER
    cx = (x0 + x1) // 2
    canvas.rect((x0, y0, x1, y1), col("iron", 1))
    # stone shaft with two flutes, between a capital and a base
    shaft = (x0 + 6, y0 + 4, x1 - 6, bottom)
    frame(canvas, shaft, [(DARK, DARK), (col("iron", 5), col("iron", 1)), (col("iron", 4), col("iron", 2))])
    canvas.rect((shaft[0] + 3, shaft[1] + 3, shaft[2] - 3, shaft[3] - 3), col("iron", 3))
    for fx in (cx - 5, cx + 3):
        canvas.rect((fx, shaft[1] + 6, fx + 1, shaft[3] - 6), col("iron", 1))
        canvas.rect((fx + 1, shaft[1] + 6, fx + 2, shaft[3] - 6), col("iron", 5))
    for band_y in (y0 + 2, shaft[3] - 9):
        band = (x0 + 3, band_y, x1 - 3, band_y + 9)
        frame(canvas, band, [(DARK, DARK), (col("gold", 4), col("gold", 1))])
        canvas.rect((band[0] + 2, band[1] + 2, band[2] - 2, band[3] - 2), col("gold", 2))
    crest_y = (art(cell(4, 0))[1] + art(cell(4, 0))[3]) // 2 + 5
    _crossed_swords(canvas, cx, crest_y)


def divider(canvas, page, pages=2):
    """Pillar, page pips centred on the third slot row, and the page button."""
    x0, _, x1, _ = layout.DIVIDER
    cx = (x0 + x1) // 2
    _pillar(canvas, layout.ARROW[1] - 4)
    pip_y = art(cell(4, 2))[1] + 4
    plate = (x0 + 2, pip_y - 12, x1 - 2, pip_y + 36)
    frame(canvas, plate, [(DARK, DARK), (col("iron", 4), col("iron", 1))])
    canvas.rect((plate[0] + 2, plate[1] + 2, plate[2] - 2, plate[3] - 2), col("iron", 1))
    for index in range(pages):
        gem(canvas, cx, pip_y + index * 24, 8 if index == page else 5,
            "gold" if index == page else "steel", lit=index == page)
    arrow_button(canvas, forward=page < pages - 1)


def arrow_button(canvas, forward):
    """The page button fills slots 40 and 49."""
    x0, y0, x1, y1 = layout.ARROW
    frame(canvas, (x0 + 1, y0, x1 - 1, y1), [
        (DARK, DARK), (DARK, DARK),
        (col("gold", 5), col("gold", 1)), (col("gold", 4), col("gold", 1)),
        (col("gold", 4), col("gold", 2))])
    face = (x0 + 6, y0 + 5, x1 - 6, y1 - 5)
    canvas.rect(face, col("gold", 3))
    canvas.rect((face[0], (y0 + y1) // 2, face[2], face[3]), col("gold", 2))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # block arrow with 45 degree head, described pointing right
    shape = [(-10, -6), (-1, -6), (-1, -14), (1, -14), (11, -1), (11, 1), (1, 14), (-1, 14), (-1, 6), (-10, 6)]
    sign = 1 if forward else -1
    points = [(cx + sign * x, cy + y) for x, y in shape]
    mask = poly_mask(points, canvas.size)
    backing = dilate(dilate(mask))
    canvas.mask(backing | shift(backing, 0, 2), DARK)
    canvas.mask(mask, col("steel", 6))
    lower = mask.copy()
    lower[:cy] = False
    canvas.mask(lower, col("steel", 5))


def _button(canvas, rect, ramp, face, text, letters, icon, icon_colour):
    """A raised button filling `rect`: an icon over a word, so it never relies on colour alone."""
    x0, y0, x1, y1 = rect
    frame(canvas, (x0 + 2, y0 + 2, x1 - 2, y1 - 2), [
        (DARK, DARK), (DARK, DARK),
        (col(ramp, face + 2), col(ramp, face - 2)), (col(ramp, face + 1), col(ramp, face - 2)),
        (col(ramp, face + 1), col(ramp, face - 1))])
    inner = (x0 + 7, y0 + 7, x1 - 7, y1 - 7)
    canvas.rect(inner, col(ramp, face))
    canvas.rect((inner[0], (y0 + y1) // 2 + 4, inner[2], inner[3]), col(ramp, face - 1))
    cx = (x0 + x1) // 2
    mask = np.zeros(canvas.px.shape[:2], bool)
    for dy, row in enumerate(icon):
        for dx, pixel in enumerate(row):
            if pixel == "#":
                left, top = cx - len(row) * 3 // 2 + dx * 3, y0 + 13 + dy * 3
                mask[top:top + 3, left:left + 3] = True
    backing = dilate(dilate(mask))
    canvas.mask(backing | shift(backing, 0, 2), DARK)
    canvas.mask(mask, col(*icon_colour))
    canvas.mask(mask & ~shift(mask, 0, 1), col("steel", 6))
    lettering.draw(canvas, text, cx, y1 - 28, letters, ("iron", 0))


# button icons in 3 px blocks
CHECK = ["........##", ".......###", "......###.", "##...###..", "###.###...", ".#####....", "..###.....",
         "...#......"]
BACK_ARROW = ["....#.....", "...##.....", "..###.....", ".#########", "##########", ".#########", "..###.....",
              "...##.....", "....#....."]


def confirm_column(canvas, ramp):
    """The right side of a confirm screen: the warning note, Confirm, Back and a class-coloured seal."""
    x0, x1 = layout.RIGHT_PANEL[0], layout.panel_frame_rect(layout.RIGHT_PANEL)[2]
    _pillar(canvas, layout.DIVIDER[3] - 4)

    note_y0, note_y1 = art(cell(5, 0))[1], art(cell(5, 0))[3]
    frame(canvas, (x0, note_y0 + 1, x1, note_y1 - 2), [
        (DARK, DARK), (DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((x0 + 3, note_y0 + 4, x1 - 3, note_y1 - 5), col("parchment", 2))
    middle = (x0 + x1) // 2
    lettering.small(canvas, "THIS CHOICE", middle, note_y0 + 6, col("leather", 0))
    lettering.small(canvas, "IS FINAL", middle, note_y0 + 19, col("crimson", 1))

    # each button covers its two slot rows (the contract's click area); like a panel frame, it also
    # reaches over the outer edge, and its own 2 px inset lines its sides up with the note
    confirm, back = ((x0 - 2, art(cell(5, top))[1], x1 + 2, art(cell(5, top + 1))[3]) for top in (1, 3))
    _button(canvas, confirm, "gold", 3, "CONFIRM", (("gold", 5), ("gold", 4), ("steel", 6)), CHECK, ("steel", 6))
    _button(canvas, back, "iron", 3, "BACK", (("steel", 6), ("steel", 5), ("steel", 6)), BACK_ARROW, ("steel", 5))

    seal_y0, seal_y1 = art(cell(5, 5))[1], art(cell(5, 5))[3]
    frame(canvas, (x0, seal_y0, x1, seal_y1), [(DARK, DARK), (DARK, DARK), (col("iron", 4), col("iron", 1))])
    canvas.rect((x0 + 3, seal_y0 + 3, x1 - 3, seal_y1 - 3), col("iron", 1))
    centre_y = (seal_y0 + seal_y1) // 2
    for direction in (-1, 1):
        rule = sorted((middle + direction * 18, middle + direction * 62))
        canvas.rect((rule[0], centre_y - 1, rule[1], centre_y), col(ramp, 3))
        canvas.rect((rule[0], centre_y, rule[1], centre_y + 1), col(ramp, 1))
        gem(canvas, middle + direction * 64, centre_y, 3)
    gem(canvas, middle, centre_y, 10, ramp)


def inventory(canvas):
    """Calm recessed cells under the player's own items, and a light plate behind the vanilla label."""
    top = layout.GRID[3]
    width = layout.CANVAS[0]
    canvas.rect((7, top, width - 7, top + 2), DARK)
    canvas.rect((7, top + 2, width - 7, top + 3), col("gold", 2))
    canvas.rect((7, top + 3, width - 7, top + 4), DARK)

    px0, py0, px1, py1 = layout.INVENTORY_PLATE
    frame(canvas, (px0, py0 + 1, px1, py1), [(DARK, DARK), (col("parchment", 3), col("parchment", 0))])
    canvas.rect((px0 + 2, py0 + 3, px1 - 2, py1 - 2), col("parchment", 2))
    gem(canvas, px1 - 8, (py0 + py1) // 2 + 1, 4)
    # a thin rule carries the line of the plate to the right edge
    rule_y = (py0 + py1) // 2
    canvas.rect((px1 + 5, rule_y, width - 18, rule_y + 1), DARK)
    canvas.rect((px1 + 5, rule_y + 1, width - 18, rule_y + 2), col("iron", 4))
    gem(canvas, width - 16, rule_y + 1, 3)

    for row in range(4):
        for column in range(9):
            x0, y0, x1, y1 = art(player_cell(column, row))
            frame(canvas, (x0, y0, x1, y1), [
                (col("iron", 2), col("iron", 2)),
                (DARK, col("iron", 4)), (col("iron", 1), col("iron", 3))])
            canvas.rect((x0 + 3, y0 + 3, x1 - 3, y1 - 3), col("iron", 3))
    for x, dx in ((4, 1), (width - 4, -1)):
        corner_bracket(canvas, x, layout.VANILLA_H * layout.DENSITY - 4, dx, -1, 9)
