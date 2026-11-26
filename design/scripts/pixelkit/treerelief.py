"""The class carvings behind the tree: one dim central relief and a pair of tall margin carvings.

Each returns a page-sized mask (art px). The centre stays inside columns 3-5, rows 1-3, which hold
no stones; margins stay in columns 1 and 7. Nothing is framed like a button.
"""
import numpy as np

from .draw import dilate, poly_mask, rect_mask


def _mirror(points, axis):
    return [(2 * axis - x, y) for x, y in points]


class _Pen:
    """Small helpers bound to the page size."""

    def __init__(self, size):
        self.size = size

    def poly(self, *points):
        return poly_mask(list(points), self.size)

    def rect(self, x0, y0, x1, y1):
        return rect_mask((x0, y0, x1, y1), self.size)

    def pair(self, points, axis=176):
        return self.poly(*points) | self.poly(*_mirror(points, axis))

    def stroke(self, width, *points):
        out = np.zeros((self.size[1], self.size[0]), bool)
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            length = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
            nx, ny = -(by - ay) / length * width / 2, (bx - ax) / length * width / 2
            out |= self.poly((ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny))
        return out


def _margins(motif):
    """The same motif in both margins, at the same height."""
    return motif(68) | motif(284)


# --- Warrior: a great nasal helm over two crossed war axes, between two grave swords ------------

def warrior_relief(size):
    pen = _Pen(size)
    helm = pen.poly((176, 76), (190, 79), (201, 88), (208, 101), (210, 116), (142, 116), (144, 101),
                    (151, 88), (162, 79))
    brow = pen.poly((140, 119), (212, 119), (212, 127), (140, 127))
    cheeks = pen.pair([(142, 130), (160, 130), (163, 150), (170, 168), (156, 164), (146, 150)])
    nasal = pen.poly((171, 130), (181, 130), (180, 156), (176, 161), (172, 156))
    ridge = pen.poly((173, 80), (179, 80), (179, 116), (173, 116))
    helm_all = (helm & ~ridge) | brow | cheeks | nasal
    haft = pen.poly((120, 187), (126, 193), (232, 87), (226, 81))
    haft = haft | haft[:, ::-1]
    axes = haft | pen.pair([(222, 62), (241, 66), (252, 77), (256, 96), (244, 90), (236, 90), (232, 84),
                            (226, 78), (226, 72)])
    return helm_all | (axes & ~dilate(dilate(dilate(helm_all))))


def warrior_hollows(size):
    eyes = poly_mask([(148, 131), (169, 131), (166, 139), (152, 139)], size)
    return eyes | eyes[:, ::-1]


def warrior_margins(size):
    pen = _Pen(size)
    top, bottom = 80, 206

    def sword(cx):
        mask = (pen.poly((cx - 3, top), (cx + 3, top), (cx + 5, top + 6), (cx - 5, top + 6))
                | pen.rect(cx - 2, top + 6, cx + 2, top + 22) | pen.rect(cx - 13, top + 22, cx + 13, top + 28)
                | pen.poly((cx - 6, top + 30), (cx + 6, top + 30), (cx + 5, bottom - 16), (cx, bottom),
                           (cx - 5, bottom - 16)))
        return mask & ~pen.rect(cx - 1, top + 34, cx + 1, bottom - 24)

    return _margins(sword)


# --- Archer: an antlered stag skull before two crossed arrows, between two old firs ------------

def archer_relief(size):
    pen = _Pen(size)
    antlers = np.zeros((size[1], size[0]), bool)
    for branch in (((168, 118), (150, 108), (137, 94), (132, 76), (135, 62)),
                   ((146, 103), (128, 101), (120, 88)), ((137, 92), (148, 82), (150, 68))):
        for points in (branch, _mirror(branch, 176)):
            antlers |= pen.stroke(7, *points)
    skull = pen.poly((162, 112), (190, 112), (196, 124), (192, 138), (185, 144), (182, 166), (176, 174),
                     (170, 166), (167, 144), (160, 138), (156, 124))
    holes = archer_hollows(size) | pen.rect(175, 148, 177, 166)
    shafts = pen.stroke(4, (126, 184), (222, 128))
    shafts |= shafts[:, ::-1]
    heads = pen.pair([(236, 119), (215, 124), (223, 137)])
    flights = pen.pair([(126, 176), (136, 178), (128, 184), (122, 192), (118, 182)])
    head_all = (skull & ~holes) | antlers
    return head_all | ((shafts | heads | flights) & ~dilate(dilate(dilate(skull))))


def archer_hollows(size):
    eyes = poly_mask([(161, 123), (172, 129), (170, 135), (162, 132)], size)
    return eyes | eyes[:, ::-1]


def archer_margins(size):
    pen = _Pen(size)

    def fir(cx):
        mask = pen.rect(cx - 2, 176, cx + 2, 206)
        for top, half in ((78, 9), (100, 12), (124, 15), (150, 17)):
            mask |= pen.poly((cx, top), (cx + half, top + 30), (cx + 4, top + 25), (cx, top + 28),
                             (cx - 4, top + 25), (cx - half, top + 30))
        return mask

    return _margins(fir)


# --- Mage: a pointed archway holding a tall crystal, between two crowned staves ---------------

def mage_relief(size):
    pen = _Pen(size)
    outer = pen.poly((126, 184), (126, 116), (134, 92), (152, 74), (176, 62), (200, 74), (218, 92),
                     (226, 116), (226, 184))
    inner = pen.poly((137, 184), (137, 118), (144, 99), (158, 84), (176, 74), (194, 84), (208, 99),
                     (215, 118), (215, 184))
    joints = np.zeros((size[1], size[0]), bool)
    for y in (104, 128, 152, 174):
        joints |= pen.rect(120, y, 232, y + 2)
    arch = outer & ~inner & ~joints
    crystal = pen.poly((176, 90), (190, 116), (176, 156), (162, 116))
    facets = mage_hollows(size)
    shards = (pen.pair([(150, 118), (155, 127), (150, 138), (145, 127)])
              | pen.pair([(156, 150), (160, 156), (156, 163), (152, 156)]))
    steps = pen.rect(146, 168, 206, 173) | pen.rect(138, 177, 214, 183)
    return arch | (crystal & ~facets) | shards | steps


def mage_hollows(size):
    return poly_mask([(176, 98), (182, 116), (176, 118), (170, 116)], size)


def mage_margins(size):
    pen = _Pen(size)

    def staff(cx):
        crown = pen.poly((cx, 76), (cx + 6, 88), (cx, 100), (cx - 6, 88))
        horns = pen.stroke(4, (cx - 2, 112), (cx - 11, 102), (cx - 11, 86), (cx - 7, 80))
        horns |= pen.stroke(4, (cx + 2, 112), (cx + 11, 102), (cx + 11, 86), (cx + 7, 80))
        shaft = pen.rect(cx - 2, 104, cx + 2, 206)
        bands = pen.rect(cx - 5, 116, cx + 5, 120) | pen.rect(cx - 5, 186, cx + 5, 190)
        return crown | horns | shaft | bands

    return _margins(staff)


# --- Captain: a great war banner bearing a crown, over crossed spears, between pennon lances ---

def captain_relief(size):
    pen = _Pen(size)
    bar = pen.rect(136, 70, 216, 77) | pen.pair([(132, 68), (139, 73), (132, 80), (126, 73)])
    cloth = pen.poly((146, 80), (206, 80), (206, 182), (176, 164), (146, 182))
    crown = _crown(size)
    hem = pen.rect(146, 90, 206, 93)
    spears = pen.stroke(5, (122, 190), (226, 94))
    spears |= spears[:, ::-1]
    points = pen.pair([(238, 78), (233, 100), (219, 88)])
    banner = bar | (cloth & ~crown & ~hem)
    return banner | ((spears | points) & ~dilate(dilate(dilate(banner))))


def _crown(size):
    pen = _Pen(size)
    return (pen.poly((158, 106), (167, 119), (176, 100), (185, 119), (194, 106), (192, 132), (160, 132))
            | pen.rect(160, 136, 192, 142))


def captain_hollows(size):
    """Only the crown's three jewels: the crown itself stands out as uncut stone in the banner."""
    pen = _Pen(size)
    return pen.pair([(165, 122), (169, 126), (165, 130), (161, 126)]) | pen.poly((176, 119), (180, 125),
                                                                                (176, 131), (172, 125))


def captain_margins(size):
    pen = _Pen(size)

    def lance(cx):
        point = pen.poly((cx, 74), (cx + 6, 88), (cx, 98), (cx - 6, 88))
        shaft = pen.rect(cx - 2, 96, cx + 2, 206)
        pennon = pen.poly((cx + 2, 100), (cx + 16, 105), (cx + 8, 110), (cx + 16, 118), (cx + 2, 122))
        return point | shaft | pennon | pen.rect(cx - 6, 126, cx + 6, 130)

    return _margins(lance)


# class -> (central relief, its hollows, margins, trace colour)
RELIEFS = {
    "warrior": (warrior_relief, warrior_hollows, warrior_margins, ("crimson", 0)),
    "archer": (archer_relief, archer_hollows, archer_margins, ("forest", 1)),
    "mage": (mage_relief, mage_hollows, mage_margins, ("violet", 1)),
    "captain": (captain_relief, captain_hollows, captain_margins, ("navy", 1)),
}
