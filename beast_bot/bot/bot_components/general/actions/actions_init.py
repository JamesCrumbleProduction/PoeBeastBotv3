from .structure import ExecutableAction

ACTIONS: dict[str, ExecutableAction] = dict()


def add_action(action_name: str, action: ExecutableAction) -> None:
    if action_name not in ACTIONS:
        ACTIONS[action_name] = action
