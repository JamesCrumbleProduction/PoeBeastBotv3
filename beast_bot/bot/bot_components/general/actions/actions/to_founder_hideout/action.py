import time

from typing import Iterator, Any

from .structure import Machine
from ...actions_init import ACTIONS
from ...abstract_action import AbstractAction
from ....structure import ControlAction
from ....bot_data_adapter import BotDataAdapter
from ....io_controllers import CommonIOController
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....world_to_screen import TemplateScanner
from ....panel_data import MachineStatus, BEASTS_STATUSES, EXTENDED_MODE
from ....requests_controller import (
    Routes,
    Service,
    RequestsController,
)

TO_PORTAL_ACTION: str = 'EnterIntoPortal'


class ToFounderHideout(AbstractAction):
    '''Bot typing tp into founder hideout if it's possible'''

    __slots__ = (
        '_permissions',
        '_loading_screen_to_map_validator',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._permissions = {
            MachineStatus.PAUSED,
            MachineStatus.IDLE_MEMBER,
            MachineStatus.FOUNDER_AVAILABLE
        }
        self._loading_screen_to_map_validator = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'to_map_loading_screen'
            ), threshold=0.8
        )

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def _chat_command(self, founder_name: str) -> None:
        CommonIOController.chat_text_command(
            f'/hideout {founder_name}'
        )

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield from super().execute_action()

        if founder := action_kwargs.get('founder'):
            self._chat_command(founder)

            # Actually never get kwargs about founder except of EXTENDED MODE
            if EXTENDED_MODE:
                # Important couse it's basically loading time to hideout
                time.sleep(1.5)

                if portal_action := ACTIONS.get(TO_PORTAL_ACTION):
                    while (
                        self._loading_screen_to_map_validator.get_condition_by_one()
                    ) is False:
                        for action in portal_action.action.execute_action():
                            if action is ControlAction.DONE:
                                yield ControlAction.DONE

                        time.sleep(0.3)

        machines_raw_data = RequestsController.execute(
            Service.LINKING_SERVER,
            Routes.LinkingServer.Control.available_machines,
            serialize=True
        )
        worker_machines: list[Machine] = list(
            Machine(**raw_machine_data)
            for raw_machine_data in machines_raw_data
        )

        for machine in worker_machines:
            if machine.status in BEASTS_STATUSES.values():
                self._chat_command(machine.name)
                if not EXTENDED_MODE:
                    yield ControlAction.DONE
