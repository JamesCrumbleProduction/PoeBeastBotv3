from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from .data import data_router
from .server_status import server_status_router


class LinkingServer:

    __slots__ = (
        '_app',

        'data_router',
        'machines_control_router',
        'server_status_router',
    )

    def __init__(self):
        self._app: FastAPI = None
        self.data_router = data_router
        self.machines_control_router = APIRouter()
        self.server_status_router = server_status_router

    def _include_routers(self) -> None:
        if self._app is None:
            return

        self._app.include_router(
            self.data_router,
            prefix='/data',
            tags=['Data']
        )
        self._app.include_router(
            self.machines_control_router,
            prefix='/control',
            tags=['Machines control']
        )
        self._app.include_router(
            self.server_status_router,
            prefix='/status',
            tags=['Server Status']
        )

    def _include_middlware(self) -> None:
        if self._app is None:
            return

        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_credentials=True,
            allow_headers=['*']
        )

    @property
    def app(self) -> FastAPI:
        if self._app is None:
            self._app = FastAPI()
            self._include_middlware()
            self._include_routers()

        return self._app
