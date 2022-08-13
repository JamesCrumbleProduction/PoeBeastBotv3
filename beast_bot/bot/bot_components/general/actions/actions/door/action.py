from typing import Iterator, Any

from ...abstract_action import AbstractAction
from ....structure import ControlAction
from ....bot_data_adapter import BotDataAdapter
from ....io_controllers import CommonIOController
from ....world_to_screen import TemplateScanner
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....panel_data import MachineStatus, BEASTS_STATUSES


class Door(AbstractAction):
    '''
    Bot enter into next layer of layout 
    (depends on available templates "next_layout_nametags_templates" of layouts) 
    if it's possible
    '''

    __slots__ = (
        '_permissions',
        '_nametags_validator',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._nametags_validator = TemplateScanner(
            iterable_templates=BEAST_BOT_COMPILED_TEMPLATES.next_layout_nametags_templates.templates,
            threshold=0.75
        )
        self._permissions = {
            MachineStatus.PAUSED,
            MachineStatus.FOUNDER_AVAILABLE,
            MachineStatus.IDLE_MEMBER,
            *BEASTS_STATUSES.values()
        }

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield from super().execute_action()
        for label_coord in self._nametags_validator.iterate_all_by_first_founded():
            if label_coord:
                CommonIOController.move_and_click(label_coord)
                break
