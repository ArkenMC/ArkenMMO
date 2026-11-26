"""Captain sigils: Rallying Strike, then Vanguard, Standard-Bearer and Warchanter, and the tab sigils."""
from .iconkit import apart, box, cut, diamond, disc, head, mirrored, poly, stroke, union


def rallying_strike():
    """A raised sword with rallying chevrons climbing on both sides."""
    sword = union(poly((10, 4), (12, 0.5), (14, 4), (14, 16), (10, 16)), box(7, 16, 17, 19),
                  box(10.5, 19, 13.5, 21.5), box(9.5, 21, 14.5, 24))
    chevrons = union(stroke(2.6, (1, 11), (4, 7), (7, 11)), stroke(2.6, (1, 17), (4, 13), (7, 17)))
    return union(sword, mirrored(chevrons))


def quarry_mark():
    """A heavy marker pointing down at a ringed spot on the ground."""
    marker = poly((4, 1), (20, 1), (20, 5), (12, 15), (4, 5))
    notch = poly((9, 1), (15, 1), (12, 6))
    ring = cut(disc(12, 19, 11, 4.8), disc(12, 19, 6.8, 2))
    return apart(cut(marker, notch), cut(ring, box(0, 0, 24, 16)))


def hardened_resolve():
    """A clenched fist, knuckles forward."""
    knuckles = union(*(box(x, 3, x + 4, 11) | disc(x + 2, 3.5, 2, 2) for x in (3, 7.8, 12.6, 17.4)))
    palm = poly((3, 12), (21.4, 12), (21, 17), (17, 20), (17, 24), (7, 24), (7, 20), (3, 17))
    thumb = poly((3, 13), (15, 13), (17, 15), (15, 17), (6, 17))
    return union(knuckles, cut(palm, stroke(1.4, (3, 12.3), (16, 12.3), (18, 15), (16, 17.8), (5, 17.8))), thumb
                 & ~box(0, 0, 24, 13.2))


def lead_from_the_front():
    """A wedge formation: one great point ahead, two following."""
    return union(head((12, 0.5), (0, -1), 13, 13), head((5.5, 11), (0, -1), 11, 10),
                 head((18.5, 11), (0, -1), 11, 10), box(10.5, 12, 13.5, 20))


def press_the_attack():
    """Two blades thrusting side by side."""
    def blade(x, y):
        return union(head((x + 14, y), (1, -1), 8, 6.5), stroke(3, (x + 3, y + 11), (x + 10, y + 4)),
                     stroke(2.6, (x + 2, y + 7), (x + 7, y + 12)), stroke(2.6, (x + 3, y + 11), (x, y + 14)))

    return union(blade(0.5, 1), blade(8.5, 9))


def gallant_example():
    """A crown."""
    crown = poly((2, 4), (7, 11), (12, 2), (17, 11), (22, 4), (21, 17), (3, 17))
    band = box(3, 19, 21, 23)
    gems = union(box(7, 13, 9, 15.5), box(15, 13, 17, 15.5), diamond(12, 12, 2, 2.6))
    return union(cut(crown, gems), band)


def scattering_shout():
    """Four arrowheads flung outward from one cry."""
    out = union(head((12, 0), (0, -1), 6.5, 11), head((12, 24), (0, 1), 6.5, 11),
                head((0, 12), (-1, 0), 6.5, 11), head((24, 12), (1, 0), 6.5, 11))
    return union(out, diamond(12, 12, 3.5, 3.5))


def plant_standard():
    """A war banner driven into the ground."""
    pole = union(box(4, 2, 7, 22), diamond(5.5, 2.5, 2.5, 2.5))
    flag = poly((7, 3), (22, 3), (18, 8), (22, 13), (7, 13))
    ground = union(box(0.5, 18.5, 3, 21), box(9, 18.5, 12, 21), box(1, 21.5, 20, 24))
    return union(pole, cut(flag, diamond(12.5, 8, 2.5, 3)), ground)


def tall_colours():
    """A tall hanging gonfalon with a swallowtail."""
    bar = union(box(2, 2, 22, 5), diamond(2.5, 3.5, 2.5, 3), diamond(21.5, 3.5, 2.5, 3))
    cloth = poly((5, 6.5), (19, 6.5), (19, 23.5), (12, 18), (5, 23.5))
    stripe = union(box(5, 10, 19, 11.6), box(11.2, 12, 12.8, 18))
    return union(bar, cut(cloth, stripe))


def close_ranks():
    """A shield wall: three shields overlapping, the middle one in front."""
    def shield(cx, top, half):
        return poly((cx - half, top), (cx + half, top), (cx + half, top + 9), (cx, top + 17),
                    (cx - half, top + 9))

    middle = cut(shield(12, 4, 5.5), box(11.2, 7, 12.8, 17))
    return apart(middle, union(shield(4.5, 2, 4.5), shield(19.5, 2, 4.5)))


def call_herald():
    """A long herald's trumpet with a hanging pennant."""
    tube = stroke(3, (1.5, 8), (16, 8))
    bell = poly((14, 6.5), (23, 1), (23, 15), (14, 9.5))
    mouth = box(0.5, 5, 3, 11)
    pennant = poly((5, 11), (15, 11), (15, 22), (10, 18), (5, 22))
    return union(tube, bell, mouth, cut(pennant, diamond(10, 14.5, 2.2, 2.4)))


def steadfast_company():
    """A closed great helm with a plume."""
    dome = union(disc(12, 11, 8, 7), box(4, 11, 20, 20), poly((4, 20), (20, 20), (17, 23.5), (7, 23.5)))
    slit = box(6, 11.5, 18, 14)
    breath = union(box(11.2, 14, 12.8, 21), box(15, 17, 16.6, 20))
    plume = poly((10, 4), (14, 0.5), (23, 2), (23.5, 7), (19, 5), (14, 5.5))
    return union(cut(dome, slit, breath), plume)


def sworn_bond():
    """Two links locked through each other."""
    def link(cx, cy):
        return cut(diamond(cx, cy, 8.6, 8.6), diamond(cx, cy, 4.4, 4.4))

    first, second = link(8.6, 8.6), link(15.4, 15.4)
    return apart(first & ~box(12, 12, 24, 24), second) | (first & box(12, 12, 24, 24) & ~second)


def war_ballad():
    """A war lute."""
    body = union(disc(8.5, 16, 7.5, 7), disc(11.5, 13, 4.5))
    hole = diamond(8.5, 15.5, 2.8, 2.8)
    bridge = stroke(1.4, (3.5, 17.5), (7, 21))
    neck = stroke(3, (11, 13), (20, 4))
    pegs = union(stroke(4.4, (19, 5), (23, 1)), box(15.5, 1, 18, 3.5), box(20.5, 6, 23, 8.5))
    return union(cut(body, hole, bridge), neck, pegs)


def stirring_melody():
    """Two beamed notes."""
    heads = union(disc(5.5, 19, 4.5, 3.8), disc(17.5, 16, 4.5, 3.8))
    stems = union(box(7.2, 5, 10, 19), box(19.2, 2, 22, 16))
    beam = poly((7.2, 5), (22, 1), (22, 6.5), (7.2, 10.5))
    return union(heads, stems, beam)


def long_refrain():
    """An hourglass: the verses last longer."""
    frame_bars = union(box(3, 1, 21, 4), box(3, 20, 21, 23))
    glass = poly((5, 4), (19, 4), (19, 6), (13.5, 11), (13.5, 13), (19, 18), (19, 20), (5, 20), (5, 18),
                 (10.5, 13), (10.5, 11), (5, 6))
    air = union(poly((8, 6), (16, 6), (12, 9.5)), poly((12, 13), (15.5, 16.5), (8.5, 16.5)))
    return union(frame_bars, cut(glass, air))


def anthem_of_courage():
    """A harp."""
    pillar = box(3, 3, 6.5, 22)
    neck = stroke(3.4, (4, 4), (10, 6), (15, 3), (21, 2.5))
    sound = stroke(4, (21, 3), (6, 21))
    strings = union(box(9, 6, 10.6, 17), box(12.6, 5.5, 14.2, 13), box(16.2, 4, 17.8, 9))
    return union(pillar, neck, sound, strings, box(2, 20.5, 10, 23))


def clear_voice():
    """A ringing bell."""
    bell = union(disc(12, 10, 6.5, 6), poly((5.5, 10), (18.5, 10), (19.5, 15), (22, 18), (2, 18), (4.5, 15)))
    crown = box(10, 1, 14, 5)
    clapper = disc(12, 21, 3, 2.6)
    shine = stroke(1.6, (8.5, 14), (9, 9.5), (11, 7.5))
    return union(cut(bell, shine), crown, clapper)


def coda():
    """The final stroke: two beaters falling on a war drum."""
    sticks = union(stroke(2.8, (2, 1), (9, 8)), stroke(2.8, (22, 1), (15, 8)), disc(9.5, 8.5, 2.2),
                   disc(14.5, 8.5, 2.2))
    drum = union(disc(12, 14, 10.5, 3.2), box(1.5, 14, 22.5, 20), disc(12, 20, 10.5, 3.4))
    lacing = stroke(1.6, (3.5, 17), (7.5, 21.5), (12, 17.5), (16.5, 21.5), (20.5, 17))
    return apart(sticks, cut(drum, box(1.5, 15.6, 22.5, 16.8), lacing))


def tab_vanguard():
    """Two crossed spears."""
    def spear(tip, tail, direction):
        return union(head(tip, direction, 9, 8), stroke(2.8, tail, (tip[0] - direction[0] * 5,
                                                                    tip[1] - direction[1] * 5)))

    return union(spear((23, 1), (3, 22), (1, -1)), spear((1, 1), (21, 22), (-1, -1)),
                 stroke(2.6, (3, 15), (9, 21)), stroke(2.6, (21, 15), (15, 21)))


def tab_standard_bearer():
    """A pole topped with a crossbar and a long pennant."""
    pole = union(box(10.5, 1, 13.5, 24), box(5, 3.5, 19, 6))
    cloth = union(poly((3, 7), (9, 7), (9, 17), (6, 14), (3, 17)), poly((15, 7), (21, 7), (21, 17), (18, 14),
                                                                        (15, 17)))
    return union(pole, cloth, diamond(12, 2, 3, 2.5))


def tab_warchanter():
    """One great flagged note."""
    note = union(disc(8, 18.5, 6, 4.8), box(11, 1, 14.5, 19))
    flag = poly((14.5, 1), (21, 6), (22, 12), (19.5, 15), (19, 10), (14.5, 7.5))
    return union(note, flag)


ICONS = {function.__name__: function() for function in (
    rallying_strike, quarry_mark, hardened_resolve, lead_from_the_front, press_the_attack, gallant_example,
    scattering_shout, plant_standard, tall_colours, close_ranks, call_herald, steadfast_company, sworn_bond,
    war_ballad, stirring_melody, long_refrain, anthem_of_courage, clear_voice, coda,
    tab_vanguard, tab_standard_bearer, tab_warchanter)}
