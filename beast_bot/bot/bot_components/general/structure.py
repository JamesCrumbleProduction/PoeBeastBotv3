from enum import Enum
from typing import Any
from pydantic import BaseModel

from .world_to_screen import Coordinate, Region

# That means, method gives control as iterator before executing main action of method
class ControlAction(Enum):
    EXIT: str = 'EXIT'
    DONE: str = 'DONE'
    ActionType: str = 'ActionType'  # Means nothing will happening
    STOP_ACTION: str = 'STOP_ACTION'


class ActionMeta(BaseModel):

    action_label: str
    action_kwargs: dict[str, Any]

class MapTabs(BaseModel):
    first_map_tab: Coordinate = Coordinate(
        x=100,
        y=60,
    )
    second_map_tab: Coordinate = Coordinate(
        x=134,
        y=60
    )
    third_map_tab: Coordinate = Coordinate(
        x=167,
        y=60
    )
    fourth_map_tab: Coordinate = Coordinate(
        x=200,
        y=60
    )
    fifth_map_tab: Coordinate = Coordinate(
        x=234,
        y=60
    )

    def __iter__(self):
        yield self.first_map_tab
        yield self.second_map_tab
        yield self.third_map_tab
        yield self.fourth_map_tab
        yield self.fifth_map_tab
class ScarabTabs(BaseModel):
    first_scarab_tab: Coordinate = Coordinate(
        x=267,
        y=60
    )
    def __iter__(self):
        yield self.first_scarab_tab

class Stash(BaseModel):
    map_tabs: MapTabs = MapTabs()
    scarab_tabs: scarab_tabs = ScarabTabs()

class Coordinates(BaseModel):
    stash: Stash = Stash()
    first_socket_inventory_position: Coordinate = Coordinate(
        x=455,
        y=342
    )
    sockets_gap: Coordinate = Coordinate(
        x=19,
        y=28
    )
    activate_map_device_button: Coordinate = Coordinate(
        x=145,
        y=460
    )

        

class Regions(BaseModel):
    stash_region: Region = Region(
        left=7,
        top=68,
        width=360,
        height=420
    )
    map_device_sockets_region: Region = Region(
        left=114,
        top=377,
        width=176,
        height=439
    )
    portals_region: Region = Region(
        left=0,
        top=0,
        width=800,
        height=510
    )
    inventory_region: Region = Region(
        left=437,
        top=324,
        width=793,
        height=475
    )
