from ...structure import ControlEvent
from ...abstract_gui_components import AbstractEventsInitializer
from ....structure import MachineStatus
from ....requests_controller import (
    RoutePrefix,
    RequestEvent,
    ConnectionRoutes
)


class EventsInitializer(AbstractEventsInitializer):

    def _init_events(self) -> None:
        self._events[ControlEvent.PAUSE] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.change_status,
            params={'status': MachineStatus.PAUSING.value}
        )
        self._events[ControlEvent.RESUME] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.change_status,
            params={'status': MachineStatus.WORKING.value}
        )
        self._events[ControlEvent.INTO_HO] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.execute_action,
            params={'action': 'ToOwnHideout'}
        )
        self._events[ControlEvent.DOOR] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.execute_action,
            params={'action': 'Door'}
        )
        self._events[ControlEvent.PORTAL] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.execute_action,
            params={'action': 'EnterIntoPortal'}
        )
        self._events[ControlEvent.PACK_BEASTS] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.execute_action,
            params={'action': 'PackBeastsAction'}
        )
        self._events[ControlEvent.STOP_PACK_BEASTS] = RequestEvent(
            prefix=RoutePrefix.CONTROL,
            route=ConnectionRoutes.ControlMachine.execute_action,
            params={'action': 'StopPackBeastsAction'}
        )
