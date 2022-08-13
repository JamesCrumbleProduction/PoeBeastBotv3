import numpy as np


PORTAL_AREA_RADIUS = 3000
# [Hmin, Smin, Vmin]
LOWER_RANGE_HSV_ARRAY_PORTAL = np.array(
    [92, 201, 69],
    dtype=np.uint8, copy=False
)
# [Hmax, Smax, Vmax]
HIGHER_RANGE_HSV_ARRAY_PORTAL = np.array(
    [150, 255, 255],
    dtype=np.uint8, copy=False
)
