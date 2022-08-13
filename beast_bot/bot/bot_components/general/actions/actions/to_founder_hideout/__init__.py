from .action import ToFounderHideout
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'ToFounderHideout',
    ExecutableAction(
        action=ToFounderHideout,
        excecutable_from_server=True
    )
)
