from functools import wraps
from PySide6.QtCore import Qt

from . import gui
from ...structure import Machine, MachineStatus


def add_machine_when_not_exists(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        as_party_machine = None

        if len(kwargs) >= 2:
            self_statement: 'gui.GUI' = kwargs['self']
            machine: Machine = kwargs['machine']
            if 'as_party_machine' in kwargs:
                as_party_machine: bool = kwargs['as_party_machine']
        elif len(args) >= 2:
            self_statement: 'gui.GUI' = args[0]
            machine: Machine = args[1]
            if len(args) == 3:
                as_party_machine: bool = args[2]
                args = tuple(args[:2])

        if machine.name not in self_statement.panel_instance.machines:

            if as_party_machine is True:
                machine.status = MachineStatus.IDLE_MEMBER

            self_statement.panel_instance.ui.comboBox.addItem(
                machine.name + machine.extended_output_format()
            )

            if not machine.is_idle_member():
                self_statement.panel_instance.ui.textBrowser.append(
                    machine.output_format()
                )
                self_statement.panel_instance.ui.textBrowser.setAlignment(
                    Qt.AlignCenter
                )

            self_statement.panel_instance.machines[machine.name] = machine
            print(machine.name)
            print(self_statement.panel_instance.binded_rendering_buttons.get(
                machine.name))
            if rendering_button := self_statement.panel_instance.binded_rendering_buttons.get(machine.name):
                print('fewgweg')
                rendering_button.setHidden(False)

        func(*args, **kwargs)

    return wrapper
