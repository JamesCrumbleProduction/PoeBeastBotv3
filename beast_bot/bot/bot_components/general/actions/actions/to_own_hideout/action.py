import time

from typing import Iterator, Any

from .settings import settings
from ...actions_init import ACTIONS
from ...abstract_action import AbstractAction
from ....structure import ControlAction
from ....panel_data import MachineStatus
from ....bot_data_adapter import BotDataAdapter
from ....io_controllers import CommonIOController
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....world_to_screen import TemplateScanner

HELPER_ACTION_LABEL: str = 'EnterIntoPortal'


class ToOwnHideout(AbstractAction):
    '''Bot typing tp into own hideout if it's possible'''

    __slots__ = (
        '_stash_validator',
        '_permissions',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._stash_validator = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.nametags_templates.get('stash'),
            threshold=0.85
        )
        self._permissions = {
            MachineStatus.PAUSED,
            MachineStatus.FOUNDER_AVAILABLE
        }

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def _in_hideout(self) -> bool:
        if 'hideout' in self.bot_data_adapter.location.current_location.lower():
            return True
        return False

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield from super().execute_action()

        if self._in_hideout():
            CommonIOController.chat_text_command('/hideout')
        else:
            if enter_into_portal_action := ACTIONS.get(HELPER_ACTION_LABEL):
                for _ in enter_into_portal_action.action.execute_action():
                    ...

                while (
                    not self._in_hideout()
                    and not self._stash_validator.get_condition_by_one()
                ):
                    time.sleep(settings.LOCATION_CHECK_RATE)

                CommonIOController.chat_text_command('/hideout')
