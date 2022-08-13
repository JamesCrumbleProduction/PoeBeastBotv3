from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QComboBox

from ..design.compiled_design import Ui_Dialog
from ...abstract_gui_components import AbstractMonitoringPanel
from ....structure import Machine


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

        if comboBox := getattr(self.ui, 'comboBox', None):
            comboBox: QComboBox
            self.ui.comboBox = ComboBox(self)
            self.ui.comboBox.setObjectName(comboBox.objectName())
            self.ui.comboBox.setGeometry(comboBox.geometry())
            self.ui.comboBox.setStyleSheet(comboBox.styleSheet())
            self.ui.comboBox.setEditable(comboBox.isEditable())
            self.ui.radioButton.setChecked(True)

        self._is_changed: bool = True
        self.machines: dict[str, Machine] = dict()

    def get_selected_machine_from_comboBox(self) -> Machine | None:
        return self.machines.get(self.ui.comboBox.currentText())

    def update_status_in_text_browser(self, machine: Machine) -> None:
        if founded_machine := self.machines.get(machine.name):
            founded_machine.status = machine.status

            self._clear_text_browser()

            for machine in self.machines.values():
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
