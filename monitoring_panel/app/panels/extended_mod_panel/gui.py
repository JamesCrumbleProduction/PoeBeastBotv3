from fastapi import APIRouter
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from .helpers import add_machine_when_not_exists
from .components import ButtonsInitializer, EventsInitializer, MonitoringPanel
from ..abstract_gui_components import AbstractGui
from ..structure import (
    EventSide,
    ControlEvent,
    ControlEventButton,
)
from ...structure import Machine, MachineStatus
from ...requests_controller import RequestsController


class ThreadSafeServerMethods(QObject):
    add_selectable_machine_signal = Signal(Machine, bool)
    update_machine_status_signal = Signal(Machine)
    founder_party_accepted_signal = Signal(str, str)

    def call_to_add_selectable_machine(self, machine: Machine, as_party_machine: bool) -> None:
        self.add_selectable_machine_signal.emit(machine, as_party_machine)

    def call_to_update_machine_status(self, machine: Machine) -> None:
        self.update_machine_status_signal.emit(machine)

    def call_tp_patry_to_founder_signal(self, founder: str, machine_name: str) -> None:
        self.founder_party_accepted_signal.emit(founder, machine_name)


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
        self._server_methods.founder_party_accepted_signal.connect(
            self._party_to_founder
        )
        self._founder_machine: Machine = None

    @add_machine_when_not_exists
    def _add_selectable_machine(self, machine: Machine) -> None:
        if (
            machine.status != self._panel_instance.machines[machine.name].status
            and not self._panel_instance.machines[machine.name].is_idle_member()
        ):
            self._panel_instance.update_status_in_text_browser(machine)

    @add_machine_when_not_exists
    def _update_machine_status(self, machine: Machine) -> None:
        if not self._panel_instance.machines[machine.name].is_idle_member():
            self._panel_instance.update_status_in_text_browser(machine)

    def _party_to_founder(self, founder: str, machine_name: str) -> None:

        self._founder_machine = self._panel_instance.machines[machine_name]

        for machine in self._panel_instance.machines.values():
            if machine.is_idle_member():
                self._requests.execute_in_thread(
                    machine, self._events_initializer.get(
                        ControlEvent.INTO_FOUNDER_HO
                    ),
                    body={'founder': founder}
                )

    def _request_to_machine(
        self,
        machine: Machine,
        control_event: ControlEvent
    ) -> None:
        if request_event := self._events_initializer.get(control_event):
            if machine.status not in (
                MachineStatus.ERROR,
                MachineStatus.OUT_OF_MAPS,
                MachineStatus.OUT_OF_SCARABS,
            ):
                self._requests.execute_in_thread(machine, request_event)

    def _define_pressed_button(self, button_name: str) -> None:

        def _execute_by_side() -> None:
            if event_button.event_side is EventSide.IDLE_SIDE:
                if machine.is_idle_member() or (
                    self._founder_machine is not None
                    and machine.name == self._founder_machine.name
                ):
                    self._request_to_machine(machine, event_button.event)
            elif event_button.event_side is EventSide.WORKER_SIDE:
                if not machine.is_idle_member():
                    self._request_to_machine(machine, event_button.event)

        if event_button := self._buttons_initializer.get(button_name):
            if event_button.event in (ControlEvent.PAUSE, ControlEvent.RESUME):
                if machine := self._panel_instance.get_selected_machine_from_comboBox():
                    _execute_by_side()
                    return

            if self._panel_instance.ui.radioButton.isChecked():
                for machine in self._panel_instance.machines.values():
                    _execute_by_side()

            elif machine := self._panel_instance.get_selected_machine_from_comboBox():
                _execute_by_side()

    @property
    def available_machines(self) -> dict[str, Machine]:
        return self._panel_instance.machines

    def init_linking_server_actions(self, machines_control_router: APIRouter) -> None:
        super().init_linking_server_actions(machines_control_router)
        machines_control_router.add_api_route(
            path='/idles_to_founder',
            endpoint=self.server_methods.call_tp_patry_to_founder_signal,
            methods=['POST'],
            status_code=200
        )
