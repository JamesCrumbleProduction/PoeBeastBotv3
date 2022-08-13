from typing import Any

from .structure import ActionMeta
from .panel_data import MachineStatus, BEASTS_STATUSES
from ...settings import settings
from ...bot_components import bot
from ...server.components.from_hud.structure import LocationContent, CurrentLocation


class BotDataAdapter:

    __slots__ = (
        '_bot_instance'
    )

    def __init__(self, bot_instance: 'bot.Bot'):
        self._bot_instance = bot_instance

    @property
    def status(self) -> MachineStatus:
        return self._bot_instance.current_status

    @property
    def location(self) -> CurrentLocation | None:
        return self._bot_instance.location

    @property
    def content(self) -> LocationContent | None:
        return self._bot_instance.content

    def get_action(self) -> ActionMeta | None:
        return self._bot_instance.get_and_pop_action()

    def update_status(self, status: MachineStatus) -> None:
        if (
            settings.PARTY_ACCEPT_LOCK
            and self._bot_instance.current_status in BEASTS_STATUSES.values()
        ):
            return

        self._bot_instance.current_status = status

    def update_content(self, content: LocationContent) -> None:
        if self._bot_instance.current_status not in (
            MachineStatus.PAUSED,
            MachineStatus.FOUNDER_AVAILABLE
        ):
            self._bot_instance.content = content

    def update_location(self, location: CurrentLocation) -> None:
        self._bot_instance.location = location

    def add_action_to_execute(
        self,
        action: str,
        action_kwargs: dict[str, Any]
    ) -> None:
        self._bot_instance.add_action_to_execute(action, action_kwargs)
