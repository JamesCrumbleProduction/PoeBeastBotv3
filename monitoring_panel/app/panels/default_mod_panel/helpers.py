from functools import wraps
from PySide6.QtCore import Qt

from . import gui
from ...structure import Machine


def add_machine_when_not_exists(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(kwargs) >= 2:
            self_statement: 'gui.GUI' = kwargs['self']
            machine: Machine = kwargs['machine']
        elif len(args) >= 2:
            self_statement: 'gui.GUI' = args[0]
            machine: Machine = args[1]

        if machine.name not in self_statement.panel_instance.machines:
            self_statement.panel_instance.ui.comboBox.addItem(machine.name)
            self_statement.panel_instance.ui.textBrowser.append(
                machine.output_format()
            )
            self_statement.panel_instance.ui.textBrowser.setAlignment(
                Qt.AlignCenter
            )

            self_statement.panel_instance.machines[machine.name] = machine

        func(*args, **kwargs)

    return wrapper
