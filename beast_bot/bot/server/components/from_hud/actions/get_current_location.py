from ..structure import CurrentLocation

from bot import bot_components


def get_current_location() -> CurrentLocation | None:
    return bot_components.BOT_INSTANCE.data_adapter.location
