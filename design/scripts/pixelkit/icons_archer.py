"""Archer sigils: Vault, then Marksman, Skirmisher and Hunter, and the three tab sigils."""
from .iconkit import apart, arc, arrow, box, cut, diamond, disc, head, mirrored, poly, stroke, union


def _fletch(x, y):
    """Fletching for an arrow that flies up and to the right, with its nock at (x, y)."""
    return union(stroke(2.6, (x, y - 5), (x + 3, y - 2)), stroke(2.6, (x + 2, y), (x + 5, y)),
                 stroke(2.6, (x, y - 3), (x, y - 6)), stroke(2.6, (x + 3, y), (x + 6, y)))


def vault():
    """A backward leap: a high arc coming down to the left, thrown off two spring chevrons."""
    leap = union(arc(12.5, 12, 11, 7.5, 180, 350), head((3.2, 20), (-0.1, 1), 9, 10))
    spring = union(stroke(2.8, (13, 17), (18, 13), (23, 17)), stroke(2.8, (13, 22.5), (18, 18.5), (23, 22.5)))
    return union(leap, spring)


def power_shot():
    """One heavy arrow with a broad head."""
    return union(head((23, 1), (1, -1), 13, 12), stroke(4, (5, 19), (16, 8)),
                 stroke(2.8, (6, 18), (1, 18)), stroke(2.8, (6, 18), (6, 23)),
                 stroke(2.8, (10, 14), (5, 14)), stroke(2.8, (10, 14), (10, 19)))


def eagle_eye():
    """An eagle's head in profile with a hooked beak."""
    skull = poly((1, 23), (2, 11), (6, 4), (12, 2), (17, 4), (18, 8), (22, 10), (23, 13), (22, 18), (20, 15),
                 (16, 14), (13, 17), (13, 23))
    eye = diamond(11.5, 8.5, 3.6, 3)
    mouth = stroke(1.4, (13.5, 11.5), (21, 12))
    feather = union(stroke(1.4, (4, 17), (9, 14)), stroke(1.4, (4, 22), (10, 18)))
    return union(cut(skull, eye, mouth, feather), box(10.5, 7.5, 12.5, 9.5))


def steady_aim():
    """A still sight: a ring broken into four, with four ticks and a centre."""
    ring = cut(arc(12, 12, 9, 6), box(10.5, 0, 13.5, 24), box(0, 10.5, 24, 13.5))
    ticks = union(box(10.5, 0, 13.5, 7), box(10.5, 17, 13.5, 24), box(0, 10.5, 7, 13.5), box(17, 10.5, 24, 13.5))
    return union(ring, ticks, box(10.5, 10.5, 13.5, 13.5))


def piercing_shot():
    """An arrow driven through two upright plates."""
    shaft = union(box(0, 10.5, 18, 13.5), head((24, 12), (1, 0), 7, 10),
                  stroke(2.4, (3.5, 12), (0.5, 8)), stroke(2.4, (3.5, 12), (0.5, 16)))
    plates = union(box(6, 2, 10, 22), box(13, 2, 17, 22))
    return apart(shaft, plates)


def weak_spot():
    """An armour plate with a jagged break and a mark where it gives."""
    plate = poly((3, 2), (21, 2), (22, 12), (18, 19), (12, 23), (6, 19), (2, 12))
    split = stroke(2.2, (15, 1), (10, 8), (15, 12), (9, 17), (12, 24))
    hole = diamond(12.5, 11.5, 4, 4.5)
    return union(cut(plate, split, hole), diamond(12.5, 11.5, 1.8, 2))


def hunters_mark():
    """Four sight corners closing on a prey diamond."""
    corner = union(box(1, 1, 10, 4.5), box(1, 1, 4.5, 10))
    corners = mirrored(corner) | mirrored(corner)[::-1, :]
    return union(corners, diamond(12, 12, 5.5, 6.5))


def volley():
    """Three arrows fanning upward from one hand."""
    return union(arrow((12, 22), (12, 1), 2.8, 7, 7.5), arrow((10.5, 22), (2, 5), 2.8, 7, 7.5),
                 arrow((13.5, 22), (22, 5), 2.8, 7, 7.5), box(7, 20, 17, 23))


def fleet_foot():
    """A boot with a wing."""
    boot = poly((11, 4), (18, 4), (18, 14), (23, 17), (23, 22), (11, 22))
    sole = box(11, 19, 23, 20.2)
    wing = union(stroke(3, (9, 7), (1, 3)), stroke(3, (9, 12), (1, 9)), stroke(3, (9, 17), (3, 15)))
    return union(cut(boot, sole), wing)


def momentum():
    """Three arrowheads, each larger than the one it follows."""
    return union(stroke(2.8, (9, 23), (12, 20), (15, 23)), stroke(3.2, (5.5, 18.5), (12, 12), (18.5, 18.5)),
                 head((12, 0.5), (0, -1), 12, 22) & ~head((12, 7.5), (0, -1), 8, 14))


def rapid_fire():
    """Three level arrows, staggered, one after another."""
    def bolt(x, y):
        return union(box(x, y - 1.5, x + 12, y + 1.5), head((x + 17, y), (1, 0), 7, 7),
                     stroke(2, (x + 3, y), (x + 0.5, y - 3)), stroke(2, (x + 3, y), (x + 0.5, y + 3)))

    return union(bolt(1, 4), bolt(6, 12), bolt(1, 20))


def light_step():
    """A single feather."""
    vane = poly((21, 1), (23, 6), (21, 12), (15, 17), (7, 19), (5, 17), (7, 10), (12, 4))
    quill = stroke(1.5, (4, 20), (20, 4))
    notches = union(stroke(1.6, (6, 12), (12, 12)), stroke(1.6, (13, 18), (13, 13)))
    return union(cut(vane, quill, notches), stroke(2.8, (1.5, 22.5), (7, 17)))


def tumble():
    """The path of a roll: along the ground, once over, and out forward."""
    path = stroke(3.2, (0.5, 20.5), (9, 20), (14, 17), (16, 11.5), (13.5, 6), (8.5, 5.5), (5.5, 10), (7, 15.5),
                  (12, 19.5), (17, 20.5))
    return union(path, head((24, 20.5), (1, 0), 8, 9))


def flame_arrow():
    """An arrow whose head is wrapped in flame."""
    flame = poly((23, 1), (22, 8), (23.5, 12), (20, 16), (14, 15), (10, 11), (10, 7), (13, 8), (13, 3),
                 (17, 5))
    core = diamond(16.8, 9.2, 2.8, 3.2)
    shaft = union(stroke(3, (4, 20), (12, 12)), _fletch(1, 23))
    return union(cut(flame, core), shaft)


def tracker():
    """A paw print."""
    pad = poly((12, 10), (17, 13), (19, 18), (17, 22), (13.5, 20.5), (10.5, 20.5), (7, 22), (5, 18), (7, 13))
    toes = union(disc(3.5, 11, 2.8, 3.4), disc(8.5, 4.5, 2.8, 3.4), disc(15.5, 4.5, 2.8, 3.4),
                 disc(20.5, 11, 2.8, 3.4))
    return union(pad, toes)


def survivalist():
    """A sprout: two leaves on a stem, growing out of the ground."""
    leaf = poly((11, 15), (4, 13), (1, 7), (1, 4), (7, 5), (11, 10))
    veins = stroke(1.3, (3.5, 7), (10, 13))
    pair = mirrored(cut(leaf, veins))
    return union(pair, box(10.5, 8, 13.5, 20), box(3, 19.5, 21, 22.5))


def wolf_companion():
    """A wolf's face: tall ears, narrow eyes, a long muzzle."""
    face = poly((2, 1), (8, 6), (16, 6), (22, 1), (21, 10), (23, 15), (17, 16), (15, 23), (9, 23), (7, 16),
                (1, 15), (3, 10))
    eyes = mirrored(poly((5, 10), (10, 13), (10, 14.5), (6, 13.5)))
    muzzle = mirrored(stroke(1.3, (9.5, 15), (10.5, 20)))
    nose = box(10, 19.5, 14, 21.5)
    return union(cut(face, eyes, muzzle), nose)


def barbed_heads():
    """A broad barbed arrowhead standing point up."""
    point = poly((12, 0.5), (22, 14), (22, 18), (16, 13), (14, 13), (14, 18), (19, 23), (14, 22), (12, 20),
                 (10, 22), (5, 23), (10, 18), (10, 13), (8, 13), (2, 18), (2, 14))
    ridge = box(11.3, 4, 12.7, 12)
    return cut(point, ridge)


def frost_arrow():
    """An arrow that ends in an ice star."""
    cx, cy = 15.5, 8.5
    star = union(stroke(2.4, (cx, 0.5), (cx, 16.5)), stroke(2.4, (cx - 8, cy), (cx + 8, cy)),
                 stroke(2.4, (cx - 5.5, cy - 5.5), (cx + 5.5, cy + 5.5)),
                 stroke(2.4, (cx - 5.5, cy + 5.5), (cx + 5.5, cy - 5.5)), diamond(cx, cy, 4, 4))
    return union(star, stroke(3, (3, 21), (10, 14)), _fletch(1, 23))


def tab_marksman():
    """One upright arrow through a bow's grip line."""
    bow = arc(2, 12, 17, 13.6, 310, 50)
    string = box(12.2, 0.5, 14, 23.5)
    return union(bow, string, arrow((1, 12), (23.5, 12), 3, 7, 8))


def tab_skirmisher():
    """Two crossed arrows."""
    return union(arrow((3, 21), (22, 2), 2.8, 8, 9), arrow((21, 21), (2, 2), 2.8, 8, 9))


def tab_hunter():
    """A pair of antlers over a narrow skull."""
    antler = union(stroke(3, (10, 14), (4, 10), (3, 2)), stroke(2.6, (5, 10), (0.5, 7)),
                   stroke(2.6, (6, 11), (9, 4)))
    skull = poly((8, 12), (16, 12), (15, 18), (13.5, 23), (10.5, 23), (9, 18))
    eyes = union(box(9.5, 14, 11.5, 17), box(12.5, 14, 14.5, 17))
    return union(mirrored(antler), cut(skull, eyes))


ICONS = {function.__name__: function() for function in (
    vault, power_shot, eagle_eye, steady_aim, piercing_shot, weak_spot, hunters_mark,
    volley, fleet_foot, momentum, rapid_fire, light_step, tumble,
    flame_arrow, tracker, survivalist, wolf_companion, barbed_heads, frost_arrow,
    tab_marksman, tab_skirmisher, tab_hunter)}
