from .....bot_components import bot


def change_status(
    status: bot.MachineStatus
) -> None:
    bot.BOT_INSTANCE.data_adapter.update_status(status)
