import time

from dataclasses import fields
from pynput.keyboard import Key
from typing import Iterator, Callable, Any

from .exceptions import UnknownStashTab
from .structure import TabMeta, StashTab
from .settings import settings as action_settings

from ...abstract_action import AbstractAction
from ....sounds_handler import SoundOperation
from ....bot_data_adapter import BotDataAdapter
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....panel_data import BEASTS_STATUSES, MachineStatus
from ....structure import (
    Regions,
    Coordinates,
    ControlAction
)
from ....world_to_screen import (
    Coordinate,
    TemplateScanner,
    ShareDataConnector
)
from ....io_controllers import (
    IterateIOController,
    CommonIOController,
    ClipboardIOController
)
from ......settings import settings
from ......services.logger import BOT_LOGGER


class KingOfTheMistsFinding(AbstractAction):

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._permissions = set()

        self._inventory_maps: list[Coordinate] = list()
        self._inventory_empty_sockets_count: int = -1

        self._init_stash_data()
        self._init_scanners()
        self._init_controllers()
        self._init_connectors()

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def _test_share_data_connector(self) -> None:
        for _ in range(10):
            self._share_data_connector.update_source()
            if self._share_data_connector._share_data_content:
                return
            
        err = RuntimeError("SHARE DATA DOES NOT WORKING !!!!!!!!!!!!!!!!!!!!!!!")
        BOT_LOGGER.error(err)
        time.sleep(10)
        raise err

    def _init_stash_data(self) -> None:
        self._tabs_coordinates: dict[StashTab, TabMeta] = {
            StashTab.MAPS: TabMeta(*list(Coordinates().stash.map_tabs)),
        }
        BOT_LOGGER.debug('"KingOfTheMistsFinding": STASH DATA WAS INITED')

    def _init_connectors(self) -> None:
        self._share_data_connector = ShareDataConnector()
        BOT_LOGGER.debug('"KingOfTheMistsFinding": CONNECTORS WAS INITED')

    def _init_scanners(self) -> None:
        self._maps_scanner = TemplateScanner(
            iterable_templates=BEAST_BOT_COMPILED_TEMPLATES.maps_templates.templates,
            region=Regions().stash_region, threshold=0.45
        )
        self._stash_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.nametags_templates.get('stash'),
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get('stash_label'),
            threshold=0.9
        )
        self._unloaded_stash_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'empty_inventory_socket'
            ), region=Regions().stash_region, threshold=0.9
        )
        self._map_device_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.nametags_templates.get('map_device'),
            BEAST_BOT_COMPILED_TEMPLATES.buttons_templates.get('activate'),
            threshold=0.8
        )
        self._loading_screen_to_map_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'to_map_loading_screen'
            ), threshold=0.8
        )
        self._loading_screen_to_ho_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'hideout_loading_screen'
            ), threshold=0.8
        )
        self._ressurect_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.buttons_templates.get(
                'ressurect_at_checkpoint'
            ), threshold=0.8
        )

        self._inventory_scanner_empty_sockets = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'empty_inventory_socket'
            ), region=Regions().inventory_region, threshold=0.75
        )
        self._inventory_scanner_maps = TemplateScanner(
            iterable_templates=BEAST_BOT_COMPILED_TEMPLATES.maps_templates.templates,
            region=Regions().inventory_region, threshold=0.45
        )
        BOT_LOGGER.debug('"KingOfTheMistsFinding": SCREEN SCANNERS WAS INITED')

    def _init_controllers(self) -> None:
        self._stash_io_controller = ClipboardIOController()
        self._inventory_io_controller = IterateIOController(
            Coordinates().first_socket_inventory_position
        )
        BOT_LOGGER.debug('"KingOfTheMistsFinding": CONTROLLERS WAS INITED')

    def _init_tab_content(self, tab: StashTab) -> None:

        if tab == StashTab.MAPS:
            scanner = self._maps_scanner
        else:
            raise NotImplementedError(
                f'tab argument in _init_tab_content have wrong source -> "{tab}"'
            )

        while True:

            if (
                self._unloaded_stash_scanner.get_condition_by_one() is True
                or scanner.get_condition_by_one() is True
            ):
                break

            time.sleep(action_settings.INIT_TAB_CONTENT_INTERVAL)

        if tab_meta := self._tabs_coordinates.get(tab):
            tab_meta.tab_content = list(scanner.iterate_all_by_each_founded())

    def _enter_to_stash(self) -> None:
        while True:
            iterator = self._stash_scanner.iterate_all_by_first_founded()

            if map_device_name_tag_coord := next(iterator):
                CommonIOController.move_and_click(map_device_name_tag_coord)
                time.sleep(0.3)
                self._stash_scanner.update_source()

            if next(iterator) is not None:
                break

            time.sleep(action_settings.ENTER_TO_INTERVAL)

    def _enter_to_map_device(self) -> None:

        while True:
            iterator = self._map_device_scanner.iterate_all_by_first_founded()

            if map_device_name_tag_coord := next(iterator):
                CommonIOController.move_and_click(map_device_name_tag_coord)
                time.sleep(0.3)
                self._map_device_scanner.update_source()

            if next(iterator) is not None:
                break

            time.sleep(action_settings.ENTER_TO_INTERVAL)

    def _set_inventory_empty_sockets_count(self) -> None:
        self._inventory_empty_sockets_count = len(list(
            self._inventory_scanner_empty_sockets.iterate_all_by_each_founded()
        ))

    def _grab_content(self, tab: StashTab) -> bool:
        if self._inventory_empty_sockets_count <= 0:
            self._set_inventory_empty_sockets_count()

        tab_meta = self._tabs_coordinates.get(tab)
        if tab_meta is None:
            raise UnknownStashTab(f'Unknown "{tab}" value of "tab" argument')

        if tab_coordinate := tab_meta.tab:
            CommonIOController.move_and_click(tab_coordinate)

            if tab_meta.tab_content is None or not tab_meta.tab_content:
                time.sleep(0.1)
                self._init_tab_content(tab)

            if not tab_meta.tab_content:
                return self._grab_content(tab)

        else:
            self.bot_data_adapter.update_status(
                MachineStatus.OUT_OF_MAPS
                if tab == StashTab.MAPS
                else MachineStatus.OUT_OF_SCARABS
            )
            return False

        for _ in range(min(len(tab_meta.tab_content), self._inventory_empty_sockets_count)):
            CommonIOController.move(tab_meta.tab_content.pop())
            time.sleep(0.05)

            start = time.monotonic()

            while True:
                if self._stash_io_controller.get_clipboard_data() is not None:
                    CommonIOController.grab()
                    break

                if time.monotonic() - start >= action_settings.GRAB_CONTENT_TIMEOUT:
                    return self._grab_content(tab)

                time.sleep(action_settings.GRAB_CONTENT_CLIPBOARD_INTERBAL)

        self._inventory_maps = list(
            self._inventory_scanner_maps.iterate_all_by_each_founded()
        )

        return True

    def _scarab_in_device(self) -> bool:
        return self._scarabs_scanner(
            as_custom_region=Regions().map_device_sockets_region
        ).get_condition_by_one()

    def _move_content_into_device(self) -> None:
        CommonIOController.move_and_grab(self._inventory_maps.pop())

    def _activate_map_device(self) -> None:
        CommonIOController.move_and_click(
            Coordinates().activate_map_device_button
        )

    def _enter_into_portal(self) -> None:

        if settings.SHARE_DATA_PORTAL_VALIDATOR is False:
            for portal_coord in self._hsv_portal_scanner.iterate_by_each_founded():
                CommonIOController.move_and_click(portal_coord)
                break

        else:
            if portal_coord := self._share_data_connector.get_closest_portal():
                CommonIOController.move_and_click(portal_coord)

    def _press_ressurect_when_found(self) -> None:
        if ressurect_coord := self._ressurect_scanner.indentify_by_first():
            CommonIOController.move_and_click(ressurect_coord)

    def _check_map_content(self) -> bool:
        while True:
            founded_content = self._share_data_connector.get_location_content()
            if founded_content is not None:
                break

        for element in founded_content:
            if founded := BEASTS_STATUSES.get(element):
                self.bot_data_adapter.update_status(founded)
                if settings.NOTIFY_BY_SOUND is True:
                    SoundOperation.execute_audio(SoundOperation.choice_random_alert())  # noqa
                break

        return self.bot_data_adapter.status in BEASTS_STATUSES.values()

    def _wait_until_not_in_location(
        self, condition: Callable[[None], bool]
    ) -> None:

        started_time = time.time()

        while True:
            if condition() is True:
                if self.bot_data_adapter.status is MachineStatus.HUD_PROBLEM:
                    self.bot_data_adapter.update_status(
                        MachineStatus.WORKING
                    )
                break

            if self._is_hud_problem(started_time) is True and self.bot_data_adapter.status is MachineStatus.WORKING:
                self.bot_data_adapter.update_status(
                    MachineStatus.HUD_PROBLEM
                )

            time.sleep(action_settings.WAIT_UNTIL_NOT_IN_LOCATION_INTEVAL)

    def _comeback_into_ho(self) -> None:
        while (
            self._loading_screen_to_ho_scanner.get_condition_by_one()
        ) is False:
            self._enter_into_portal()
            self._press_ressurect_when_found()
            time.sleep(action_settings.ENTER_INTO_PORTAL_INTERVAL)

        self._wait_until_not_in_location(lambda: (
            self._share_data_connector.get_current_location() is not None
            and self._in_hideout()
        ))

    def _in_hideout(self) -> bool:
        if 'hideout' in (self._share_data_connector.get_current_location() or '').lower():
            return True

        return False

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield ControlAction.ActionType

        self._enter_to_stash()
        if not self._inventory_maps:
            if self._grab_content(StashTab.MAPS) is False:
                yield ControlAction.EXIT

        CommonIOController.press(Key.esc)

        self._enter_to_map_device()
        time.sleep(0.1)

        self._move_content_into_device()
        self._activate_map_device()

        yield ControlAction.ActionType

        time.sleep(1.5)

        while self._loading_screen_to_map_scanner.get_condition_by_one() is False:
            self._enter_into_portal()
            time.sleep(action_settings.ENTER_INTO_PORTAL_INTERVAL)

        self._wait_until_not_in_location(lambda: (
            self._share_data_connector.get_current_location() is not None
            and not self._in_hideout()
        ))

        if self._check_map_content() is True:
            yield ControlAction.ActionType

        if not self._in_hideout():
            self._comeback_into_ho()
