
from __future__ import annotations

import httpx
import orjson

from math import isnan
from typing import Any
from typing import Iterator

# from ..helpers import source_auto_update
from .structure import (
    Entity,
    Coordinate,
)
# from ....requests_controller import (
#     Routes,
#     Service,
#     RequestsController,
# )
from ......settings import settings


class ShareDataConnector:

    _instance: ShareDataConnector = None

    def __init__(self):
        self._source_kwargs = dict()
        self._share_data_content: dict[str, dict[str, Any]] = dict()

    def __call__(self) -> ShareDataConnector:
        '''Not implemented (actually nothing to do with custom arguments)'''
        return self

    def update_source(self) -> None:
        sds = settings.SHARE_DATA_SERVICE
        url = f'{sds.SCHEME}127.0.0.1:{sds.PORT}/get_content'

        with httpx.Client() as client:
            resp = client.get(url)
            if resp.status_code != 200:
                raise ValueError('resp is not 200 status code')

            self._share_data_content = orjson.loads(resp.text)

    def _iterate_by_portal_entity(self) -> Iterator[Entity]:
        self.update_source()
        if on_ground_content := self._share_data_content.get('items_on_ground_label'):

            for raw_entity in on_ground_content:
                raw_entity: str

                if settings.SHARE_DATA_SERVICE.PORTAL_PREFIX in raw_entity:
                    yield Entity(**on_ground_content[raw_entity])

    def iterate_by_each_founded_portal(self) -> Iterator[Coordinate]:
        self.update_source()
        for portal_entity in self._iterate_by_portal_entity():
            if not isnan(portal_entity.on_screen_position.x):
                yield portal_entity.screen_coordinate()

    def get_closest_portal(self) -> Coordinate | None:
        self.update_source()
        closest_portal_entity: Entity = None

        for portal_entity in self._iterate_by_portal_entity():
            if not isnan(portal_entity.on_screen_position.x):
                if closest_portal_entity is None:
                    closest_portal_entity = portal_entity

                if portal_entity.distance_to_player < closest_portal_entity.distance_to_player:
                    closest_portal_entity = portal_entity

        if closest_portal_entity is not None:
            return closest_portal_entity.screen_coordinate()

    def get_current_location(self) -> str | None:
        self.update_source()
        return self._share_data_content.get('current_location')

    def get_location_content(self) -> list[str] | None:
        self.update_source()
        return self._share_data_content.get('location_content')
