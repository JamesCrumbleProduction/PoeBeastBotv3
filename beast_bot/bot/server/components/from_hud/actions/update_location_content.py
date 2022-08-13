from ..structure import LocationContent
from .....bot_components import bot


def update_location_content(
    location_content: LocationContent
) -> None:
    bot.BOT_INSTANCE.data_adapter.update_content(location_content)
