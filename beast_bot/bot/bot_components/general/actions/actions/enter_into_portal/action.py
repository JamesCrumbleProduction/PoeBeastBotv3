from typing import Iterator, Any

from ...abstract_action import AbstractAction
from ....panel_data import MachineStatus, EXTENDED_MODE
from ....bot_data_adapter import BotDataAdapter
from ....structure import ControlAction, Regions
from ....io_controllers import CommonIOController
from ....templates import EXTRA_CONTENT_COMPILED_TEMPLATES
from ....world_to_screen import (
    Coordinate,
    TemplateScanner,
    HSVPortalScanner,
    ShareDataConnector,
)
from ......settings import settings


class EnterIntoPortal(AbstractAction):
    '''Bot enter into portal if it's possible'''

    __slots__ = (
        '_permissions',
        '_hsv_portal_validator',
        '_share_data_validator',
        '_tempalates_defiles_and_ho',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._hsv_portal_validator = HSVPortalScanner(Regions.portals_region)
        self._tempalates_defiles_and_ho = TemplateScanner(
            iterable_templates=EXTRA_CONTENT_COMPILED_TEMPLATES.portal_action_templates.templates,
            threshold=0.65
        )
        self._share_data_validator = ShareDataConnector()
        self._permissions = {
            MachineStatus.IDLE_MEMBER,
            MachineStatus.FOUNDER_AVAILABLE
        }
        if not EXTENDED_MODE:
            self._permissions.add(MachineStatus.PAUSED)

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    # def _portals_coordinates(self, **action_kwargs: dict[str, Any]) -> Iterator[Coordinate]:

    #     if settings.SHARE_DATA_PORTAL_VALIDATOR is False:
    #         for portal_coord in self._hsv_portal_validator.iterate_by_each_founded():
    #             yield portal_coord
    #     else:
    #         for portal_coord in self._share_data_validator.iterate_by_each_founded_portal():
    #             yield portal_coord

    def _portals_coordinates(self, **kwargs) -> Iterator[Coordinate]:
        for portal_coord in self._tempalates_defiles_and_ho.iterate_one_by_each_founded():
            if portal_coord is not None:
                yield portal_coord

    def execute_action(self) -> Iterator[ControlAction]:
        yield from super().execute_action()

        for portal_coord in self._portals_coordinates():
            CommonIOController.move_and_click(portal_coord)
            yield ControlAction.DONE
            break
