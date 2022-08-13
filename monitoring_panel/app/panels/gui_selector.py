from fastapi import APIRouter

from .default_mod_panel import DefaultModGui
from .extended_mod_panel import ExtendedModGui
from .abstract_gui_components import AbstractGui
from ..settings import settings


class GuiSelector:

    __slots__ = (
        '_gui_instance'
    )

    def __init__(self, machines_control_router: APIRouter) -> None:
        if settings.EXTENDED_NETWORK_MODE is True:
            self._gui_instance = ExtendedModGui()
        else:
            self._gui_instance = DefaultModGui()

        self._gui_instance.init_linking_server_actions(machines_control_router)

    @property
    def instance(self) -> type[AbstractGui]:
        return self._gui_instance
