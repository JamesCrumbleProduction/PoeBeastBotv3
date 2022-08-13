from .action import EnterIntoPortal
from ...actions_init import add_action
from ...structure import ExecutableAction

add_action(
    'EnterIntoPortal',
    ExecutableAction(
        action=EnterIntoPortal,
        excecutable_from_server=True
    )
)
