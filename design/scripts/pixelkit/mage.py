"""The Mage: a tall triangle. Stepped wizard hat, block beard, flared robe, orb staff and arcane flame."""
import numpy as np

from .figure import Figure, block_eye, grid_detail, pixel_blocks
from .hullrig import Rig, box, euler, prism, slab

HEAD_CENTRE = np.array((3.0, 101.0, 5.0))
HEAD_TURN = euler(yaw=12, pitch=3, roll=-2)
STAFF_FOOT = np.array((-46.0, 3.0, 22.0))
STAFF_TOP = np.array((-66.0, 121.0, 12.0))
FLAME_HAND = (54.0, 82.0, 20.0)

# arcane flame in 4 px blocks, with a dark rim so it reads against the sky
FLAME = [
    ".....0.....",
    "....020....",
    "....0220...",
    "...02320.0.",
    ".0.023320..",
    "...0233220.",
    "..02334320.",
    ".023344320.",
    ".023444320.",
    ".022344320.",
    "..0223320..",
    "...01220...",
    "....000....",
]
FLAME_LEGEND = {str(step): ("arcane", step) for step in range(5)}
# the casting hand, hand-placed over the flame: palm up, fingers curling round its base
CUPPED_HAND = [
    ".kk.................",
    "kHHk............kk..",
    "kHhk...........kHHk.",
    "kHhhk....kk....kHhk.",
    "kHhhk...kHHk..kHhhk.",
    ".kHhhkkkkHhkkkHhhdk.",
    ".kHHHHHHHHHHHHhhhdk.",
    "..khhhhhhhhhhhhhdk..",
    "...kddddddddddddk...",
    "....kkkkkkkkkkkk....",
]
HAND_LEGEND = {"k": ("skin", 0), "H": ("skin", 4), "h": ("skin", 3), "d": ("skin", 2)}
# free-floating square motes around the flame and the orb
MOTE = pixel_blocks([".1.", "132", ".2."], 2)
MOTE_SMALL = pixel_blocks(["32", "21"], 2)
MOTE_LEGEND = {"1": ("arcane", 1), "2": ("arcane", 2), "3": ("arcane", 3)}


def build(facing=1):
    rig = Rig(yaw=24.0, pitch=10.0, scale=0.84)
    _robe(rig)
    _body(rig)
    _head(rig)
    _hat(rig)
    _staff(rig)
    _arms(rig)
    details = []
    for x, mirrored in ((-7.0, False), (8.5, True)):
        anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 1.5, 18.5))
        eye = block_eye("w", "i", "g", mirrored, block=5)
        details.append(grid_detail(["s" * len(eye[0])] * 2 + eye, EYES, anchor))
        brow = pixel_blocks([".bbbb", "bbb.."], 2)
        brow_anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 10.0, 19.0))
        details.append(grid_detail([r[::-1] for r in brow] if mirrored else brow, BROWS, brow_anchor))
    details.append(grid_detail(pixel_blocks(FLAME, 4), FLAME_LEGEND, FLAME_HAND, offset=(-18, -57)))
    details.append(grid_detail(CUPPED_HAND, HAND_LEGEND, FLAME_HAND, offset=(-8, -9)))
    for point, shape in (((68, 142, 10), MOTE), ((44, 150, 10), MOTE_SMALL), ((72, 104, 10), MOTE_SMALL),
                         ((-74, 112, 10), MOTE_SMALL), ((40, 62, 10), MOTE_SMALL)):
        details.append(grid_detail(shape, MOTE_LEGEND, point))
    # leans back from the flame he is raising
    return Figure(rig, lean=4.0, facing=facing,
                  blocky=("staffhead", "orb", "hatbrim", "hattip", "hemtail"),
                  rim={"violet": ("arcane", 2), "leather": ("violet", 4)},
                  no_rim=("staff", "orb"), details=details)


EYES = {"w": ("ivory", 4), "i": ("arcane", 2), "g": ("arcane", 3), "s": ("skin", 0)}
BROWS = {"b": ("ivory", 4)}


def _robe(rig):
    for side, z in ((-1, 3), (1, 10)):
        rig.add(box(18, 9, 28, 1.5), "leather", 2, f"leg_boot{side}", (side * 19, 4.5, z + 6), euler(yaw=side * 14))
    # the flared skirt in two tiers, wide at the hem
    rig.add(slab((76, 46), (42, 29), 42, 2.5, top_shift=(2, 0)), "violet", 2, "leg_robe", (0, 30, 0))
    rig.add(slab((44, 30), (35, 25), 20, 2), "violet", 2, "leg_waist", (2, 59, 0))
    rig.add(slab((79, 49), (77, 47), 6, 1.5), "gold", 2, "leg_hem", (-0.5, 11.5, 0))
    # cloth caught by the magic, streaming out behind
    rig.add(prism([(-20, 52), (-30, 14), (-66, 20), (-44, 32)], -16, -6), "violet", 2, "hemtail")
    rig.add(prism([(-44, 32), (-66, 20), (-70, 36), (-58, 30)], -15, -8), "violet", 1, "hemtail")
    # open front over a dark under-robe, edged in gold
    rig.add(prism([(-5, 62), (7, 62), (18, 15), (-12, 15)], 19, 27), "violet", 1, "leg_under")
    for top, foot in ((-5, -12), (7, 18)):
        edge = [(top - 2, 62), (top + 2, 62), (foot + 3, 15), (foot - 3, 15)]
        rig.add(prism(edge, 24, 29), "gold", 3 if top < 0 else 2, "leg_trim")
    for y in (47, 33):
        rig.add(prism([(1, y + 5), (6, y), (1, y - 5), (-4, y)], 27, 30), "arcane", 2, "leg_rune")


def _body(rig):
    rig.add(slab((35, 25), (41, 28), 28, 2.5), "violet", 2, "chest", (0, 78, 0))
    rig.add(slab((39, 29), (39, 29), 8, 1.5), "leather", 2, "belt", (0, 66, 0))
    rig.add(prism([(0, 73), (8, 66), (0, 59), (-8, 66)], 14, 19), "gold", 3, "clasp")
    rig.add(prism([(0, 70), (4, 66), (0, 62), (-4, 66)], 18, 20.5), "arcane", 2, "claspgem")
    rig.add(prism([(2, 64), (10, 64), (16, 40), (7, 37)], 24, 29), "leather", 3, "sash")
    rig.add(box(10, 12, 9, 2), "leather", 3, "pouch", (-17, 59, 15))
    # layered mantle with a gold edge, and a high collar behind the head
    rig.add(slab((55, 36), (35, 28), 12, 2.5), "violet", 2, "mantle", (0, 91, -1))
    rig.add(slab((57, 38), (56, 37), 4, 1), "gold", 2, "mantletrim", (0, 84.5, -1))
    for side in (-1, 1):
        wing = [(side * 12, 90), (side * 30, 96), (side * 31, 117), (side * 18, 104)]
        rig.add(prism(wing, -17, -11), "violet", 2, "collar")


def _head(rig):
    def put(points, material, base, group, local, **kw):
        rig.add(points + np.array(local, float), material, base, group, HEAD_CENTRE, HEAD_TURN, **kw)

    put(box(33, 29, 29, 1.5), "skin", 4, "face", (0, 1, 3))
    put(box(7, 9, 7, 1.5), "skin", 3, "nose", (1, -4.5, 19))
    # long white hair at the sides
    for side in (-1, 1):
        put(box(8, 31, 26, 1.5), "ivory", 3, "hair", (side * 19, -4, -2))
    put(box(36, 32, 8, 1.5), "ivory", 2, "hair", (0, -3, -14))
    # moustache and a beard that steps down to a point
    for side in (-1, 1):
        put(prism([(0, -6), (side * 17, -8), (side * 19, -15), (side * 3, -11)], 17, 23), "ivory", 4, "moustache",
            (0, 0, 0))
    for (width, y, depth, z) in ((35, -14, 13, 14), (27, -22, 12, 17), (18, -30, 11, 19), (9, -37, 9, 20)):
        put(box(width, 9, depth, 1.5), "ivory", 3, "beard", (1, y, z))
    put(box(8, 4, 3, 1), "skin", 1, "mouth", (1, -11, 21))


def _hat(rig):
    base = HEAD_CENTRE + np.array((0.0, 16.0, 0.0))

    def tier(size_low, size_high, height, offset, material, step, group, roll):
        rig.add(slab(size_low, size_high, height, 1.5), material, step, group, base + np.array(offset, float),
                euler(yaw=12, roll=roll, pitch=-5))

    tier((59, 52), (55, 48), 6, (0, 0, 0), "violet", 2, "hatbrim", -4)
    tier((42, 39), (37, 34), 8, (-1, 6, -1), "gold", 2, "hatband", -3)
    tier((40, 37), (29, 27), 15, (-2, 16, -2), "violet", 2, "hat", 1)
    tier((29, 27), (20, 19), 15, (-4, 30, -4), "violet", 2, "hat", 5)
    tier((20, 19), (13, 13), 14, (-7, 43, -6), "violet", 2, "hattip", 18)
    tier((13, 13), (8, 8), 13, (-15, 52, -7), "violet", 2, "hattip", 62)
    tier((8, 8), (3, 3), 14, (-26, 52, -8), "violet", 3, "hattip", 118)
    front = base + np.array((2.0, 7.0, 20.0))
    rig.add(prism([(0, 8), (7, 0), (0, -8), (-7, 0)], -1, 3), "gold", 3, "hatgem", front, euler(yaw=12))
    rig.add(prism([(0, 4.5), (4, 0), (0, -4.5), (-4, 0)], 2, 5), "arcane", 3, "hatgem", front, euler(yaw=12))


def _staff(rig):
    rig.bone(STAFF_FOOT, STAFF_TOP, (6, 6), (7, 7), "leather", 3, "staff", 1.5)
    along = (STAFF_TOP - STAFF_FOOT) / np.linalg.norm(STAFF_TOP - STAFF_FOOT)
    for t in (0.04, 0.38, 0.86):
        centre = STAFF_FOOT + (STAFF_TOP - STAFF_FOOT) * t
        rig.bone(centre - along * 3, centre + along * 3, (10, 10), (10, 10), "gold", 2, "staffband", 1.5)
    top = STAFF_TOP
    # a forked head cradling a floating crystal
    for side in (-1, 1):
        elbow = top + np.array((side * 12.0, 8.0, 0.0))
        rig.bone(top + (0, -2, 0), elbow, (8, 8), (7, 7), "gold", 3, "staffhead", 1.5)
        rig.bone(elbow + (0, -2, 0), elbow + np.array((-side * 1.0, 18.0, 0.0)), (7, 7), (3, 3), "gold", 3,
                 "staffhead", 0.8)
    crystal = top + np.array((0.0, 23.0, 1.0))
    points = [(0, 15, 0), (0, -13, 0), (10, 0, 0), (-10, 0, 0), (0, 0, 9), (0, 0, -9)]
    rig.solid([crystal + np.array(p, float) for p in points], "arcane", 2, "orb", lo=1, hi=4)


def _arms(rig):
    def sleeve(name, shoulder, elbow, wrist):
        rig.bone(shoulder, elbow, (15, 17), (15, 17), "violet", 2, name + "up", 2)
        elbow, wrist = np.array(elbow, float), np.array(wrist, float)
        rig.bone(elbow, wrist, (15, 17), (23, 23), "violet", 2, name + "bell", 2)
        along = (wrist - elbow) / np.linalg.norm(wrist - elbow)
        rig.bone(wrist - along * 4, wrist + along * 2, (25, 25), (25, 25), "gold", 2, name + "cuff", 1.5)
        rig.bone(wrist, wrist + along * 5, (10, 10), (10, 10), "skin", 3, name + "wrist", 1.5)

    # staff arm, reaching out so that sky shows between the staff and the robe
    sleeve("staffarm", (-18, 90, 0), (-39, 72, 3), (-49, 76, 14))
    rig.add(box(14, 13, 14, 1.5), "skin", 3, "stafffist", (-57, 76, 20), euler(roll=10))
    for y in (72, 77):
        rig.add(box(15, 1.2, 15, 0), "skin", 1, "stafffist", (-57, y, 20.3), euler(roll=10))
    # casting arm: thrust toward the centre, palm up under the flame
    sleeve("castarm", (19, 90, 1), (36, 73, 8), (49, 79, 17))
    rig.add(box(17, 7, 16, 1.5), "skin", 3, "palm", (FLAME_HAND[0] + 2, FLAME_HAND[1], FLAME_HAND[2]))
