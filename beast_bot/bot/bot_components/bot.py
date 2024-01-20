from typing import Any

from .exceptions import BotMainActionError
from .general.panel_data import MachineStatus
from .general.bot_data_adapter import BotDataAdapter
from .general.sleep_controller import SleepController
from .general.actions import ACTIONS, ExecutableAction
from .general.structure import ControlAction, ActionMeta
from .general.requests_controller import (
    Routes,
    Service,
    RequestsController,
)

from ..settings import settings
from ..services.logger import BOT_LOGGER
from ..server.components.from_hud.structure import LocationContent, CurrentLocation


MAIN_ACTION_LABEL: str = (
    'KingOfTheMistsFinding'
    if settings.IS_PARTY_MEMBER is False
    else 'PartyMembering'
)


class Bot:

    __slots__ = (
        '_main_action',
        '_data_adapter',
        '_current_status',
        '_sleep_controller',
        '_current_location',
        '_location_content',
        '_actions_for_executing',
    )

    def __init__(self):
        self._main_action: ExecutableAction = None
        self._actions_for_executing: list[ActionMeta] = list()

        self._data_adapter = BotDataAdapter(self)
        self._sleep_controller = SleepController(self.data_adapter)

        self._current_status: MachineStatus = None
        self._current_location: CurrentLocation = None
        self._location_content: LocationContent = None

        self._init_actions()
        self._register_machine()

        BOT_LOGGER.info('Data inited and bot is on pause...')

    @property
    def data_adapter(self) -> BotDataAdapter:
        return self._data_adapter

    @property
    def actions_for_executing(self) -> list[ActionMeta]:
        return self._actions_for_executing

    @property
    def content(self) -> LocationContent | None:
        return self._location_content

    @property
    def location(self) -> CurrentLocation | None:
        return self._current_location

    @property
    def current_status(self) -> MachineStatus:
        return self._current_status

    @content.setter
    def content(self, content: LocationContent) -> None:
        self._location_content = content

    @location.setter
    def location(self, location: CurrentLocation) -> None:
        self._current_location = location

    @current_status.setter
    def current_status(self, status: MachineStatus) -> None:
        self._current_status = status
        RequestsController.execute_in_thread(
            Service.LINKING_SERVER,
            Routes.LinkingServer.Control.update_machine_status,
            params={
                'vm_name': settings.VM_NAME,
                'register_status': status.value
            }
        )

    def _init_actions(self) -> None:

        for action_label, executable_action in ACTIONS.items():
            if action_label == MAIN_ACTION_LABEL:
                self._main_action = executable_action.init_action(
                    self._data_adapter
                )
                continue

            ACTIONS[action_label] = executable_action.init_action(
                self._data_adapter
            )

        if self._main_action is None:
            raise BotMainActionError(
                f'Cannot find main "{MAIN_ACTION_LABEL}" action...'
            )

        del ACTIONS[MAIN_ACTION_LABEL]

    def _register_machine(self) -> None:
        self._current_status = (
            MachineStatus.IDLE_MEMBER
            if settings.IS_PARTY_MEMBER
            else MachineStatus.PAUSED
        )
        RequestsController.execute(
            Service.LINKING_SERVER,
            Routes.LinkingServer.Control.register_machine,
            params={
                'vm_name': settings.VM_NAME,
                'port': settings.BOT_SERVER.PORT,
                'as_party_machine': settings.IS_PARTY_MEMBER
            }
        )

    def _in_actions_for_executing(self, action_label: str) -> bool:
        for action_meta in self._actions_for_executing:
            if action_meta.action_label == action_label:
                return True

        return False

    def add_action_to_execute(
        self,
        action_label: str,
        action_kwargs: dict[str, Any]
    ) -> None:
        if action := ACTIONS.get(action_label):
            if (
                action.excecutable_from_server is True
                and not self._in_actions_for_executing(action_label)
            ):
                self._actions_for_executing.insert(0, ActionMeta(
                    action_label=action_label,
                    action_kwargs=action_kwargs
                ))

    def get_and_pop_action(self) -> ActionMeta | None:
        if self.actions_for_executing:
            return self.actions_for_executing.pop()

    def run(self) -> None:
        while True:
            for action in self._main_action.action.execute_action():
                if action is ControlAction.EXIT:
                    return

                self._sleep_controller.loop()


BOT_INSTANCE = Bot()
