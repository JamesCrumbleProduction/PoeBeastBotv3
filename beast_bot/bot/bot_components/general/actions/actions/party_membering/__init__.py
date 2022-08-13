from .action import PartyMembering
from ...actions_init import add_action
from ...structure import ExecutableAction


add_action(
    'PartyMembering',
    ExecutableAction(
        action=PartyMembering,
        excecutable_from_server=False
    )
)
