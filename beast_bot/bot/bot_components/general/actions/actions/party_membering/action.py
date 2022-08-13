from typing import Iterator, Any

from ...abstract_action import AbstractAction
from ....structure import ControlAction
from ....bot_data_adapter import BotDataAdapter
from ....world_to_screen import TemplateScanner
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....panel_data import MachineStatus


class PartyMembering(AbstractAction):
    '''
    Idle action for insta checking when machine is party member
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
        self._permissions = set()

    @property
    def permissions(self, **action_kwargs: dict[str, Any]) -> set[MachineStatus]:
        return self._permissions

    def execute_action(self) -> Iterator[ControlAction]:
        yield from super().execute_action()
        ...
