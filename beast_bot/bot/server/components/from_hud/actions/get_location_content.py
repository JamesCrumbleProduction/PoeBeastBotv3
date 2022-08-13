from ..structure import LocationContent

from bot import bot_components


def get_location_content() -> LocationContent | None:
    return bot_components.BOT_INSTANCE.data_adapter.content
