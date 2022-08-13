from .action import PartyAccept
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'PartyAccept',
    ExecutableAction(
        action=PartyAccept,
        excecutable_from_server=True
    )
)
