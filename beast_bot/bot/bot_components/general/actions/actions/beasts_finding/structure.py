from enum import Enum

from ....world_to_screen import Coordinate


class StashTab(Enum):
    MAPS: str = 'MAPS'
    SCARABS: str = 'SCARABS'


class TabMeta:

    __slots__ = (
        '_index',
        '_coordinates',
        '_tab_content',
    )

    def __init__(self, *coordinates: Coordinate) -> None:
        self._index = 0
        self._tab_content: list[Coordinate] = None
        self._coordinates: list[Coordinate] = coordinates

    @property
    def tab(self) -> Coordinate | None:
        if not self._tab_content and self._tab_content is not None:
            self._index += 1

        if self._index < len(self._coordinates):
            return self._coordinates[self._index]

    @property
    def tab_content(self) -> list[Coordinate]:
        return self._tab_content

    @tab_content.setter
    def tab_content(self, content: list[Coordinate]) -> None:
        self._tab_content = content
