"""The Archer: slim and diagonal. Pointed hood, a long recurve bow at full draw, quiver and cloak tail."""
import numpy as np

from .figure import Figure, block_eye, grid_detail
from .hullrig import Rig, box, euler, prism, slab

HEAD_CENTRE = np.array((5.0, 114.0, 4.0))
HEAD_TURN = euler(yaw=14, pitch=2, roll=-2)
DRAW_HAND = (-17.0, 87.0, 24.0)
BOW_HAND = (52.0, 89.0, 14.0)
# bow limbs from the grip outward: (x, y, z, thickness)
BOW_UPPER = [(53, 89, 13, 9), (55, 111, 11, 8), (47, 134, 7, 7), (35, 151, 3, 6), (36, 163, 2, 4)]
BOW_LOWER = [(53, 89, 13, 9), (55, 67, 14, 8), (47, 44, 15, 7), (35, 27, 16, 6), (37, 15, 16, 4)]


def build(facing=1):
    rig = Rig(yaw=24.0, pitch=10.0, scale=0.87)
    _cloak(rig)
    _quiver(rig)
    _legs(rig)
    _body(rig)
    _head(rig)
    _arms(rig)
    _bow_and_arrow(rig)
    details = []
    for x, mirrored in ((-6.5, False), (9.0, True)):
        anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 0.5, 18.5))
        details.append(grid_detail(block_eye("w", "i", "p", mirrored), EYES, anchor))
    for x, mirrored in ((-6.5, False), (9.0, True)):
        brow = ["bbbbb....", "..bbbbbbb"]
        anchor = HEAD_CENTRE + HEAD_TURN @ np.array((x, 5.5, 18.5))
        details.append(grid_detail([r[::-1] for r in brow] if mirrored else brow, BROWS, anchor))
    return Figure(rig, lean=-3.0, facing=facing,
                  blocky=("bow", "cloakhem", "hoodpoint", "feather"),
                  rim={"forest": ("forest", 4), "leather": ("leather", 4)},
                  no_rim=("bow", "arrow", "string", "vane", "nockvane", "cloak"), details=details)


EYES = {"w": ("ivory", 4), "i": ("forest", 4), "p": ("forest", 1)}
BROWS = {"b": ("leather", 0)}


def _legs(rig):
    # a deep lunge: the front knee bent over its foot, the back leg stretched out behind
    legs = (("leg_back", (-47, 0, -4), (-30, 28, -2), (-9, 54, 0), -14),
            ("leg_front", (30, 0, 12), (28, 32, 15), (9, 54, 2), 18))
    for group, foot, knee, hip, toe_yaw in legs:
        turn = euler(yaw=toe_yaw)
        foot = np.array(foot, float)

        def boot(points, material, base, local, name):
            rig.add(points + np.array(local, float), material, base, group + name, foot, turn)

        boot(box(19, 5, 31, 1.5), "leather", 1, (0, 2.5, 4), "_sole")
        boot(slab((17, 25), (15, 18), 11, 1.5), "leather", 2, (0, 9, 2), "_boot")
        ankle = foot + np.array((0, 13, 0))
        rig.bone(ankle, knee, (13, 14), (16, 17), "leather", 3, group + "_shin", 1.5)
        cuff = np.array(knee) * 0.8 + ankle * 0.2
        rig.bone(cuff + (0, -3, 0), cuff + (0, 4, 0), (19, 20), (20, 21), "leather", 3, group + "_cuff", 1.5)
        rig.bone(knee, hip, (14, 15), (16, 17), "leather", 1, group + "_thigh", 1.5, lo=1)
        rig.add(box(11, 10, 7, 2), "forest", 3, group + "_knee", (knee[0], knee[1] + 1, knee[2] + 9),
                euler(yaw=toe_yaw * 0.6))


def _cloak(rig):
    """A short cloak thrown back by the draw: two flaring panels with a ragged, stair-stepped hem."""
    rig.add(prism([(-20, 99), (12, 99), (-14, 58), (-38, 62)], -24, -17), "forest", 2, "cloak")
    rig.add(prism([(-38, 62), (-14, 58), (-48, 44), (-58, 54)], -26, -19), "forest", 1, "cloakhem")
    rig.add(prism([(-20, 70), (-4, 74), (-22, 44), (-34, 48)], -24, -18), "forest", 1, "cloakhem")


def _quiver(rig):
    foot, mouth = np.array((-14.0, 66.0, -24.0)), np.array((-43.0, 109.0, -10.0))
    rig.bone(foot, mouth, (14, 14), (18, 18), "leather", 2, "quiver", 2)
    along = (mouth - foot) / np.linalg.norm(mouth - foot)
    rig.bone(mouth - along * 3, mouth + along * 2, (21, 21), (21, 21), "leather", 4, "quiverband", 1.5)
    # three separate arrows, fanned so that sky shows between their feathers
    for index, end in enumerate(((-45.0, 134.0, -6.0), (-60.0, 125.0, -6.0), (-65.0, 108.0, -6.0))):
        end = np.array(end)
        direction = (end - mouth) / np.linalg.norm(end - mouth)
        side = np.array((direction[1], -direction[0], 0.0)) / np.linalg.norm(direction[:2])
        rig.bone(mouth, end, (3, 3), (3, 3), "leather", 4, "arrowshaft", 0.5)
        for sign, step in ((1, 3), (-1, 2)):
            vane = [end + direction * 3, end - direction * 7, end - direction * 11 + side * sign * 5,
                    end - direction * 1 + side * sign * 5]
            points = [p + (0, 0, z) for p in vane for z in (-1.5, 1.5)]
            rig.solid(points, "parchment", step, f"vane{index}")


def _body(rig):
    rig.add(slab((31, 23), (30, 22), 11, 1.5), "leather", 1, "hips", (0, 55, 0))
    # split tunic skirt with a pale hem
    for side, drop in ((-1, 0), (1, 3)):
        outline = [(0, 62), (side * 19, 62), (side * 24, 43 - drop), (side * 3, 38 - drop)]
        rig.add(prism(outline, 8, 15), "forest", 3 if side < 0 else 2, f"skirt{side}")
        hem = [(side * 24, 43 - drop), (side * 3, 38 - drop), (side * 3, 41 - drop), (side * 23, 46 - drop)]
        rig.add(prism(hem, 14, 16), "parchment", 2, f"skirt{side}")
    rig.add(slab((33, 25), (34, 26), 7, 1.5), "leather", 2, "belt", (0, 63, 0))
    rig.add(box(9, 9, 4, 1), "gold", 3, "buckle", (2, 63, 14))
    rig.add(box(12, 14, 9, 2), "leather", 3, "pouch", (-15, 58, 15))
    rig.add(box(14, 4, 10, 1), "leather", 2, "pouchflap", (-15, 65, 15.5))
    rig.add(slab((30, 23), (43, 28), 31, 2.5), "forest", 3, "chest", (0, 81, 0))
    # leather jerkin panel and the quiver strap across it
    rig.add(prism([(-11, 94), (11, 94), (9, 68), (-9, 68)], 10, 16), "leather", 3, "jerkin")
    rig.add(prism([(-17, 96), (-10, 97), (15, 70), (9, 67)], 15, 18), "leather", 1, "strap")
    rig.add(box(6, 6, 3, 1), "gold", 3, "strapstud", (-2, 83, 18.5))
    # hood collar: a short mantle over the shoulders with a pointed front
    rig.add(slab((50, 33), (36, 29), 10, 2), "forest", 2, "mantle", (0, 98, -1))
    rig.add(prism([(-15, 96), (15, 96), (1, 82)], 13, 19), "forest", 3, "mantlepoint")


def _head(rig):
    def put(points, material, base, group, local, **kw):
        rig.add(points + np.array(local, float), material, base, group, HEAD_CENTRE, HEAD_TURN, **kw)

    put(box(31, 31, 28, 1.5), "skin", 3, "face", (0, -1, 4))
    # scarf over nose and chin
    put(box(33, 12, 8, 1.5), "forest", 1, "scarf", (0, -12, 17))
    fold = [(-16, -6), (0, -9), (16, -6), (14, -8.5), (0, -12), (-14, -8.5)]
    put(prism(fold, 20, 22), "forest", 2, "scarf", (0, 0, 0))
    # fringe under the hood
    put(prism([(-16, 15), (16, 15), (16, 9), (6, 11), (2, 7), (-6, 11), (-16, 7)], 16, 20), "leather", 2, "hair",
        (0, 0, 0))
    # boxy hood: cheek flaps, back, roof and a peak over the brow
    for side in (-1, 1):
        put(prism([(-3.5, -18), (3.5, -18), (3.5, 17), (-3.5, 17)], -18, 20), "forest", 2, "hood", (side * 19, 0, 0))
    put(box(42, 40, 9, 1.5), "forest", 2, "hood", (0, 0, -17))
    put(box(45, 9, 42, 2), "forest", 2, "hood", (0, 20, 0))
    put(prism([(-23, 16), (23, 16), (23, 20), (0, 25), (-23, 20)], 18, 25), "forest", 4, "hoodpeak", (0, 0, 0))
    put(prism([(-20, 14), (20, 14), (20, 16.5), (-20, 16.5)], 23, 25.5), "parchment", 1, "hoodpeak", (0, 0, 0))
    # the roof rises into a long point that flops backward: the hood reads in solid black
    point = [(-22, 23, 16), (22, 23, 16), (-22, 23, -18), (16, 23, -18), (-14, 34, -2), (-40, 45, -22)]
    rig.add(point, "forest", 2, "hoodpoint", HEAD_CENTRE, HEAD_TURN)
    # a fold down the hood side breaks up the large lit plane
    put(prism([(-3, -16), (1, -16), (3, 14), (-3, 8)], -8, 2), "forest", 1, "hood", (-22, 0, 0))
    # a pale feather tucked into the band
    feather = [(-22, 10), (-26, 17), (-45, 25), (-38, 15)]
    put(prism(feather, 8, 11), "parchment", 3, "feather", (0, 0, 0))
    put(box(5, 5, 5, 1), "gold", 3, "hoodpin", (-23, 15, 0))


def _arms(rig):
    # bow arm: stretched out straight toward the centre
    shoulder, elbow, hand = (17, 93, 1), (34, 90, 8), BOW_HAND
    rig.bone(shoulder, elbow, (16, 17), (13, 14), "forest", 3, "bowarm_up", 1.5)
    rig.bone(elbow, hand, (14, 15), (12, 13), "leather", 3, "bowarm_fore", 1.5)
    rig.add(box(13, 13, 13, 1.5), "skin", 3, "bowfist", BOW_HAND)
    # draw arm: the elbow high and far back, the hand anchored under the jaw
    shoulder, elbow = (-18, 93, 2), (-54, 90, 10)
    rig.bone(shoulder, elbow, (16, 17), (14, 15), "forest", 3, "drawarm_up", 1.5)
    rig.bone(elbow, (-23, 87, 23), (15, 16), (12, 13), "leather", 3, "drawarm_fore", 1.5)
    rig.bone((-49, 89, 13), (-39, 88, 17), (18, 19), (17, 18), "leather", 2, "bracer", 1.5)
    rig.add(box(12, 12, 12, 1.5), "skin", 3, "drawfist", DRAW_HAND)
    for side, at in ((-1, (-20, 96, 2)), (1, (20, 96, 2))):
        rig.add(slab((19, 22), (14, 17), 10, 2), "leather", 3, f"shoulder{side}", at, euler(roll=-side * 14))


def _bow_and_arrow(rig):
    for limb in (BOW_UPPER, BOW_LOWER):
        for index, (a, b) in enumerate(zip(limb, limb[1:])):
            ramp, step = ("gold", 3) if index == 3 else ("leather", 3)
            rig.bone(a[:3], b[:3], (a[3], a[3]), (b[3], b[3]), ramp, step, "bow", 1)
    rig.add(box(12, 20, 12, 1.5), "forest", 2, "bowgrip", (53, 89, 13))
    # the string runs behind the head, so it never crosses the face
    nock = (DRAW_HAND[0] - 2, DRAW_HAND[1], 8)
    rig.bone(BOW_UPPER[-1][:3], nock, (2.2, 2.2), (2.2, 2.2), "ivory", 1, "string", 0.4, lo=1)
    # the lower half runs in front of the body, so the pair reads as one drawn string
    low = (DRAW_HAND[0] + 1, DRAW_HAND[1] - 4, 30)
    rig.bone(BOW_LOWER[-1][:3], low, (2.2, 2.2), (2.2, 2.2), "ivory", 1, "string", 0.4, lo=1)
    rig.bone((-24, 87, 27), (66, 89, 23), (4, 4), (4, 4), "leather", 4, "arrow", 1)
    head = [(60, 97), (80, 89), (60, 81), (66, 89)]
    rig.add(prism([head[0], head[1], head[3]], 21, 25), "steel", 5, "arrowhead")
    rig.add(prism([head[3], head[1], head[2]], 21, 25), "steel", 3, "arrowhead")
    # the nock end sticks out behind the draw hand
    for sign, step in ((1, 3), (-1, 2)):
        vane = [(-24, 87), (-31, 87), (-37, 87 + sign * 6), (-30, 87 + sign * 6)]
        rig.add(prism(vane, 28, 30), "parchment", step, "nockvane")
