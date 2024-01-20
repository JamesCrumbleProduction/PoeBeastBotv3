from enum import Enum
from typing import Any
from pydantic import BaseModel

from .helpers import static_dataclass
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


@static_dataclass
class Coordinates:

    @static_dataclass
    class Stash:

        @static_dataclass
        class MapTabs:
            first_map_tab = Coordinate(
                x=100,
                y=60,
            )
            second_map_tab = Coordinate(
                x=134,
                y=60
            )
            third_map_tab = Coordinate(
                x=167,
                y=60
            )
            fourth_map_tab = Coordinate(
                x=200,
                y=60
            )
            fifth_map_tab = Coordinate(
                x=234,
                y=60
            )

        @static_dataclass
        class ScarabTabs:
            first_scarab_tab = Coordinate(
                x=267,
                y=60
            )

    first_socket_inventory_position = Coordinate(
        x=455,
        y=342
    )
    sockets_gap = Coordinate(
        x=19,
        y=28
    )
    activate_map_device_button = Coordinate(
        x=145,
        y=460
    )


@static_dataclass
class Regions:
    stash_region = Region(
        left=7,
        top=68,
        width=360,
        height=420
    )
    map_device_sockets_region = Region(
        left=114,
        top=377,
        width=176,
        height=439
    )
    portals_region = Region(
        left=0,
        top=0,
        width=800,
        height=510
    )
    inventory_region = Region(
        left=437,
        top=324,
        width=793,
        height=475
    )
