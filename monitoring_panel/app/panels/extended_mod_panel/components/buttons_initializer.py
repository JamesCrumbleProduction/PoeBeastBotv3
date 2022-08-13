from typing import Callable

from .monitoring_panel import MonitoringPanel
from ...structure import ControlEvent, EventSide
from ...abstract_gui_components import AbstractButtonsInitializer


class ButtonsInitializer(AbstractButtonsInitializer):

    def __init__(
        self,
        panel_instance: MonitoringPanel,
        button_events_connection_method: Callable[[str], None]
    ) -> None:
        super().__init__(panel_instance, button_events_connection_method)
        # self._init_combobox_button_event(panel_instance)
        # self._init_switch_button_event(panel_instance)

    # def _init_combobox_button_event(
    #     self,
    #     panel_instance: MonitoringPanel
    # ) -> None:
    #     panel_instance.ui.comboBox.popupAboutToBeShown.connect(
    #         lambda: panel_instance.event_switch_control()
    #     )

    # def _init_switch_button_event(
    #     self,
    #     panel_instance: MonitoringPanel
    # ) -> None:
    #     panel_instance.ui.radioButton.clicked.connect(
    #         lambda: panel_instance.event_combobox_control()
    #     )

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
