from typing import Callable
from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QComboBox, QToolButton

from .exceptions import MaxRenderButtonsBindingReached
from ..design.compiled_design import Ui_Dialog
from ...abstract_gui_components import AbstractMonitoringPanel
from ....structure import Machine

RENDER_BUTTON_PREFIX: str = 'renderButton'


class ComboBox(QComboBox):
    popupAboutToBeShown = Signal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super().showPopup()


class MonitoringPanel(AbstractMonitoringPanel):

    _browser_cursor: QTextCursor = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.binded_rendering_buttons: dict[str, QToolButton] = dict()
        self.rendering_buttons: list[QToolButton] = list()  # sorted

        self._is_changed: bool = True
        self.machines: dict[str, Machine] = dict()

        if comboBox := getattr(self.ui, 'comboBox', None):
            comboBox: QComboBox
            self.ui.comboBox = ComboBox(self)
            self.ui.comboBox.setObjectName(comboBox.objectName())
            self.ui.comboBox.setGeometry(comboBox.geometry())
            self.ui.comboBox.setStyleSheet(comboBox.styleSheet())
            self.ui.comboBox.setEditable(comboBox.isEditable())
            self.ui.radioButton.setChecked(True)

        self._init_rendering_buttons()
        self._hide_rendering_buttons()

    def bind_render_button(
        self,
        /,
        machine_name: str,
        action: Callable,
        custom_button_text: str = None
    ) -> None:
        if not self.rendering_buttons:
            raise MaxRenderButtonsBindingReached(
                'Cannot binding another renderButton '
                f'couse limit "{len(self.binded_rendering_buttons)}" was reached'
            )

        rendering_button = self.rendering_buttons.pop()

        if custom_button_text is not None:
            rendering_button.setText(custom_button_text)

        rendering_button.clicked.connect(action)
        self.binded_rendering_buttons[machine_name] = rendering_button

    def _init_rendering_buttons(self) -> None:
        self.rendering_buttons = [
            getattr(self.ui, render_button)
            for render_button in sorted(
                [
                    ui_element
                    for ui_element in self.ui.__dict__.keys()
                    if RENDER_BUTTON_PREFIX in ui_element
                ],
                reverse=True
            )
        ]

    def _hide_rendering_buttons(self) -> None:
        for rendering_button in self.rendering_buttons:
            rendering_button.hide()

    def get_selected_machine_from_comboBox(self) -> Machine | None:
        if machine_fake_name := self.ui.comboBox.currentText():
            return self.machines.get(machine_fake_name.split(' - ')[0])

    def update_status_in_text_browser(self, machine: Machine) -> None:
        if founded_machine := self.machines.get(machine.name):
            founded_machine.status = machine.status

            self._clear_text_browser()

            for machine in self.machines.values():
                if not machine.is_idle_member():
                    self.ui.textBrowser.append(machine.output_format())

    def event_combobox_control(self) -> None:
        self._is_changed = True

    def event_switch_control(self) -> None:
        if self.ui.radioButton.isChecked() is True and self._is_changed is True:
            self.ui.radioButton.setChecked(False)
            self._is_changed = False

    def _clear_text_browser(self) -> None:
        if self._browser_cursor is None:
            self._browser_cursor = self.ui.textBrowser.textCursor()

        self._browser_cursor.movePosition(QTextCursor.MoveOperation.Start)
        self._browser_cursor.select(QTextCursor.SelectionType.Document)
        self._browser_cursor.removeSelectedText()
