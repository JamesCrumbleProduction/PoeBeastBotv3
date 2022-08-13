from .action import ToOwnHideout
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'ToOwnHideout',
    ExecutableAction(
        action=ToOwnHideout,
        excecutable_from_server=True
    )
)
