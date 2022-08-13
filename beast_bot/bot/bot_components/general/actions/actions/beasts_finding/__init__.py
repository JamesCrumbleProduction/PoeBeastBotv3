from .action import BeastsFindingAction
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'BeastsFindingAction',
    ExecutableAction(
        action=BeastsFindingAction,
        excecutable_from_server=False
    )
)
