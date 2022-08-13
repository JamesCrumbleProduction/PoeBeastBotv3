from __future__ import annotations


import cv2
import numpy as np

from numpy import ndarray
from typing import Iterator, Iterable

from ...helpers import source_auto_update
from ....image_grabber import grab_screen, validate_region
from ....structure import (
    Region,
    Coordinate,
    ValidatedTemplateData
)
from .....templates import CompiledTemplate


class TemplateScanner:

    __slots__ = (
        'region',
        'templates',
        'threshold',

        '_image_rgb',
        '_source_kwargs',
    )

    def __init__(
        self,
        *compiled_templates: CompiledTemplate,
        iterable_templates: Iterable[CompiledTemplate] = list(),
        region: Region = None,
        threshold: int = 1
    ):
        assert 0 < threshold <= 1

        self.region = validate_region(region)
        self.threshold = threshold
        self.templates = [*compiled_templates, *iterable_templates]

        self._image_rgb: ndarray = None
        self._source_kwargs = dict()

    def __call__(self, /, as_custom_region: Region) -> TemplateScanner:
        self._source_kwargs['as_custom_region'] = as_custom_region
        return self

    @source_auto_update
    def iterate_one_by_each_founded(self) -> Iterator[Coordinate]:
        for coordinate in self._rectangles_group_by(
            self._validate_template(self.templates[0])
        ):
            yield coordinate

    @source_auto_update
    def iterate_all_by_first_founded(self) -> Iterator[Coordinate | None]:
        for template in self.templates:
            if template_data := self._validate_template(template):
                yield Coordinate(
                    x=(
                        template_data.location_x[0]
                        + template_data.width//2
                        + self.region.left
                    ),
                    y=(
                        template_data.location_y[0]
                        + template_data.height//2
                        + self.region.top
                    )
                )
            else:
                # saving iteration template order
                yield None

    @source_auto_update
    def iterate_all_by_each_founded(self) -> Iterator[Coordinate]:
        for coordinate in self._rectangles_group_by((
            self._validate_template(template)
            for template in self.templates
        )):
            yield coordinate

    @source_auto_update
    def indentify_by_first(self) -> Coordinate | None:
        if template_data := self._validate_template(self.templates[0]):
            return Coordinate(
                x=(
                    template_data.location_x[0]
                    + template_data.width//2
                    + self.region.left
                ),
                y=(
                    template_data.location_y[0]
                    + template_data.height//2
                    + self.region.top
                )
            )

    @source_auto_update
    def get_condition_by_one(self) -> bool:
        for coordinate in self.iterate_all_by_first_founded():
            if coordinate is not None:
                return True

        return False

    def update_source(self, as_custom_region: Region = None) -> None:
        self._image_rgb = cv2.cvtColor(
            grab_screen(
                self.region if as_custom_region is None else as_custom_region
            ),
            cv2.COLOR_BGR2RGB
        )

    def _validate_template(
        self, template: CompiledTemplate
    ) -> ValidatedTemplateData | None:
        height, width = template.template_data.shape[:-1]
        res = cv2.matchTemplate(
            self._image_rgb,
            template.template_data,
            cv2.TM_CCOEFF_NORMED
        )
        location_y, location_x = np.where(res >= self.threshold)

        if location_y.size > 0 and location_x.size > 0:
            return ValidatedTemplateData(
                location_x=location_x,
                location_y=location_y,
                height=height,
                width=width
            )

    def _rectangles_group_by(self, templates_data: Iterable[ValidatedTemplateData | None]) -> Iterator[Coordinate]:
        rectangles = list()

        for template_data in templates_data:
            if template_data is not None:

                for x, y in zip(template_data.location_x, template_data.location_y):
                    rectangles.extend([
                        [
                            int(x) + template_data.width//2 +
                            self.region.left,
                            int(y) + template_data.height//2 +
                            self.region.top,
                            template_data.width,
                            template_data.height
                        ],
                        [
                            int(x) + template_data.width//2 +
                            self.region.left,
                            int(y) + template_data.height//2 +
                            self.region.top,
                            template_data.width,
                            template_data.height
                        ]
                    ])

        for x, y, *_ in cv2.groupRectangles(rectangles, 1, 0.8)[0]:
            yield Coordinate(x=x, y=y)
