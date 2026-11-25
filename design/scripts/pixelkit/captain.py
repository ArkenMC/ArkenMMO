"""The Captain: a tall banner pole and a cape sweep. Open helm, ivory tabard, war horn held aloft."""
import numpy as np

from .figure import Figure, block_eye, grid_detail, pixel_blocks
from .hullrig import Rig, box, euler, prism, slab

HEAD_CENTRE = np.array((4.0, 112.0, 6.0))
HEAD_TURN = euler(yaw=11, pitch=-3, roll=3)
POLE_X, POLE_Z = -35.0, 18.0
POLE_TOP = 171.0
# the war horn from mouthpiece to bell: (x, y, z, thickness)
HORN = [(34, 111, 32, 4), (35, 98, 32, 7), (46, 89, 32, 10), (61, 94, 30, 13), (67, 112, 27, 17)]
# a four-pointed star as two crossed slivers (each part must be convex)
STAR = ([(0, 13), (4, 0), (0, -13), (-4, 0)], [(11, 0), (0, 4), (-11, 0), (0, -4)])
# the rallying call: a pair of notes leaving the bell, the Minstrel side of the class
BEAMED_NOTES = pixel_blocks(["..11111", "..11111", "..1...1", "..1...1", "111.111", "111.111"], 3)
CALL_LEGEND = {"1": ("gold", 4)}

def build(facing=1):
    rig = Rig(yaw=24.0, pitch=10.0, scale=0.815)
    _cape(rig)
    _legs(rig)
    _body(rig)
    _head(rig)
    _banner(rig)
    _arms(rig)
    _horn(rig)
    details = []
    for x, mirrored in ((-9.5, False), (7.5, True)):
        anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 1.0, 18.0))
        eye = block_eye("w", "i", "g", mirrored)
        details.append(grid_detail(["s" * len(eye[0])] * 2 + eye, EYES, anchor))
        brow = pixel_blocks(["..bbb", "bbb.."], 2)
        brow_anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 7.0, 18.0))
        details.append(grid_detail([r[::-1] for r in brow] if mirrored else brow, BROWS, brow_anchor))
    details.append(grid_detail(BEAMED_NOTES, CALL_LEGEND, (64, 147, 22), flip=False))
    return Figure(rig, lean=-2.0, facing=facing, blocky=("flag", "plume", "capehem"),
                  rim={"gold": ("gold", 5), "navy": ("navy", 4), "leather": ("gold", 2)},
                  no_rim=("pole", "flag", "horn", "finial", "plume"), details=details)


EYES = {"w": ("ivory", 4), "i": ("navy", 3), "g": ("navy", 4), "s": ("skin", 1)}
BROWS = {"b": ("leather", 1)}


def _cape(rig):
    """A half cape swept back from the far shoulder: the second half of his silhouette."""
    rig.add(prism([(-27, 97), (14, 97), (-8, 40), (-46, 38)], -24, -17), "navy", 2, "cape")
    rig.add(prism([(-27, 97), (-46, 38), (-61, 28), (-46, 68)], -26, -19), "navy", 3, "cape")
    rig.add(prism([(-46, 38), (-8, 40), (-12, 33), (-47, 31)], -23, -17), "gold", 2, "capehem")
    rig.add(prism([(-61, 28), (-46, 38), (-47, 31), (-61, 21)], -25, -19), "gold", 3, "capehem")


def _legs(rig):
    # the front foot is planted up on a stone block, as if leading the way
    rig.add(box(32, 14, 34, 1.5), "dawn_stone", 3, "leg_block", (27, 7, 14), euler(yaw=10))
    legs = (("leg_back", (-25, 0, -2), (-18, 31, 0), (-9, 57, 0), -12),
            ("leg_front", (26, 14, 14), (29, 40, 20), (9, 57, 2), 14))
    for group, foot, knee, hip, toe_yaw in legs:
        turn = euler(yaw=toe_yaw)
        foot = np.array(foot, float)

        def boot(points, material, base, local, name):
            rig.add(points + np.array(local, float), material, base, group + name, foot, turn)

        boot(box(21, 5, 31, 1.5), "navy", 1, (0, 2.5, 4), "_sole")
        boot(slab((19, 25), (18, 20), 12, 1.5), "gold", 2, (0, 10, 2), "_boot")
        boot(slab((19, 12), (15, 8), 7, 1.5), "gold", 3, (0, 7.5, 16), "_toe")
        rig.bone(foot + (0, 14, 0), knee, (15, 16), (18, 19), "gold", 2, group + "_greave", 1.5)
        rig.bone(knee, hip, (15, 16), (18, 18), "navy", 2, group + "_thigh", 1.5)
        rig.add(slab((18, 10), (12, 8), 11, 1.5), "gold", 3, group + "_knee", (knee[0], knee[1] + 1, knee[2] + 9),
                euler(yaw=toe_yaw * 0.6))


def _body(rig):
    rig.add(slab((34, 25), (32, 24), 11, 1.5), "navy", 2, "hips", (0, 59, 0))
    for side in (-1, 1):
        turn = euler(roll=side * 14)
        rig.add(slab((18, 27), (14, 25), 18, 1.5), "gold", 2, f"tasset{side}", (side * 20, 53, 0), turn)
    rig.add(slab((36, 27), (50, 33), 32, 2.5), "gold", 2, "chest", (0, 83, 0))
    # long ivory tabard with a navy border and the star emblem that doubles as his mark
    rig.add(prism([(-14, 96), (14, 96), (13, 66), (-13, 66)], 14, 19), "ivory", 3, "tabard")
    rig.add(prism([(-13, 66), (13, 66), (16, 34), (0, 27), (-16, 34)], 14, 20), "ivory", 3, "tabardlow")
    for side, step in ((-1, 3), (1, 2)):
        rig.add(prism([(side * 14, 96), (side * 18, 95), (side * 17, 66), (side * 13, 66)], 15, 20), "navy", step,
                "tabard")
        rig.add(prism([(side * 13, 66), (side * 17, 66), (side * 21, 36), (side * 16, 34)], 15, 21), "navy", step,
                "tabardlow")
    for sliver in STAR:
        rig.add(prism([(x * 0.95, y * 0.95 + 82) for x, y in sliver], 20, 23), "navy", 2, "emblem")
    rig.add(prism([(0, 87), (5, 82), (0, 77), (-5, 82)], 22, 25), "gold", 4, "emblemboss")
    rig.add(prism([(0, 53), (5, 46), (0, 39), (-5, 46)], 20, 22.5), "navy", 3, "tabardmark")
    rig.add(slab((39, 40), (39, 40), 7, 1.5), "leather", 3, "belt", (0, 66, 1))
    rig.add(box(11, 10, 5, 1.5), "gold", 3, "buckle", (0, 66, 22))
    rig.add(box(5, 4, 3, 0.5), "navy", 3, "bucklegem", (0, 66, 24.5))
    # sheathed sword: the hilt stays small at the hip
    rig.bone((-24, 66, 14), (-34, 30, 2), (9, 7), (7, 5), "navy", 3, "scabbard", 1.5)
    rig.bone((-34, 30, 2), (-36, 24, 0), (9, 8), (4, 4), "gold", 3, "scabbard", 1)
    rig.bone((-24, 66, 14), (-19, 78, 18), (6, 6), (6, 6), "leather", 3, "hilt", 1)
    rig.add(box(15, 4, 7, 1), "gold", 3, "hilt", (-23, 68, 15), euler(roll=-20))
    rig.add(box(8, 7, 8, 1.5), "gold", 3, "hilt", (-18.5, 80, 18))
    rig.add(slab((42, 32), (34, 28), 8, 2), "navy", 2, "collar", (0, 98, -1))


def _head(rig):
    def put(points, material, base, group, local, **kw):
        rig.add(points + np.array(local, float), material, base, group, HEAD_CENTRE, HEAD_TURN, **kw)

    put(box(32, 31, 28, 1.5), "skin", 3, "face", (0, 0, 3))
    # short square beard and moustache, mouth open in a shout
    put(box(34, 8, 9, 1.5), "leather", 3, "beard", (0, -14, 15))
    for side in (-1, 1):
        put(box(5, 15, 8, 1), "leather", 3, "beard", (side * 14.5, -7, 15))
    put(box(21, 4, 4, 1), "leather", 2, "beard", (0, -7, 18))
    put(box(11, 4, 3, 0.5), "skin", 0, "mouth", (0, -10.5, 19.5), lo=0, hi=0)
    put(box(6, 7, 6, 1.5), "skin", 3, "nose", (0.5, -3, 18))
    # open helm: a gold cap with a raised front, cheek guards set back so the whole face shows
    put(box(40, 11, 37, 2), "gold", 2, "helm", (0, 17, 0))
    put(slab((36, 33), (26, 24), 7, 1.5), "gold", 3, "helm", (0, 26, -1))
    put(box(41, 4, 38, 1), "gold", 3, "helmrim", (0, 11.5, 0))
    put(prism([(-9, 13), (9, 13), (5, 26), (0, 31), (-5, 26)], 17, 21), "gold", 4, "helm", (0, 0, 0))
    put(prism([(0, 24), (4, 19.5), (0, 15), (-4, 19.5)], 20, 23), "navy", 3, "helmgem", (0, 0, 0))
    for side in (-1, 1):
        put(box(5, 27, 22, 1.5), "gold", 2, "helm", (side * 18.5, -1, -4))
    put(box(38, 30, 9, 1.5), "gold", 2, "helm", (0, -1, -15))
    # a short ivory horsetail plume that pours down behind him
    plume = [[(-2, 28), (-11, 39), (-23, 34), (-13, 27)], [(-11, 39), (-26, 29), (-27, 14), (-19, 28)],
             [(-26, 29), (-30, 8), (-24, -6), (-20, 20)]]
    for index, outline in enumerate(plume):
        points = np.array([(x, y, z) for z in (-16, -8) for x, y in outline], float)
        put(points, "ivory", 3 if index != 1 else 2, "plume", (0, 0, 0))


def _banner(rig):
    rig.bone((POLE_X, 2, POLE_Z), (POLE_X, POLE_TOP, POLE_Z), (6, 6), (6, 6), "leather", 3, "pole", 1.5)
    finial = np.array((POLE_X, POLE_TOP + 8, POLE_Z))
    points = [(0, 11, 0), (0, -8, 0), (7, 0, 0), (-7, 0, 0), (0, 0, 6), (0, 0, -6)]
    rig.solid([finial + np.array(p, float) for p in points], "gold", 3, "finial")
    rig.add(box(10, 4, 10, 1), "gold", 3, "finial", (POLE_X, POLE_TOP - 1, POLE_Z))
    z = POLE_Z - 6
    top, bottom = POLE_TOP - 4, POLE_TOP - 44
    middle = (top + bottom) / 2

    def cloth(outline, depth, material, step, group):
        rig.add(prism([(POLE_X - x, y) for x, y in outline], z + depth, z + depth + 3), material, step, group)

    # the swallowtail streams back from the pole into open sky: x runs away from the pole
    cloth([(2, top), (26, top - 4), (26, bottom - 4), (2, bottom)], 0, "ivory", 3, "flagfield")
    cloth([(26, top - 4), (50, top + 1), (28, middle - 3), (26, middle - 4)], -1, "ivory", 3, "flagfield")
    cloth([(26, middle - 4), (28, middle - 3), (50, bottom - 7), (26, bottom - 4)], -1, "ivory", 2, "flagfield")
    for outline in ([(2, top + 1), (26, top - 3), (26, top - 8), (2, top - 4)],
                    [(2, bottom + 5), (26, bottom + 1), (26, bottom - 4), (2, bottom - 1)],
                    [(26, top - 3), (50, top + 2), (45, top - 5), (26, top - 8)],
                    [(26, bottom + 1), (45, bottom - 1), (50, bottom - 8), (26, bottom - 4)]):
        cloth(outline, 3, "navy", 3, "flagedge")
    for sliver in STAR:
        cloth([(15 + x * 1.15, middle - 2 + y * 1.15) for x, y in sliver], 4, "navy", 2, "emblemflag")
    cloth([(15, middle + 2), (19, middle - 2), (15, middle - 6), (11, middle - 2)], 7, "gold", 3, "emblemflag")


def _pauldron(rig, side, at):
    turn = euler(roll=-side * 14, yaw=side * 6)
    rig.add(box(25, 4, 29, 1), "navy", 3, f"pauldron{side}trim", (at[0] + side, at[1] - 6, at[2]), turn)
    rig.add(slab((24, 28), (16, 20), 11, 2), "gold", 3, f"pauldron{side}", at, turn)


def _arms(rig):
    # banner arm
    shoulder, elbow, hand = (-23, 93, 0), (-39, 73, 8), (POLE_X + 1, 84, POLE_Z + 3)
    rig.bone(shoulder, elbow, (15, 16), (13, 14), "navy", 3, "polearm_up", 1.5)
    rig.bone(elbow, hand, (14, 15), (15, 15), "gold", 2, "polearm_fore", 1.5)
    rig.add(box(13, 13, 13, 1.5), "gold", 3, "polefist", (POLE_X, 85, POLE_Z + 4))
    for y in (81.5, 86.5):
        rig.add(box(14, 1.2, 14, 0), "gold", 1, "polefist", (POLE_X, y, POLE_Z + 4.3))
    # horn arm: raised high and forward to rally the company
    shoulder, elbow, hand = (23, 94, 0), (41, 70, 8), (46, 84, 28)
    rig.bone(shoulder, elbow, (15, 16), (13, 14), "navy", 3, "hornarm_up", 1.5)
    rig.bone(elbow, hand, (13, 14), (14, 15), "gold", 2, "hornarm_fore", 1.5)
    rig.add(box(14, 13, 15, 1.5), "gold", 3, "hornfist", (47, 87, 35), euler(roll=8))
    for x in (43.5, 48.5):
        rig.add(box(1.2, 14, 16, 0), "gold", 1, "hornfist", (x, 87, 35.3), euler(roll=8))
    for side, at in ((-1, (-25, 96, 0)), (1, (26, 96, 0))):
        _pauldron(rig, side, at)


def _horn(rig):
    for index, (a, b) in enumerate(zip(HORN, HORN[1:])):
        rig.bone(a[:3], b[:3], (a[3], a[3]), (b[3], b[3]), "ivory", 3 if index != 1 else 2, "horn", 1.5)
    for index, grow in ((1, 3), (2, 3)):
        a, b = np.array(HORN[index + 1][:3], float), np.array(HORN[index + 2][:3], float)
        size = HORN[index + 1][3] + grow
        rig.bone(a - (b - a) * 0.14, a + (b - a) * 0.14, (size, size), (size, size), "gold", 2, "hornband", 1)
    bell = np.array(HORN[-1][:3], float)
    rig.bone(bell + (0, -2, 0), bell + (1, 4, 0), (20, 20), (22, 22), "gold", 3, "hornbell", 1.5)
    rig.add(box(14, 2, 14, 1), "leather", 0, "hornmouth", bell + np.array((0.0, 5.0, 0.0)), lo=0, hi=0)
