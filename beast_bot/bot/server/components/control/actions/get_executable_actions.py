from ..structure import ExecutableActionsResponse
from .....bot_components.general.actions import ACTIONS


def get_executable_actions() -> ExecutableActionsResponse:
    return ExecutableActionsResponse(
        actions=[
            action_name
            for action_name, action in ACTIONS.items()
            if action.excecutable_from_server is True
        ]
    )
