from fastapi import APIRouter
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from concurrent.futures import ThreadPoolExecutor

from .helpers import add_machine_when_not_exists
from .components import ButtonsInitializer, EventsInitializer, MonitoringPanel
from ..abstract_gui_components import AbstractGui
from ..structure import (
    ControlEvent,
    ControlEventButton,
)
from ...settings import settings
from ...structure import Machine, MachineStatus
from ...requests_controller import RequestsController


class ThreadSafeServerMethods(QObject):
    add_selectable_machine_signal = Signal(Machine)
    update_machine_status_signal = Signal(Machine)
    worked_to_pausing_signal = Signal()

    def call_to_add_selectable_machine(self, machine: Machine, *_, **__) -> None:
        self.add_selectable_machine_signal.emit(machine)

    def call_to_update_machine_status(self, machine: Machine) -> None:
        self.update_machine_status_signal.emit(machine)

    def call_worked_to_pausing(self) -> None:
        self.worked_to_pausing_signal.emit()


class GUI(AbstractGui):

    _instance: 'GUI' = None
    _application: QApplication = None
    _events_initializer: EventsInitializer = None
    _buttons_initializer: ButtonsInitializer = None
    _panel_instance: MonitoringPanel = None
    _server_methods: ThreadSafeServerMethods = None

    def __new__(cls: type['GUI'], *args, **kwargs) -> 'GUI':

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._application = QApplication()
            cls._instance._panel_instance = MonitoringPanel()
            cls._instance._events_initializer = EventsInitializer()
            cls._instance._buttons_initializer = ButtonsInitializer(
                cls._instance, cls._instance._panel_instance, cls._instance._define_pressed_button
            )
            cls._instance._server_methods = ThreadSafeServerMethods()

        return cls._instance

    @property
    def singleton_instance(self) -> 'GUI':
        return self._instance

    @property
    def application(self) -> QApplication:
        return self._application

    @property
    def events_initializer(self) -> EventsInitializer:
        return self._events_initializer

    @property
    def buttons_initializer(self) -> ButtonsInitializer:
        return self._buttons_initializer

    @property
    def panel_instance(self) -> MonitoringPanel:
        return self._panel_instance

    @property
    def server_methods(self) -> ThreadSafeServerMethods:
        return self._server_methods

    def __init__(self):
        self._requests = RequestsController()

        self._server_methods.add_selectable_machine_signal.connect(
            self._add_selectable_machine
        )
        self._server_methods.update_machine_status_signal.connect(
            self._update_machine_status
        )
        self._server_methods.worked_to_pausing_signal.connect(
            self._worked_to_pausing
        )

    @add_machine_when_not_exists
    def _add_selectable_machine(self, machine: Machine) -> None:
        if machine.status != self._panel_instance.machines[machine.name].status:
            self._panel_instance.update_status_in_text_browser(machine)

    @add_machine_when_not_exists
    def _update_machine_status(self, machine: Machine) -> None:
        self._panel_instance.update_status_in_text_browser(machine)

    def _worked_to_pausing(self) -> None:
        for machine in self._panel_instance.machines.values():
            if machine.status is MachineStatus.WORKING:
                self._requests.execute_in_thread(
                    machine, self._events_initializer.get(ControlEvent.PAUSE)
                )

    def _request_to_machine(
        self,
        machine: Machine,
        control_event: ControlEvent
    ) -> None:
        if request_event := self._events_initializer.get(control_event):
            if machine.status != MachineStatus.ERROR:
                self._requests.execute(machine, request_event)

    def _define_pressed_button(self, button_name: str) -> None:
        if event_button := self._buttons_initializer.get(button_name):
            if self._panel_instance.ui.radioButton.isChecked():
                for machine in self._panel_instance.machines.values():
                    self._request_to_machine(machine, event_button.event)

            elif machine := self._panel_instance.get_selected_machine_from_comboBox():
                self._request_to_machine(machine, event_button.event)

    @property
    def available_machines(self) -> dict[str, Machine]:
        return self._panel_instance.machines

    def init_linking_server_actions(self, machines_control_router: APIRouter) -> None:
        super().init_linking_server_actions(machines_control_router)
        machines_control_router.add_api_route(
            path='/call_worked_to_pausing',
            endpoint=self.server_methods.call_worked_to_pausing,
            methods=['PATCH'],
            status_code=200
        )
