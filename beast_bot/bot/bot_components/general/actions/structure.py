from pydantic import BaseModel

from .abstract_action import AbstractAction
from ..bot_data_adapter import BotDataAdapter


class ExecutableAction(BaseModel):

    action: type[AbstractAction]
    excecutable_from_server: bool

    def init_action(self, bot_data_adapter: BotDataAdapter) -> 'ExecutableAction':
        if (
            issubclass(self.action, AbstractAction)
            and not isinstance(self.action, AbstractAction)
        ):
            self.action = self.action(bot_data_adapter)

        return self
