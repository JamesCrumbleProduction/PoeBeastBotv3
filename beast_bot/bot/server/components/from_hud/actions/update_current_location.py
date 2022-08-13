from ..structure import CurrentLocation
from .....bot_components import bot


def update_current_location(
    current_location: CurrentLocation
) -> None:
    bot.BOT_INSTANCE.data_adapter.update_location(current_location)
