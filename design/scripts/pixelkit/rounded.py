"""Pixel-art rounded shapes on the GUI pixel grid (2x2 art px) and bevel rings that follow them. Binary masks only."""
import numpy as np
from scipy import ndimage

# One corner recipe for every rounded shape, in GUI px: the first row loses 3 px, the next two rows 1 px each
# (a classic 3-1-1 corner; it is its own mirror image, so all four corners look alike).
CORNER = (3, 1, 1)


def rect(size, box):
    """Mask of `size` = (w, h) with a filled box (x0, y0, x1, y1)."""
    mask = np.zeros((size[1], size[0]), bool)
    mask[box[1]:box[3], box[0]:box[2]] = True
    return mask


def cut_corner(mask, x, y, sx, sy):
    """Round the corner whose outermost pixel is (x, y); (sx, sy) points into the shape."""
    for row, inset in enumerate(CORNER):
        py = y + sy * row
        columns = range(x, x + sx * inset, sx)
        for px in columns:
            mask[py, px] = False
    return mask


def round_box(mask, box):
    """Apply the corner recipe to the four corners of a box (x0, y0, x1, y1) inside `mask`."""
    x0, y0, x1, y1 = box
    for x, y, sx, sy in ((x0, y0, 1, 1), (x1 - 1, y0, -1, 1), (x0, y1 - 1, 1, -1), (x1 - 1, y1 - 1, -1, -1)):
        cut_corner(mask, x, y, sx, sy)
    return mask


def rounded_box(size, box):
    return round_box(rect(size, box), box)


def grow(mask, steps):
    """Dilate by `steps` px in the four directions (a diamond), so stairs stay stairs."""
    return ndimage.binary_dilation(mask, structure=ndimage.generate_binary_structure(2, 1), iterations=steps)


def upscale(mask, factor=2):
    return np.kron(mask, np.ones((factor, factor), bool)).astype(bool)


def rings(mask, inside):
    """Per pixel: (ring number from the edge, 1 = touching it; lit side). `inside` numbers the mask's own pixels
    inward from its edge, otherwise the pixels outside it outward. Distances count steps along rows and columns,
    so rings follow stairs. A pixel is on the top-left side when its outward direction points up or left; the
    diagonal splits so the top edge's colour runs round the top corners."""
    ys, xs = np.mgrid[0:mask.shape[0], 0:mask.shape[1]]
    if inside:
        padded = np.pad(mask, 1)
        dist, (iy, ix) = ndimage.distance_transform_cdt(padded, metric="taxicab", return_indices=True)
        dist, iy, ix = dist[1:-1, 1:-1], iy[1:-1, 1:-1] - 1, ix[1:-1, 1:-1] - 1
        oy, ox = iy - ys, ix - xs
        wanted = mask
    else:
        dist, (iy, ix) = ndimage.distance_transform_cdt(~mask, metric="taxicab", return_indices=True)
        oy, ox = ys - iy, xs - ix
        wanted = ~mask
    total = ox + oy
    lit = (total < 0) | ((total == 0) & (oy < 0))
    return np.where(wanted, dist, 0), lit
