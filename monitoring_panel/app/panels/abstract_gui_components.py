from typing import Callable
from PySide6.QtCore import QObject
from abc import ABC, abstractmethod
from fastapi import APIRouter, Request
from PySide6.QtWidgets import QDialog, QApplication, QAbstractButton

from .exceptions import InitializerError
from .structure import ControlEventButton, ControlEvent, EventSide
from ..structure import Machine, MachineStatus
from ..requests_controller.structure import RequestEvent


class AbstractThreadSafeServerMethods(QObject):

    def __init__(self) -> None:
        try:
            self.__dict__
        except Exception:
            raise NotImplementedError(
                'ThreadSafeServerMethods class should implement signals as class objects and cannot have __slots__'
            )
        else:
            super().__init__()


class AbstractMonitoringPanel(QDialog):
    def __init__(self) -> None:
        try:
            self.__dict__
        except Exception:
            raise NotImplementedError(
                'MonitoringPanel class cannot have __slots__'
            )
        else:
            super().__init__()


class AbstractEventsInitializer(ABC):
    __slots__ = (
        '_events'
    )

    def __init__(self) -> None:
        self._events: dict[ControlEvent, RequestEvent] = dict()
        self._init_events()

    def get(self, event: ControlEvent) -> RequestEvent:
        try:
            return self._events[event]
        except KeyError:
            raise InitializerError(
                f'"{event}" event doesn\'t exists'
            )

    @abstractmethod
    def _init_events(self) -> None:
        ...


class AbstractButtonsInitializer(ABC):

    __slots__ = (
        '_buttons_events',
    )

    def __init__(
        self,
        panel_instance: type[QDialog],
        button_events_connection_method: Callable[[str], None]
    ) -> None:
        self._buttons_events: dict[str, ControlEventButton] = dict()
        self._init_buttons_events(
            panel_instance, button_events_connection_method
        )

    def get(self, button: str) -> ControlEventButton:
        try:
            return self._buttons_events[button]
        except KeyError:
            raise InitializerError(
                f'"{button}" button doesn\'t exists'
            )

    def _add_button_event(
        self,
        button: type[QAbstractButton],
        control_event: ControlEvent,
        connection_method: Callable[[str], None],
        event_side: EventSide = EventSide.WORKER_SIDE
    ) -> None:
        self._buttons_events[button.objectName()] = ControlEventButton(
            event=control_event,
            button=button,
            event_side=event_side
        )
        button.clicked.connect(lambda: connection_method(
            button.objectName()
        ))

    @abstractmethod
    def _init_buttons_events(
        self,
        panel_instance: type[AbstractMonitoringPanel],
        connection_method: Callable
    ) -> None:
        ...


class AbstractGui(ABC):

    working_status: bool = False

    def __init__(self) -> None:
        try:
            self.__dict__
        except Exception:
            raise NotImplementedError(
                'GUI class should implement singleton instances of all property as class objects and cannot have __slots__'
            )

    @property
    @abstractmethod
    def singleton_instance(self) -> 'AbstractGui':
        ...

    @property
    @abstractmethod
    def application(self) -> QApplication:
        ...

    @property
    @abstractmethod
    def events_initializer(self) -> type[AbstractEventsInitializer]:
        ...

    @property
    @abstractmethod
    def buttons_initializer(self) -> type[AbstractButtonsInitializer]:
        ...

    @property
    @abstractmethod
    def panel_instance(self) -> type[AbstractMonitoringPanel]:
        ...

    @property
    @abstractmethod
    def server_methods(self) -> type[AbstractThreadSafeServerMethods]:
        ...

    @property
    @abstractmethod
    def available_machines(self) -> dict[str, Machine]:
        ...

    def init_linking_server_actions(self, machines_control_router: APIRouter) -> None:

        async def available_machines() -> dict[str, Machine]:
            return self.available_machines

        async def register_machine(
            vm_name: str,
            port: int,
            request: Request,
            as_party_machine: bool = True
        ) -> None:
            self.server_methods.call_to_add_selectable_machine(Machine(
                name=vm_name,
                host=request.client.host,
                port=port,
                status=MachineStatus.PAUSED
            ), as_party_machine)

        async def update_machine_status(
            vm_name: str,
            request: Request,
            register_status: MachineStatus | MachineStatus = MachineStatus.PAUSED,
        ) -> None:
            self.server_methods.call_to_update_machine_status(Machine(
                name=vm_name,
                host=request.client.host,
                port=request.client.port,
                status=register_status
            ))

        machines_control_router.add_api_route(
            path='/available_machines',
            endpoint=available_machines,
            methods=['GET'],
            status_code=200
        )
        machines_control_router.add_api_route(
            path='/register_machine',
            endpoint=register_machine,
            methods=['POST'],
            status_code=200
        )
        machines_control_router.add_api_route(
            path='/update_machine_status',
            endpoint=update_machine_status,
            methods=['POST'],
            status_code=200
        )

    def run_gui_components(self) -> None:
        self.working_status = True
        self.panel_instance.show()
        self.application.exec()
