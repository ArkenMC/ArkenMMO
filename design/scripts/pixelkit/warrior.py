"""The Warrior: wide, low, square. Great helm, huge pauldrons, tower shield, cleaver hoisted high."""
import numpy as np

from .figure import Figure, block_eye, grid_detail
from .hullrig import Rig, box, euler, prism, slab

SWORD_GRIP = (-46.0, 74.0, 31.0)
SWORD_TIP = (-66.0, 164.5, -6.0)
HEAD_CENTRE = (4.0, 115.0, 7.0)
HEAD_TURN = euler(yaw=10, pitch=4, roll=-3)


def build(facing=1):
    rig = Rig(yaw=24.0, pitch=10.0, scale=0.885)
    _legs(rig)
    _body(rig)
    _head(rig)
    _sword_arm(rig)
    _shield_arm(rig)
    details = [grid_detail(GAUNTLET, GAUNTLET_LEGEND, SWORD_GRIP, offset=(-10, -7))]
    # narrowed, glowing block eyes inside the visor slot
    for x, mirrored in ((-9.5, False), (10.5, True)):
        anchor = np.array(HEAD_CENTRE) + HEAD_TURN @ np.array((x, -0.5, 22.0))
        details.append(grid_detail(block_eye("o", "y", "W", mirrored, block=5), EYE_LEGEND, anchor))
    # leans into a lunge toward the centre of the menu
    return Figure(rig, lean=-4.5, facing=facing,
                    blocky=("edge", "guard", "crest"),
                    rim={"steel": ("crimson", 3), "crimson": ("crimson", 4)},
                    no_rim=("edge", "pauldron1spike"), details=details)


EYE_LEGEND = {"o": ("crimson", 4), "y": ("gold", 4), "W": ("gold", 5)}


# The sword hand, hand-placed: thumb over the top, four fingers wrapped round the grip.
GAUNTLET = [
    ".kkkkkkkkkkkkkkkkk....",
    ".k555555555444443k....",
    ".k55555444444443kkkk..",
    ".kkkkkkkkkkkkkk33333k.",
    ".k5555544444k3k33222k.",
    ".k4444433333k2k33221k.",
    ".kkkkkkkkkkkkkk33221k.",
    ".k5555544444k3k33221k.",
    ".k4444433333k2k32221k.",
    ".kkkkkkkkkkkkkk32221k.",
    ".k5555444444k3k32211k.",
    ".k4444333333k2k22211k.",
    ".kkkkkkkkkkkkkk22211k.",
    ".k4444433333k3k22111k.",
    ".k3333322222k2k21111k.",
    ".kkkkkkkkkkkkkkkkkkkk.",
]
GAUNTLET_LEGEND = {"k": ("steel", 0), "1": ("steel", 1), "2": ("steel", 2), "3": ("steel", 3),
                   "4": ("steel", 4), "5": ("steel", 5)}


def _legs(rig):
    # back foot (screen left) trails wide, front foot steps toward the centre
    for side, foot_x, foot_z in ((-1, -36, -6), (1, 22, 13)):
        g = "leg_r" if side < 0 else "leg_l"
        toe_turn = euler(yaw=side * 14)

        def boot(points, material, base, group, local):
            rig.add(points + np.array(local, float), material, base, group, (foot_x, 0, foot_z), toe_turn)

        boot(box(27, 5, 38, 1.5), "steel", 1, g + "_sole", (0, 2.5, 4))
        boot(slab((25, 31), (23, 26), 13, 1.5), "steel", 2, g + "_boot", (0, 10, 1))
        boot(slab((24, 13), (20, 10), 8, 1.5), "steel", 3, g + "_toe", (0, 8, 19))
        boot(box(26, 5, 27, 1.5), "gold", 2, g + "_band", (0, 18, 0))
        knee = (foot_x * 0.80, 36, foot_z * 0.8 + 3)
        hip = (side * 12, 56, 0)
        rig.bone((foot_x, 17, foot_z), knee, (20, 21), (21, 22), "steel", 2, g + "_shin", 1.5)
        rig.bone(knee, hip, (19, 20), (21, 21), "steel", 1, g + "_thigh", 1.5)
        # pointed knee plate in steel, so the lower body stays quiet under the hilt and shield
        turn = euler(yaw=side * 10, roll=-side * 6)
        rig.add(slab((15, 9), (18, 10), 7, 1.5), "steel", 2, g + "_knee", (knee[0], 32, knee[2] + 11), turn)
        rig.add(slab((18, 10), (9, 7), 8, 1.5), "steel", 3, g + "_knee", (knee[0], 39, knee[2] + 11), turn)


def _body(rig):
    rig.add(slab((38, 28), (36, 27), 12, 1.5), "steel", 1, "hips", (0, 56, 0))
    # two-layer tassets flaring over the thighs
    for side in (-1, 1):
        turn = euler(roll=side * 16)
        rig.add(slab((22, 31), (18, 28), 17, 1.5), "crimson", 2, f"tasset{side}", (side * 23, 50, 1), turn)
        rig.add(box(23, 3, 32, 1), "gold", 2 if side > 0 else 1, f"tassettrim{side}", (side * 25.6, 42, 1), turn)
        rig.add(slab((20, 33), (19, 31), 7, 2), "steel", 2, f"fauld{side}", (side * 21, 57, 1), turn)
    # war skirt: a crimson tabard flap with a gold hem
    rig.add(prism([(-10, 58), (10, 58), (12, 37), (0, 29), (-12, 37)], 12, 19), "crimson", 2, "tabard")
    rig.add(prism([(-12, 37), (0, 29), (0, 33), (-11.5, 40)], 18, 20.5), "gold", 3, "tabard")
    rig.add(prism([(0, 29), (12, 37), (11.5, 40), (0, 33)], 18, 20.5), "gold", 2, "tabard")
    rig.add(prism([(0, 52), (4, 47), (0, 40), (-4, 47)], 18.5, 21), "gold", 3, "tabardmark")
    # belt with a heavy buckle
    rig.add(slab((43, 33), (44, 34), 8, 2), "leather", 2, "belt", (0, 61, 0))
    rig.add(box(16, 13, 5, 1.5), "gold", 3, "buckle", (0, 61, 18))
    rig.add(box(6, 5, 3, 2), "crimson", 3, "bucklegem", (0, 61, 21.5))
    # abdomen lames, then a barrel chest that flares toward the shoulders
    rig.add(slab((38, 29), (42, 31), 6, 2), "steel", 3, "lame1", (0, 67, 0))
    rig.add(slab((43, 31), (47, 33), 6, 2), "steel", 3, "lame2", (0, 72, 0))
    rig.add(slab((48, 32), (65, 38), 23, 2.5), "crimson", 2, "chest", (0, 85, 0))
    rig.add(prism([(-21, 93), (0, 88), (0, 74), (-17, 79)], 14, 21), "crimson", 3, "keel_r")
    rig.add(prism([(0, 88), (21, 93), (17, 79), (0, 74)], 14, 21), "crimson", 2, "keel_l")
    rig.add(prism([(-25, 98), (-22, 92), (0, 86), (0, 91.5)], 19, 24), "gold", 3, "collar")
    rig.add(prism([(0, 91.5), (0, 86), (22, 92), (25, 98)], 19, 24), "gold", 2, "collar")
    rig.add(prism([(-5.5, 83), (0, 89), (0, 76)], 20, 25), "gold", 4, "medal")
    rig.add(prism([(0, 89), (5.5, 83), (0, 76)], 20, 25), "gold", 2, "medal")
    rig.add(slab((50, 34), (42, 31), 9, 2), "steel", 2, "gorget", (1, 99, 0))


def _head(rig):
    def put(points, material, base, group, local, **kw):
        rig.add(points + np.array(local, float), material, base, group, HEAD_CENTRE, HEAD_TURN, **kw)

    # great helm: skull, domed crown and a jutting two-plate chin guard
    put(slab((43, 37), (43, 37), 27, 1.5), "steel", 3, "helm", (0, 1, 0))
    put(slab((43, 37), (35, 29), 9, 1.5), "steel", 3, "crown", (0, 18.5, 0))
    put(prism([(-21, -2), (0, -2), (0, -19), (-21, -19)], 8, 22), "steel", 4, "helm", (0, 0, 0))
    put(prism([(0, -2), (20, -2), (18, -19), (0, -19)], 10, 22), "steel", 3, "helm", (0, 0, 0))
    # visor: a wide dark eye slot with a breath slit below
    put(box(35, 11, 3, 0), "steel", 0, "visor", (0, 0.8, 19.5), lo=0, hi=0)
    put(box(5, 13, 3, 0), "steel", 0, "visor", (0, -8, 22), lo=0, hi=0)
    for x in (-10, 10):
        for y in (-9, -13):
            put(box(4, 3, 2), "steel", 0, "breath", (x, y, 22.5), lo=0, hi=0)
    # heavy brow: gold blocks stepping down to the middle, which reads as a scowl
    for side, base in ((-1, 3), (1, 2)):
        for x, y in ((18, 12.5), (11, 10.5), (4, 8.5)):
            put(box(7.4, 5, 7), "gold", base, "brow", (side * x, y, 19.5))
    put(box(4, 13, 4, 1.5), "gold", 3, "ridge", (0, 17, 18))
    # plain cheek plates, one step darker than the skull
    for x in (-21, 21):
        put(box(3, 25, 16, 1.5), "steel", 2, "helm", (x, -6, 5))
    _crest(rig, put)


# Crest teeth as (z, y) outlines on the helm's centre plane; each one sweeps back, so the silhouette is jagged.
CREST = [
    [(16, 22), (3, 22), (3, 35), (7, 38)],
    [(8, 22), (-8, 22), (-12, 48), (1, 36)],
    [(-3, 22), (-19, 21), (-30, 47), (-10, 36)],
    [(-13, 21), (-25, 13), (-44, 33), (-23, 29)],
    [(-19, 15), (-24, 0), (-45, 13), (-27, 17)],
]


def _crest(rig, put):
    put(box(10, 5, 32, 1.5), "gold", 2, "crestbase", (0, 23, -1))
    for i, outline in enumerate(CREST):
        points = np.array([(x, y, z) for x in (-4.5, 4.5) for z, y in outline], float)
        put(points, "crimson", 2 - i % 2, f"crest{i}", (0, 0, 0), hi=4)


def _pauldron(rig, side, at, scale=1.0):
    """Stacked plates, each smaller and higher, tilted down toward the outside."""
    g = f"pauldron{side}"
    turn = euler(roll=-side * 16, yaw=side * 6)
    at = np.array(at, float)

    def put(points, material, base, group, local):
        rig.add(points * scale + np.array(local, float) * scale, material, base, group, at, turn)

    put(slab((33, 38), (31, 36), 8, 1.5), "steel", 2, g + "low", (side * 3, -11, 0))
    put(box(40, 4, 42, 1.5), "gold", 2, g + "trim", (side, -5.5, 0))
    put(slab((39, 41), (32, 34), 16, 2.5), "crimson", 2, g + "main", (0, 4, 0))
    put(box(26, 3, 28, 1), "gold", 2, g + "trim2", (-side, 12.5, 0))
    put(slab((23, 25), (17, 19), 7, 1.5), "crimson", 2, g + "cap", (-side, 17, 0))
    put(box(6, 6, 4, 2), "gold", 3, g + "stud", (side * 7, 2, 21))
    if side < 0:
        return  # the blade covers this shoulder; a horn here would only peek out as a stray nub
    # a two-segment horn spike that breaks the outline
    put(box(13, 5, 13, 1.5), "gold", 2, g + "spikeseat", (side * 14, 13, 1))
    horn = at + turn @ (np.array((side * 15.0, 14.0, 1.0)) * scale)
    mid = at + turn @ (np.array((side * 23.0, 24.0, 1.0)) * scale)
    end = at + turn @ (np.array((side * 24.5, 36.0, 1.0)) * scale)
    rig.bone(horn, mid, (10, 10), (7, 7), "steel", 4, g + "spike", 1.5)
    rig.bone(mid, end, (7, 7), (1.5, 1.5), "steel", 4, g + "spike", 0.4)


def _sword_arm(rig):
    """His right arm (screen left): elbow flung out, fist gripping the raised cleaver."""
    shoulder, elbow, hand = (-33, 90, 0), (-55, 70, 5), (-47, 70, 25)
    rig.bone(shoulder, elbow, (19, 20), (16, 17), "steel", 2, "arm_r_up", 1.5)
    rig.bone(elbow, hand, (18, 19), (19, 19), "crimson", 1, "arm_r_fore", 1.5)
    _pauldron(rig, -1, (-37, 96, -2))
    _sword(rig, np.array(SWORD_GRIP), np.array(SWORD_TIP))
    _fist(rig, np.array(SWORD_GRIP))


def _fist(rig, at):
    turn = euler(roll=17)

    def put(points, material, base, group, local):
        rig.add(points + np.array(local, float), material, base, group, at, turn)

    put(box(19, 16, 17, 1.5), "steel", 3, "fist", (0, 0, 0))
    put(box(21, 5, 18, 1.5), "gold", 2, "fist_cuff", (2, -9, -3))
    for i, y in enumerate((4.5, -0.5, -5.5)):
        put(box(11, 4, 4, 1.5), "steel", 3, f"finger{i}", (1.5, y, 9))
    put(box(6, 9, 6, 2), "steel", 3, "thumb", (-8, 3, 8))


def _sword(rig, grip, tip):
    """A broad cleaver greatsword along the line grip -> tip."""
    along = (tip - grip) / np.linalg.norm(tip - grip)
    across = np.cross((0.0, 0.0, 1.0), along)
    across /= np.linalg.norm(across)
    if across[0] > 0:
        across = -across  # points to the cutting edge, up and left
    normal = np.cross(along, across)
    if normal[2] < 0:
        normal = -normal

    def at(t, s, n=0.0):
        return grip + along * t + across * s + normal * n

    def blade(outline, thickness, material, base, group, lift=0.0, lo=1, hi=99):
        pts = [at(t, s, side * thickness / 2 + lift) for t, s in outline for side in (-1, 1)]
        rig.solid(pts, material, base, group, lo, hi)

    rig.bone(at(-16, 0), at(15, 0), (7, 7), (7, 7), "leather", 2, "grip", 2)
    # faceted diamond pommel
    blade([(-13, 0), (-18.5, 5.5), (-18.5, 0)], 9, "gold", 3, "pommel")
    blade([(-13, 0), (-18.5, 0), (-18.5, -5.5)], 9, "gold", 2, "pommel")
    blade([(-24, 0), (-18.5, 5.5), (-18.5, 0)], 9, "gold", 2, "pommel")
    blade([(-24, 0), (-18.5, 0), (-18.5, -5.5)], 9, "gold", 1, "pommel")
    # crossguard with down-turned quillons
    blade([(12, -6), (21, -6), (21, 6), (12, 6)], 11, "gold", 3, "guard")
    blade([(15, 5), (21, 5), (15, 20), (10, 21)], 8, "gold", 3, "guard")
    blade([(14, -5), (21, -5), (15, -21), (9, -22)], 8, "gold", 2, "guard")
    blade([(14, -3), (19, -3), (19, 3), (14, 3)], 3, "crimson", 3, "guardgem", lift=6)
    length = float(np.linalg.norm(tip - grip))
    # blade: a bright bevelled edge and a darker flat, ending in a heavy clipped point
    blade([(20, 0), (20, 10), (31, 13), (length - 13, 15), (length - 13, 0)], 5, "steel", 4, "edge", hi=5)
    blade([(length - 13, 0), (length - 13, 15), (length + 6, 2), (length - 3, 0)], 5, "steel", 4, "edge", hi=5)
    blade([(20, -10), (20, 0), (length - 13, 0), (length - 13, -11), (31, -9)], 5, "steel", 3, "edge", hi=3)
    blade([(length - 13, -11), (length - 13, 0), (length - 3, 0)], 5, "steel", 3, "edge", hi=3)
    # back hook below the point: the cleaver's signature shape in silhouette
    blade([(length - 36, -8), (length - 21, -8), (length - 18, -20), (length - 24, -17)], 5, "steel", 3, "edge", hi=3)
    blade([(20, 10), (31, 13), (length - 13, 15), (length - 15, 10), (31, 8), (20, 5)], 1, "steel", 6, "edge",
          lift=3, lo=6)


def _shield_arm(rig):
    """His left arm (screen right): braced behind a tower shield held toward the centre."""
    shoulder, elbow, hand = (34, 91, 0), (47, 70, 4), (41, 60, 22)
    rig.bone(shoulder, elbow, (19, 20), (16, 17), "steel", 2, "arm_l_up", 1.5)
    rig.bone(elbow, hand, (19, 19), (17, 17), "crimson", 2, "arm_l_fore", 1.5)
    _pauldron(rig, 1, (38, 96, -3), 0.94)
    _shield(rig, np.array((34.0, 46.0, 30.0)), euler(yaw=4, roll=-5))


def _shield(rig, centre, turn):
    def put(outline, z0, z1, material, base, group, **kw):
        rig.add(prism(outline, z0, z1), material, base, group, centre, turn, **kw)

    rim = [(-23, 30), (-16, 37), (16, 37), (23, 30), (23, -20), (0, -41), (-23, -20)]
    inner = [(-17, 27), (-12, 31), (12, 31), (17, 27), (17, -18), (0, -33), (-17, -18)]
    put(rim, -5, 1, "steel", 1, "shield_back")
    # rim built from bars so each side takes its own light
    rim_steps = (4, 5, 4, 2, 2, 2, 3)
    for i in range(len(rim)):
        j = (i + 1) % len(rim)
        put([rim[i], rim[j], inner[j], inner[i]], 0, 7, "steel", rim_steps[i], "shield_rim")
    put([(-17, 27), (-12, 31), (0, 31), (0, -33), (-17, -18)], 0, 3.5, "crimson", 3, "shield_face")
    put([(0, 31), (12, 31), (17, 27), (17, -18), (0, -33)], 0, 3.5, "crimson", 2, "shield_face")
    # emblem: one bold chevron over a diamond; anything busier turns to noise at screen size
    put([(-14, 11), (0, 22), (0, 13), (-14, 2)], 3, 7, "gold", 4, "emblem")
    put([(0, 22), (14, 11), (14, 2), (0, 13)], 3, 7, "gold", 3, "emblem")
    put([(-9, -7), (0, 4), (0, -19)], 3, 9, "gold", 4, "emblem_boss")
    put([(0, 4), (9, -7), (0, -19)], 3, 9, "gold", 2, "emblem_boss")
    for x, y in ((-19.5, 28), (19.5, 28), (-20, -18), (20, -18), (0, -36), (0, 34)):
        put([(x - 2.5, y), (x, y + 2.5), (x + 2.5, y), (x, y - 2.5)], 6, 8.5, "gold", 3, "shield_rivet")
