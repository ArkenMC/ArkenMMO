"""Warrior sigils added for A2: the redrawn Berserker three, Guardian and Duelist."""
from .iconkit import apart, arc, box, cut, diamond, disc, grid, head, mirrored, poly, stroke, union


def whirlwind():
    """One solid, bent funnel with slanted wind cuts, a curling tail and flung debris."""
    return grid("""
        ........................
        ...##################...
        .######################.
        ########################
        ###############.....###.
        .#########.......#####..
        ..####.......########...
        ..###....##########.....
        ....#############.......
        .....#########.....##...
        ......####......#..##...
        ......##.....####.......
        .##....#########........
        .##.....######..........
        ........###.....#.......
        .........#....###.......
        .........########.......
        ..........#####.........
        ..........###...........
        ..........###...........
        ...........####...###...
        ............#########...
        .............#######....
        ........................""")


def fury():
    """A blazing rage: a three-tongued flame with two slanted eyes cut out of it."""
    flame = poly((12, 1), (15, 6), (17, 9), (21, 3), (20, 9), (23, 13), (21, 19), (16, 23), (8, 23),
                 (3, 19), (1, 13), (4, 9), (3, 3), (7, 9), (9, 6))
    eyes = mirrored(poly((5, 12), (11, 15), (11, 18), (7, 17)))
    grin = poly((9, 20), (15, 20), (13, 22), (11, 22))
    return cut(flame, eyes, grin)


def relentless():
    """A kill feeding mana: a skull below, a large mana crystal rising out of it."""
    crystal = cut(diamond(12, 6, 6.5, 6.5), box(11.2, 2.5, 12.8, 7))
    sparks = union(diamond(3.5, 9, 2.5, 3), diamond(20.5, 9, 2.5, 3))
    skull = union(disc(12, 17.5, 7.5, 5), box(8, 18, 16, 23))
    face = union(box(7, 16, 10.5, 19), box(13.5, 16, 17, 19), box(11, 21, 13, 23))
    return apart(crystal, union(cut(skull, face), sparks))


def shield_bash():
    """A shield driven forward, with three impact wedges."""
    shield = cut(poly((1, 3), (13, 3), (13, 14), (7, 22), (1, 14)), box(6, 5, 8, 17))
    return union(shield, poly((15, 8), (21, 1), (23, 5)), poly((15, 12), (23, 9), (23, 15)),
                 poly((15, 16), (23, 19), (21, 23)))


def iron_hide():
    """A heavy cuirass banded with overlapping iron lames."""
    plate = poly((1, 4), (7, 1), (9, 4), (15, 4), (17, 1), (23, 4), (20, 9), (21, 16), (18, 23), (6, 23),
                 (3, 16), (4, 9))
    lames = union(stroke(1.7, (3, 11), (12, 14), (21, 11)), stroke(1.7, (3, 16), (12, 19), (21, 16)))
    return cut(plate, lames, box(11.2, 6, 12.8, 13))


def stalwart():
    """A mountain: broad at the foot and not to be moved."""
    peaks = union(poly((0.5, 20), (9, 3), (18, 20)), poly((10, 20), (17, 7), (23.5, 20)))
    snow = stroke(1.7, (4.5, 11.5), (7, 9.5), (9, 11.5), (11, 9.5), (14, 11.5))
    seam = stroke(1.5, (13.5, 11), (18, 20))
    return union(cut(peaks, snow, seam), box(0.5, 21, 23.5, 23.5))


def challenging_shout():
    """A head in profile, mouth wide open, throwing two bars of sound."""
    face = poly((0.5, 8), (2, 3), (7, 1), (11, 3), (12, 8), (14.5, 11), (12, 12), (5, 13.5), (12, 17),
                (11, 20), (7, 21), (7, 23), (0.5, 23))
    eye = box(7, 6, 10, 8.5)
    near = stroke(2.6, (15.8, 16), (17.3, 19), (15.8, 22))
    far = stroke(2.8, (17.5, 3), (22.2, 12.5), (20.5, 22))
    return union(cut(face, eye), near, far)


def second_wind():
    """A healing cross lifted on two curling gusts."""
    cross = union(box(10, 1, 15, 13), box(6.5, 4.5, 18.5, 9.5))
    upper = union(box(3, 15, 18, 18), arc(18, 14, 4, 1, 270, 90))
    lower = union(box(6, 20, 14, 23), arc(5.5, 19.5, 3.8, 1, 90, 270))
    return union(cross, upper, lower)


def bulwark():
    """A crenellated wall block."""
    wall = union(box(2, 9, 22, 22), box(2, 3, 7, 10), box(9.5, 3, 14.5, 10), box(17, 3, 22, 10))
    mortar = union(box(2, 13, 22, 14.8), box(9, 15, 11, 18), box(15, 15, 17, 18), box(6, 19, 8, 22),
                   box(12, 19, 14, 22), box(2, 17.6, 22, 19))
    return cut(wall, mortar)


def lunge():
    """A long thrust with two trailing speed cuts."""
    blade = union(head((22, 2), (1, -1), 11, 8), stroke(3.4, (6, 18), (17, 7)), stroke(3, (3, 15), (9, 21)),
                  stroke(3, (6, 18), (2, 22)))
    return union(blade, stroke(2.4, (2, 10), (10, 2)), stroke(2.4, (14, 22), (22, 14)))


def footwork():
    """Two staggered boot soles with arches and separate heels."""
    return grid("""
        ........................
        ...............#####....
        ..............########..
        .............##########.
        .............##########.
        .............##########.
        ..............#########.
        ................#######.
        ....#####........######.
        ..########.......#####..
        .##########.............
        .##########.............
        .##########.....#####...
        .#########.....######...
        .#######.......######...
        .######.........####....
        ..#####.................
        ........................
        ........................
        ...#####................
        ...######...............
        ...######...............
        ....####................
        ........................""")


def focus():
    """An angular eye with a diamond pupil."""
    lids = poly((0.5, 12), (7, 5), (17, 5), (23.5, 12), (17, 19), (7, 19))
    white = poly((4.5, 12), (8.5, 8), (15.5, 8), (19.5, 12), (15.5, 16), (8.5, 16))
    return union(cut(lids, white), diamond(12, 12, 4, 4.5), box(11, 1, 13, 4), box(11, 20, 13, 23))


def riposte():
    """An upright blade with a hooked return stroke around one side."""
    sword = union(poly((5, 3), (7, 1), (9, 3), (9, 16), (5, 16)), box(1, 16, 13, 19), box(5, 19, 9, 23))
    back = union(arc(12, 11, 10.5, 7, 270, 70), head((10, 19.5), (-1, 0.35), 7, 9))
    return union(sword, back)


def opportunist():
    """A dagger dropping from the upper right on a turned back, shown as a half ring."""
    dagger = union(head((8, 16), (-1, 1), 11, 7.5), stroke(3, (13, 5), (19, 11)), stroke(3.2, (16, 8), (22, 2)))
    return apart(dagger, arc(11, 13, 10.5, 7.2, 60, 215))


def hamstring():
    """A tall booted leg with one long slash straight through it."""
    leg = poly((6, 1), (15, 1), (14, 9), (13, 15), (16, 18), (22, 19), (23, 23), (6, 23), (7, 15), (5, 7))
    return apart(stroke(3, (1.5, 17.5), (22.5, 5.5)), leg)


ICONS = {
    "whirlwind": whirlwind(), "fury": fury(), "relentless": relentless(),
    "shield_bash": shield_bash(), "iron_hide": iron_hide(), "stalwart": stalwart(),
    "challenging_shout": challenging_shout(), "second_wind": second_wind(), "bulwark": bulwark(),
    "lunge": lunge(), "footwork": footwork(), "focus": focus(), "riposte": riposte(),
    "opportunist": opportunist(), "hamstring": hamstring(),
}
