"""Mage sigils: Blink, then Pyromancer, Frostweaver and Lifebinder, and the three tab sigils."""
from .iconkit import apart, arc, box, cut, diamond, disc, mirrored, poly, stroke, union


def _flame(cx, top, width, height):
    """A leaning three-tongued flame in a box `width` x `height`."""
    def at(*points):
        return poly(*[(cx + x * width / 2, top + y * height) for x, y in points])

    return at((0.1, 0), (0.45, 0.28), (0.55, 0.45), (0.95, 0.25), (1, 0.65), (0.65, 0.93), (0, 1),
              (-0.65, 0.93), (-1, 0.65), (-0.85, 0.3), (-0.45, 0.5), (-0.4, 0.28))


def blink():
    """Gone from here, standing there: a broken after-image and a bright arrival star."""
    arrival = poly((16.5, 0.5), (18.5, 6), (23.5, 8), (18.5, 10), (16.5, 15.5), (14.5, 10), (9.5, 8),
                   (14.5, 6))
    ghost = cut(arc(7, 17, 6.5, 3.4), box(5.8, 8, 8.2, 26), box(-2, 15.8, 16, 18.2))
    jump = union(box(13.5, 17, 17, 20), box(18.5, 13.5, 22, 16.5))
    return union(arrival, ghost, jump)


def fireball():
    """A burning orb flying right with three tails."""
    orb = cut(disc(16, 12, 7.5), disc(17.5, 12, 3))
    core = diamond(17.5, 12, 1.6, 1.8)
    tails = union(poly((12, 4.5), (1, 3), (10, 9)), poly((10, 9), (0.5, 12), (10, 15)),
                  poly((10, 15), (1, 21), (12, 19.5)))
    return union(apart(orb, tails), core)


def kindling():
    """A young flame over two crossed sticks."""
    sticks = union(stroke(3.4, (2, 16), (22, 22)), stroke(3.4, (22, 16), (2, 22)))
    return apart(_flame(12, 1, 12, 15), sticks)


def inner_heat():
    """A heart of fire held inside a diamond."""
    outer = cut(diamond(12, 12, 11.5, 11.5), diamond(12, 12, 8, 8))
    return union(outer, _flame(12, 6, 8, 12))


def flame_wave():
    """Three tongues of fire riding one rolling front, rising to the right."""
    front = poly((1, 23), (1, 18), (3, 12), (6, 17), (8, 15), (11, 6), (14, 14), (16, 11), (21, 1), (23, 12),
                 (23, 23))
    swell = stroke(2, (0, 22), (7, 19.5), (13, 20.5), (24, 16))
    return cut(front, swell)


def ash_siphon():
    """Motes of ash drawn down into a cupped vessel."""
    cup = poly((3, 12), (21, 12), (18, 18), (14, 19), (14, 21), (18, 23), (6, 23), (10, 21), (10, 19), (6, 18))
    hollow = box(7, 12, 17, 14.5)
    motes = union(diamond(12, 7, 3, 3.6), diamond(5, 4, 2.4, 2.8), diamond(19, 4, 2.4, 2.8),
                  box(10.8, 0, 13.2, 2.2))
    return union(cut(cup, hollow), motes)


def meteor():
    """A falling rock with burning trails, about to strike the ground."""
    rock = poly((5, 10), (10, 8), (15, 10), (16, 15), (13, 19), (7, 19), (4, 15))
    pit = union(box(8, 12, 10.5, 14.5), box(12, 15, 14, 17))
    trails = union(stroke(3, (12, 8), (19, 1)), stroke(3, (16, 11), (23, 4)), stroke(2.4, (17, 16), (23, 10)),
                   stroke(2.4, (6, 7.5), (12, 1.5)))
    ground = union(box(1, 21, 8, 23.5), box(11, 21, 19, 23.5))
    return union(cut(rock, pit), trails, ground)


def ice_lance():
    """A long spindle of ice flying up and right, trailing two cold streaks."""
    lance = poly((23.8, 0.2), (18, 14), (8, 21), (3, 21), (3, 16), (10, 6))
    ridge = stroke(1.3, (5, 19), (21, 3))
    streaks = union(stroke(2.6, (1, 10.5), (6.5, 5)), stroke(2.6, (13.5, 23), (19, 17.5)))
    return union(cut(lance, ridge), streaks)


def chill_touch():
    """An open hand."""
    palm = poly((6, 11), (19, 11), (19, 18), (16, 23), (8, 23), (5, 19))
    fingers = union(box(6, 3, 8.6, 12), box(9.8, 1, 12.4, 12), box(13.6, 2, 16.2, 12), box(17.4, 5, 20, 12))
    thumb = stroke(3.2, (6.5, 18), (1.8, 11.5))
    frost = diamond(12.5, 17, 3, 3.5)
    return cut(union(palm, fingers, thumb), frost)


def frost_armor():
    """A breastplate hung with icicles."""
    chest = poly((2, 3), (8, 1), (10, 4), (14, 4), (16, 1), (22, 3), (19, 8), (20, 15), (4, 15), (5, 8))
    keel = box(11.2, 7, 12.8, 15)
    icicles = union(*(poly((x, 17), (x + 4, 17), (x + 2, y)) for x, y in ((4, 22), (10, 23.5), (16, 22))))
    return union(cut(chest, keel), icicles)


def frost_nova():
    """A crown of ice spikes bursting up out of the ground."""
    spikes = union(poly((9.5, 19), (12, 1), (14.5, 19)), poly((5, 19), (3.5, 6), (10, 19)),
                   poly((14, 19), (20.5, 6), (19, 19)), poly((1, 20), (0.5, 12), (6, 20)),
                   poly((18, 20), (23.5, 12), (23, 20)))
    return union(spikes, box(1, 19.5, 23, 23))


def shatter():
    """A crystal broken into four pieces that drift apart."""
    crystal = diamond(12, 12, 11, 12)
    breaks = union(stroke(2.2, (9, 0), (13, 8), (10, 13), (14, 24)), stroke(2.2, (0, 14), (10, 12.5)),
                   stroke(2.2, (12, 8.5), (24, 10)))
    return cut(crystal, breaks)


def blizzard():
    """A heavy cloud driving slanted sleet."""
    cloud = union(disc(7, 8, 5), disc(13.5, 6, 5.5), disc(18, 9, 4.5), box(4, 8, 20, 13))
    sleet = union(stroke(2.6, (8, 15.5), (4.5, 20)), stroke(2.6, (14, 15.5), (10.5, 20)),
                  stroke(2.6, (20, 15.5), (16.5, 20)), box(1, 21, 4, 23.5), box(8, 21, 11, 23.5),
                  box(14, 21, 17, 23.5))
    return union(cloud, sleet)


def mending_light():
    """A healing cross shedding four sparks."""
    cross = union(box(9, 3, 15, 21), box(3, 9, 21, 15))
    sparks = union(*(diamond(x, y, 3, 3) for x in (3.5, 20.5) for y in (3.5, 20.5)))
    return apart(cross, sparks)


def gentle_soul():
    """A heart."""
    heart = union(disc(7, 8.5, 6), disc(17, 8.5, 6), poly((1.4, 11), (22.6, 11), (12, 23)))
    return cut(heart, stroke(2, (5, 10), (5.5, 7), (8.5, 5.5)))


def radiance():
    """Dawn: a half sun on the horizon with short straight rays."""
    sun = arc(12, 18, 8, 0, 180, 360)
    rays = union(stroke(2.8, (12, 1), (12, 7)), stroke(2.8, (2, 6), (6, 10.5)), stroke(2.8, (22, 6), (18, 10.5)),
                 box(0, 13, 2.5, 16), box(21.5, 13, 24, 16))
    return union(sun, rays, box(1, 20, 23, 23))


def sanctuary():
    """A sheltering dome over a small cross."""
    dome = arc(12, 14, 11.5, 8, 180, 360)
    walls = union(box(0.5, 14, 4, 20), box(20, 14, 23.5, 20), box(0.5, 20, 23.5, 23))
    cross = union(box(10.5, 9, 13.5, 18), box(7.5, 12, 16.5, 15))
    return union(dome, walls, cross)


def smite():
    """A pillar of judgement falling and bursting on the ground."""
    beam = poly((7, 0), (17, 0), (15, 15), (12, 18), (9, 15))
    seam = box(11.2, 0, 12.8, 11)
    burst = union(poly((1, 13), (8, 19), (6, 21)), poly((23, 13), (16, 19), (18, 21)), box(2, 20.5, 22, 23.5))
    return union(cut(beam, seam), burst)


def sunburst():
    """A light bursting outward: four long points and four short ones around an open centre."""
    long = poly((12, 0), (15.5, 8.5), (24, 12), (15.5, 15.5), (12, 24), (8.5, 15.5), (0, 12), (8.5, 8.5))
    short = union(*(diamond(x, y, 3.2, 3.2) for x in (4.5, 19.5) for y in (4.5, 19.5)))
    return union(cut(long, diamond(12, 12, 4.5, 4.5)), diamond(12, 12, 2, 2), short)


def tab_pyromancer():
    """One tall flame with a hollow heart."""
    return cut(_flame(12, 0.5, 19, 22.5), _flame(11.5, 11, 7, 10))


def tab_frostweaver():
    """A six-armed snowflake."""
    arms = union(stroke(2.6, (12, 0.5), (12, 23.5)), stroke(2.6, (2, 6.25), (22, 17.75)),
                 stroke(2.6, (2, 17.75), (22, 6.25)))
    barbs = union(stroke(2, (8, 1.5), (12, 5.5), (16, 1.5)), stroke(2, (8, 22.5), (12, 18.5), (16, 22.5)))
    return union(arms, barbs)


def tab_lifebinder():
    """Two leaves on a stem that curls at its foot."""
    leaf = poly((11, 14), (3, 13), (1, 6), (1, 2), (8, 3), (12, 10))
    pair = mirrored(cut(leaf, stroke(1.4, (4, 5), (10.5, 12.5))))
    stem = union(box(10.5, 10, 13.5, 20), arc(9, 19.5, 4.5, 1.5, 0, 200))
    return union(pair, stem)


ICONS = {function.__name__: function() for function in (
    blink, fireball, kindling, inner_heat, flame_wave, ash_siphon, meteor,
    ice_lance, chill_touch, frost_armor, frost_nova, shatter, blizzard,
    mending_light, gentle_soul, radiance, sanctuary, smite, sunburst,
    tab_pyromancer, tab_frostweaver, tab_lifebinder)}
