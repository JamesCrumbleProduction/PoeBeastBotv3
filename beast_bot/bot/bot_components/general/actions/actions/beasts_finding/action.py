import time

from dataclasses import fields
from pynput.keyboard import Key
from typing import Iterator, Callable, Any

from .exceptions import UnknownStashTab
from .structure import TabMeta, StashTab
from .settings import settings as action_settings

from ...actions_init import ACTIONS
from ...abstract_action import AbstractAction
from ....sounds_handler import SoundOperation
from ....bot_data_adapter import BotDataAdapter
from ....templates import BEAST_BOT_COMPILED_TEMPLATES
from ....panel_data import BEASTS_STATUSES, EXTENDED_MODE, MachineStatus
from ....structure import (
    Regions,
    Coordinates,
    ControlAction
)
from ....world_to_screen import (
    TemplateScanner,
    HSVPortalScanner,
    ShareDataConnector
)
from ....io_controllers import (
    IterateByAxis,
    IterateIOController,
    CommonIOController,
    ClipboardIOController
)
from ....requests_controller import (
    Routes,
    Service,
    RequestsController
)
from ......settings import settings
from ......services.logger import BOT_LOGGER
from ......server.components.from_hud.structure import LocationContent

PARTY_ACCEPT_ACTION: str = 'PartyAccept'


class BeastsFindingAction(AbstractAction):

    __slots__ = (
        '_permissions',
        '_maps_scanner',
        '_stash_scanner',
        '_tabs_coordinates',
        '_scarabs_scanner',
        '_ressurect_scanner',
        '_stash_io_controller',
        '_share_data_connector',
        '_hsv_portal_scanner',
        '_map_device_scanner',
        '_past_location_content',
        '_inventory_io_controller',
        '_unloaded_stash_scanner',
        '_loading_screen_to_ho_scanner',
        '_loading_screen_to_map_scanner',
    )

    def __init__(self, bot_data_adapter: BotDataAdapter):
        super().__init__(bot_data_adapter)
        self._permissions = set()
        self._past_location_content: LocationContent = None

        self._init_stash_data()
        self._init_scanners()
        self._init_controllers()
        self._init_connectors()

    @property
    def permissions(self) -> set[MachineStatus]:
        return self._permissions

    def _init_stash_data(self) -> None:
        self._tabs_coordinates: dict[StashTab, TabMeta] = {
            StashTab.MAPS: TabMeta(*list(
                field.default
                for field in fields(Coordinates.Stash.MapTabs)
            )),
            StashTab.SCARABS: TabMeta(*list(
                field.default
                for field in fields(Coordinates.Stash.ScarabTabs)
            ))
        }
        BOT_LOGGER.debug('"BeastsFindingAction": STASH DATA WAS INITED')

    def _init_connectors(self) -> None:
        self._share_data_connector = ShareDataConnector()
        BOT_LOGGER.debug('"BeastsFindingAction": CONNECTORS WAS INITED')

    def _init_scanners(self) -> None:

        self._hsv_portal_scanner = HSVPortalScanner(Regions.portals_region)
        self._maps_scanner = TemplateScanner(
            iterable_templates=BEAST_BOT_COMPILED_TEMPLATES.maps_templates.templates,
            region=Regions.stash_region, threshold=0.45
        )
        self._scarabs_scanner = TemplateScanner(
            iterable_templates=BEAST_BOT_COMPILED_TEMPLATES.scarabs_templates.templates,
            region=Regions.stash_region, threshold=0.6
        )
        self._stash_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.nametags_templates.get('stash'),
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get('stash_label'),
            threshold=0.9
        )
        self._unloaded_stash_scanner = TemplateScanner(
            BEAST_BOT_COMPILED_TEMPLATES.other_templates.get(
                'empty_inventory_socket'
            ), region=Regions.stash_region, threshold=0.9
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
        BOT_LOGGER.debug('"BeastsFindingAction": SCREEN SCANNERS WAS INITED')

    def _init_controllers(self) -> None:
        self._stash_io_controller = ClipboardIOController()
        self._inventory_io_controller = IterateIOController(
            Coordinates.first_socket_inventory_position
        )
        BOT_LOGGER.debug('"BeastsFindingAction": CONTROLLERS WAS INITED')

    def _init_tab_content(self, tab: StashTab) -> None:

        if tab == StashTab.MAPS:
            scanner = self._maps_scanner
        elif tab == StashTab.SCARABS:
            scanner = self._scarabs_scanner
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
            if coord := self._stash_scanner.indentify_by_first():
                CommonIOController.move_and_click(coord)
                time.sleep(0.3)

            if (
                self._unloaded_stash_scanner.get_condition_by_one() is True
                or self._scarabs_scanner.get_condition_by_one() is True
                or self._maps_scanner.get_condition_by_one() is True
            ):
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

    def _grab_content(self, tab: StashTab) -> bool:
        if tab_meta := self._tabs_coordinates.get(tab):

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

            CommonIOController.move(tab_meta.tab_content.pop())
            time.sleep(0.05)

            start = time.time()

            while True:
                if self._stash_io_controller.get_clipboard_data() is not None:
                    CommonIOController.grab()
                    break

                if time.time() - start >= action_settings.GRAB_CONTENT_TIMEOUT:
                    return self._grab_content(tab)

                time.sleep(action_settings.GRAB_CONTENT_CLIPBOARD_INTERBAL)

            return True

        raise UnknownStashTab(
            f'Unknown "{tab}" value of "tab" argument'
        )

    def _scarab_in_device(self) -> bool:
        return self._scarabs_scanner(
            as_custom_region=Regions.map_device_sockets_region
        ).get_condition_by_one()

    def _move_content_into_device(self) -> None:
        self._inventory_io_controller.iterate_with_move_and_replace_action(
            Coordinates.sockets_gap, IterateByAxis.X, switch_value=2, iterate_count=1
        )

    def _activate_map_device(self) -> None:
        CommonIOController.move_and_click(
            Coordinates.activate_map_device_button
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

    def _is_location_and_content_updated(self) -> bool:
        if (
            self.bot_data_adapter.content is not None
            and self.bot_data_adapter.content.last_update != (
                self._past_location_content
                if self._past_location_content is None
                else self._past_location_content.last_update
            )
        ):
            return True

        return False

    def _check_map_content(self) -> bool:

        started_time = time.time()

        while True:
            if self._is_location_and_content_updated():

                for founded_beasts in self.bot_data_adapter.content.content:
                    if founded := BEASTS_STATUSES.get(founded_beasts):
                        self.bot_data_adapter.update_status(founded)
                        if not EXTENDED_MODE:
                            RequestsController.execute_in_thread(
                                Service.LINKING_SERVER,
                                Routes.LinkingServer.Control.call_worked_to_pausing
                            )
                        if settings.NOTIFY_BY_SOUND is True:
                            SoundOperation.execute_audio(
                                SoundOperation.choice_random_alert()
                            )
                        if settings.NOTIFY_BY_MESSAGE is True and settings.PARTY_LEADER_NICKNAME:
                            CommonIOController.chat_text_command(
                                f'@{settings.PARTY_LEADER_NICKNAME} {settings.MESSAGE_PLACEHOLDER.format(beast=founded)}'
                            )
                        break

                self._past_location_content = self.bot_data_adapter.content

                if self.bot_data_adapter.status is MachineStatus.HUD_PROBLEM:
                    self.bot_data_adapter.update_status(
                        MachineStatus.WORKING
                    )

                return self.bot_data_adapter.status in BEASTS_STATUSES.values()

            if (
                self._is_hud_problem(started_time) is True
                and self.bot_data_adapter.status is MachineStatus.WORKING
            ):
                self.bot_data_adapter.update_status(
                    MachineStatus.HUD_PROBLEM
                )

            time.sleep(action_settings.CHECK_MAP_CONTENT_INTERVAL)

    def _wait_until_party_is_accepted(self) -> None:
        while True:
            for action in ACTIONS[PARTY_ACCEPT_ACTION].action.execute_action():
                if not settings.PARTY_ACCEPT_LOCK:
                    if self.bot_data_adapter.status in (
                        MachineStatus.WORKING,
                    ):
                        return

                if action is ControlAction.DONE:
                    RequestsController.execute(
                        Service.LINKING_SERVER,
                        Routes.LinkingServer.Control.idles_to_founder,
                        params={
                            'founder': settings.INGAME_CHAR_NAME,
                            'machine_name': settings.VM_NAME
                        }
                    )
                    return

            time.sleep(action_settings.PARTY_ACCEPT_INTERVAL)

    def _is_hud_problem(self, started_time: float) -> bool:
        return time.time() - started_time >= action_settings.HUD_PROBLEM_TIMEOUT

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
            self.bot_data_adapter.location is not None
            and self._in_hideout()
        ))

    def _in_hideout(self) -> bool:
        if 'hideout' in self.bot_data_adapter.location.current_location.lower():
            return True

        return False

    def execute_action(self, **action_kwargs: dict[str, Any]) -> Iterator[ControlAction]:
        yield ControlAction.ActionType

        self._enter_to_stash()
        if self._grab_content(StashTab.MAPS) is False:
            yield ControlAction.EXIT

        CommonIOController.press(Key.esc)

        self._enter_to_map_device()
        time.sleep(0.1)

        if self._scarab_in_device() is False:
            CommonIOController.press(Key.esc)
            self._enter_to_stash()

            if self._grab_content(StashTab.SCARABS) is False:
                yield ControlAction.EXIT

            CommonIOController.press(Key.esc)

            self._enter_to_map_device()

        self._move_content_into_device()
        self._activate_map_device()

        yield ControlAction.ActionType

        time.sleep(1.5)

        while self._loading_screen_to_map_scanner.get_condition_by_one() is False:
            self._enter_into_portal()
            time.sleep(action_settings.ENTER_INTO_PORTAL_INTERVAL)

        self._wait_until_not_in_location(lambda: (
            self.bot_data_adapter.location is not None
            and not self._in_hideout()
        ))

        if self._check_map_content() is True:
            if settings.IS_PARTY_MEMBER is False and EXTENDED_MODE is True:
                self._wait_until_party_is_accepted()

            yield ControlAction.ActionType

        if not self._in_hideout():
            self._comeback_into_ho()
