import os
import asyncio
import uvicorn

from bot import (
    app,
    settings,
    BOT_LOGGER,
    BOT_INSTANCE,
    SERVER_EXECUTOR
)
from bot.bot_components.general.panel_data import MachineStatus

MAIN_THREAD_WORKING: bool = True


@app.on_event('startup')
async def on_startup():
    async def _working_event():
        global MAIN_THREAD_WORKING

        while True:
            if MAIN_THREAD_WORKING is False:
                os._exit(0)
            await asyncio.sleep(2)

    asyncio.get_running_loop().create_task(
        _working_event(), name='_working_event'
    )

if __name__ == '__main__':
    try:
        SERVER_EXECUTOR.submit(
            uvicorn.run,
            app="run:app",
            host=settings.BOT_SERVER.HOST,
            port=settings.BOT_SERVER.PORT
        )
        BOT_INSTANCE.run()
    except (Exception, KeyboardInterrupt) as exception:
        BOT_INSTANCE.data_adapter.update_status(MachineStatus.ERROR)
        BOT_LOGGER.critical(exception, exc_info=True)
    finally:
        MAIN_THREAD_WORKING = False
