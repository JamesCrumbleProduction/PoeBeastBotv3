from __future__ import annotations


import cv2

from numpy import ndarray
from typing import Iterator

from .parameters import (
    PORTAL_AREA_RADIUS,
    LOWER_RANGE_HSV_ARRAY_PORTAL,
    HIGHER_RANGE_HSV_ARRAY_PORTAL
)
from ...helpers import source_auto_update
from ....image_grabber import grab_screen, validate_region
from ....structure import Region, Coordinate


class HSVPortalScanner:

    __slots__ = (
        'region',
        '_hsv_mask',
        '_hsv_matrix',

        '_source_kwargs',
    )

    def __init__(self, region: Region = None) -> None:
        self.region = validate_region(region)
        self._hsv_mask: ndarray = None
        self._hsv_matrix: ndarray = None

        self._source_kwargs = dict()

    def __call__(self, /, as_custom_region: Region) -> HSVPortalScanner:
        self._source_kwargs['as_custom_region'] = as_custom_region
        return self

    @source_auto_update
    def iterate_by_each_founded(self) -> Iterator[Coordinate]:
        for contour in cv2.findContours(
            self._hsv_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )[0]:
            if cv2.contourArea(contour) > PORTAL_AREA_RADIUS:
                x, y, w, h = cv2.boundingRect(contour)
                yield Coordinate(
                    x=x + w // 2 + self.region.left,
                    y=y + h // 2 + self.region.top
                )

    def update_source(self, as_custom_region: Region = None) -> None:
        self._hsv_matrix = cv2.cvtColor(
            grab_screen(
                self.region if as_custom_region is None else as_custom_region
            ),
            cv2.COLOR_BGR2HSV
        )
        self._hsv_mask = cv2.inRange(
            self._hsv_matrix,
            LOWER_RANGE_HSV_ARRAY_PORTAL,
            HIGHER_RANGE_HSV_ARRAY_PORTAL
        )
