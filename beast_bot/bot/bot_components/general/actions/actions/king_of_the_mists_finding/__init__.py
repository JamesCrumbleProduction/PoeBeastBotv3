from .action import KingOfTheMistsFinding
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'KingOfTheMistsFinding',
    ExecutableAction(
        action=KingOfTheMistsFinding,
        excecutable_from_server=False
    )
)
