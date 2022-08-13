from .action import Door
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'Door',
    ExecutableAction(
        action=Door,
        excecutable_from_server=True
    )
)
