from typing import Any

from .....bot_components import bot


def execute_action(action: str, action_kwargs: dict[str, Any]) -> None:
    bot.BOT_INSTANCE.data_adapter.add_action_to_execute(
        action, action_kwargs
    )
