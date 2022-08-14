
from typing import Callable

from .monitoring_panel import MonitoringPanel
from ...structure import ControlEvent, EventSide
from ...abstract_gui_components import AbstractButtonsInitializer, AbstractGui


class ButtonsInitializer(AbstractButtonsInitializer):

    def __init__(
        self,
        gui_instance: type[AbstractGui],
        panel_instance: MonitoringPanel,
        button_events_connection_method: Callable[[str], None]
    ) -> None:
        super().__init__(gui_instance, panel_instance, button_events_connection_method)
        self.add_binds_to_rendering_buttons(gui_instance, panel_instance)

    def add_binds_to_rendering_buttons(
        self,
        gui_instance: type[AbstractGui],
        panel_instance: MonitoringPanel
    ) -> None:

        def resume_working_action(machine_name: str) -> None:
            if machine := gui_instance.available_machines.get(machine_name):
                gui_instance._request_to_machine(
                    machine, ControlEvent.RESUME
                )

        panel_instance.bind_render_button(
            machine_name='1',
            action=lambda: resume_working_action('1'),
            custom_button_text='1'
        )
        panel_instance.bind_render_button(
            machine_name='2',
            action=lambda: resume_working_action('2'),
            custom_button_text='2'
        )
        panel_instance.bind_render_button(
            machine_name='3',
            action=lambda: resume_working_action('3'),
            custom_button_text='3'
        )
        panel_instance.bind_render_button(
            machine_name='4',
            action=lambda: resume_working_action('4'),
            custom_button_text='4'
        )

    def _init_buttons_events(
        self,
        panel_instance: MonitoringPanel,
        connection_method: Callable[[str], None]
    ) -> None:
        self._add_button_event(
            panel_instance.ui.toolButton_3,
            ControlEvent.PAUSE,
            connection_method
        )
        self._add_button_event(
            panel_instance.ui.toolButton_4,
            ControlEvent.RESUME,
            connection_method
        )
        self._add_button_event(
            panel_instance.ui.toolButton_8,
            ControlEvent.PORTAL,
            connection_method,
            event_side=EventSide.IDLE_SIDE
        )
        self._add_button_event(
            panel_instance.ui.toolButton_9,
            ControlEvent.INTO_HO,
            connection_method,
            event_side=EventSide.IDLE_SIDE
        )
        self._add_button_event(
            panel_instance.ui.toolButton_10,
            ControlEvent.DOOR,
            connection_method,
            event_side=EventSide.IDLE_SIDE
        )
