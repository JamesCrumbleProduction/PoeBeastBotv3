import time

from ..actions import ACTIONS
from ..structure import ActionMeta, ControlAction
from ..panel_data import MachineStatus, BEASTS_STATUSES
from ...general import bot_data_adapter


class SleepController:

    __slots__ = ('_data_adapter',)

    def __init__(self, data_adapter: 'bot_data_adapter.BotDataAdapter'):
        self._data_adapter = data_adapter

    def _in_hideout(self) -> bool:
        if self._data_adapter.location.current_location is None:
            return False

        return 'hideout' in self._data_adapter.location.current_location.lower()

    def _run_executable_action(self, action_meta: ActionMeta) -> None:
        if executable_action := ACTIONS.get(action_meta.action_label):
            if self._data_adapter.status in executable_action.action.permissions:
                for action in executable_action.action.execute_action(
                    **action_meta.action_kwargs
                ):
                    if action is ControlAction.EXIT:
                        break

    def loop(self) -> None:
        '''Controller while machine isn't working...'''
        while self._data_adapter.status is not MachineStatus.WORKING:

            if self._data_adapter.status is MachineStatus.PAUSING and self._in_hideout():
                self._data_adapter.update_status(MachineStatus.PAUSED)

            elif (
                self._data_adapter.location is not None and self._in_hideout()
                and self._data_adapter.status in BEASTS_STATUSES.values()
            ):
                self._data_adapter.update_status(
                    MachineStatus.FOUNDER_AVAILABLE
                )

            if action_meta := self._data_adapter.get_action():
                self._run_executable_action(action_meta)

            time.sleep(0.1)
