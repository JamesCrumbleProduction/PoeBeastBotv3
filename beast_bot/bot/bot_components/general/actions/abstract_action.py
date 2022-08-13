from typing import Iterator, Any
from abc import ABC, abstractmethod

from ..panel_data import MachineStatus
from ..structure import ControlAction
from ..bot_data_adapter import BotDataAdapter


class AbstractAction(ABC):

    __slots__ = (
        'bot_data_adapter',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        self.bot_data_adapter = bot_data_adapter

    @property
    @abstractmethod
    def permissions(self) -> set[MachineStatus]:
        ...

    @abstractmethod
    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield ControlAction.ActionType
