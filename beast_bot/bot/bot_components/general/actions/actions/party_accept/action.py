import time

from typing import Iterator, Any

from .settings import settings as action_settings
from ...abstract_action import AbstractAction
from ....structure import ControlAction
from ....bot_data_adapter import BotDataAdapter
from ....io_controllers import CommonIOController
from ....world_to_screen import TemplateScanner
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....panel_data import MachineStatus, BEASTS_STATUSES


class PartyAccept(AbstractAction):
    '''
    Bot trying to find accept button and press it
    '''

    __slots__ = (
        '_permissions',
        '_activate_validator',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._activate_validator = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.buttons_templates.get('accept'),
            threshold=0.75
        )
        self._permissions = {
            MachineStatus.PAUSED,
            MachineStatus.FOUNDER_AVAILABLE,
            MachineStatus.IDLE_MEMBER,
            *BEASTS_STATUSES.values()
        }

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield from super().execute_action()

        if coordinate := self._activate_validator.indentify_by_first():
            CommonIOController.move_and_click(coordinate)

            time.sleep(action_settings.AWAIT_TO_CHECK_CONDITION_INTERVAL)

            if self._activate_validator.get_condition_by_one() is False:
                yield ControlAction.DONE
