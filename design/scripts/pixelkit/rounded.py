"""Rounded, stepped silhouettes and bevel rings that follow them. Hard edges only, binary masks."""
import numpy as np
from scipy import ndimage


def disk(radius):
    """Even-sized disk centred on a pixel corner, so opening a rectangle gives exactly `rounded_rect`'s corners."""
    ys, xs = np.mgrid[-radius:radius, -radius:radius] + 0.5
    return xs * xs + ys * ys <= radius * radius


def rounded_rect(size, radius):
    """Filled rectangle `size` = (w, h) with quarter-circle corners; pixel centres decide, so the curve steps."""
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w]
    cx = np.clip(xs + 0.5, radius, w - radius)
    cy = np.clip(ys + 0.5, radius, h - radius)
    return (xs + 0.5 - cx) ** 2 + (ys + 0.5 - cy) ** 2 <= radius * radius


def round_convex(mask, radius):
    return ndimage.binary_opening(mask, structure=disk(radius))


def round_concave(mask, radius):
    return ndimage.binary_closing(mask, structure=disk(radius))


def rings(mask, inside):
    """Per pixel: (ring number from the edge, 1 = touching it; lit side). `inside` numbers the mask's own pixels
    inward from its edge, otherwise the pixels outside it outward. A pixel is on the top-left (lit) side when its
    outward direction points up or left; the diagonal splits so the top edge's colour runs round the top corners."""
    ys, xs = np.mgrid[0:mask.shape[0], 0:mask.shape[1]]
    if inside:
        padded = np.pad(mask, 1)
        dist, (iy, ix) = ndimage.distance_transform_edt(padded, return_indices=True)
        dist, iy, ix = dist[1:-1, 1:-1], iy[1:-1, 1:-1] - 1, ix[1:-1, 1:-1] - 1
        oy, ox = iy - ys, ix - xs
        wanted = mask
    else:
        dist, (iy, ix) = ndimage.distance_transform_edt(~mask, return_indices=True)
        oy, ox = ys - iy, xs - ix
        wanted = ~mask
    total = ox + oy
    lit = (total < 0) | ((total == 0) & (oy < 0))
    number = np.where(wanted, np.ceil(dist).astype(int), 0)
    return number, lit
