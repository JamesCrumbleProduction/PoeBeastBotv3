import os
import asyncio
import uvicorn

from app.services.logger import PANEL_LOGGER
from app.services.executor import LINKING_SERVER_EXECUTOR
from app import (
    settings,
    GuiSelector,
    LinkingServer
)

linking_server = LinkingServer()
GUI_SELECTOR = GuiSelector(
    linking_server.machines_control_router
)
app = linking_server.app


@app.on_event('startup')
async def on_startup():
    async def _working_event():
        global GUI_SELECTOR

        while True:
            if GUI_SELECTOR.instance.working_status is False:
                os._exit(0)
            await asyncio.sleep(2)

    asyncio.get_running_loop().create_task(
        _working_event(), name='_working_event'
    )

if __name__ == '__main__':
    try:
        LINKING_SERVER_EXECUTOR.submit(
            uvicorn.run,
            app="run:app",
            host=settings.HOST,
            port=settings.PORT
        )
        GUI_SELECTOR.instance.run_gui_components()
    except Exception as exception:
        PANEL_LOGGER.critical(exception, exc_info=True)
    finally:
        settings.save_settings()
        GUI_SELECTOR.instance.working_status = False
