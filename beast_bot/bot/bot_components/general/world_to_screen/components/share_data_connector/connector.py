
from __future__ import annotations


from math import isnan
from typing import Any
from typing import Iterator

from ..helpers import source_auto_update
from .structure import (
    Entity,
    Coordinate,
)
from ....requests_controller import (
    Routes,
    Service,
    RequestsController,
)
from ......settings import settings


class ShareDataConnector:

    _instance: ShareDataConnector = None

    def __new__(cls: type[ShareDataConnector], *args, **kwargs) -> ShareDataConnector:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._source_kwargs = dict()
            cls._instance._share_data_content = dict()

        return cls._instance

    def __call__(self) -> ShareDataConnector:
        '''Not implemented (actually nothing to do with custom arguments)'''
        return self

    def update_source(self) -> None:

        if content := RequestsController.execute(
            Service.SHARE_DATA,
            Routes.ShareData.get_content,
            serialize=True
        ):
            self._share_data_content: dict[str, dict[str, Any]] = content
        else:
            self._share_data_content = dict()

    def _iterate_by_portal_entity(self) -> Iterator[Entity]:
        if on_ground_content := self._share_data_content.get('items_on_ground_label'):

            for raw_entity in on_ground_content:
                raw_entity: str

                if settings.SHARE_DATA_SERVICE.PORTAL_PREFIX in raw_entity:
                    yield Entity(**on_ground_content[raw_entity])

    @source_auto_update
    def iterate_by_each_founded_portal(self) -> Iterator[Coordinate]:
        for portal_entity in self._iterate_by_portal_entity():
            if not isnan(portal_entity.on_screen_position.x):
                yield portal_entity.screen_coordinate()

    def get_closest_portal(self) -> Coordinate | None:
        closest_portal_entity: Entity = None

        for portal_entity in self._iterate_by_portal_entity():
            if not isnan(portal_entity.on_screen_position.x):
                if closest_portal_entity is None:
                    closest_portal_entity = portal_entity

                if portal_entity.distance_to_player < closest_portal_entity.distance_to_player:
                    closest_portal_entity = portal_entity

        if closest_portal_entity is not None:
            return closest_portal_entity.screen_coordinate()

    @source_auto_update
    def get_current_location(self) -> str | None:
        return self._share_data_content.get('current_location')

    @source_auto_update
    def get_location_content(self) -> list[str] | None:
        return self._share_data_content.get('location_content')
