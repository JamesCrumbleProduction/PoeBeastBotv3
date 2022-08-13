import time
import pyperclip

from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from .structure import IterateByAxis
from ..world_to_screen import Coordinate
from ....settings import settings


MOUSE = MouseController()
KEYBOARD = KeyboardController()


class CommonIOController:

    @staticmethod
    def move(coordinate: Coordinate) -> None:
        MOUSE.position = coordinate.tuple_format()

    @staticmethod
    def press(key: Key) -> None:
        KEYBOARD.press(key)
        KEYBOARD.release(key)

    @staticmethod
    def grab() -> None:
        KEYBOARD.press(Key.ctrl)
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

        MOUSE.click(Button.left)
        KEYBOARD.release(Key.ctrl)
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

    @staticmethod
    def move_and_grab(coordinate: Coordinate) -> None:

        CommonIOController.move(coordinate)
        CommonIOController.grab()

    @staticmethod
    def move_and_click(coordinate: Coordinate) -> None:

        CommonIOController.move(coordinate)
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

        MOUSE.click(Button.left)
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

    @staticmethod
    def chat_text_command(text: str) -> None:

        KEYBOARD.press(Key.enter)
        KEYBOARD.release(Key.enter)
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

        KEYBOARD.type(text)

        KEYBOARD.press(Key.enter)
        KEYBOARD.release(Key.enter)


class ClipboardIOController:

    __slots__ = ()

    def _clear_clipboard(self) -> None:
        pyperclip.copy('')

    def _copy_to_clipboard(self) -> None:
        KEYBOARD.press(Key.ctrl_l)
        KEYBOARD.press('c')
        time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)
        KEYBOARD.release('c')
        KEYBOARD.release(Key.ctrl_l)

    def get_clipboard_data(self) -> str | None:
        self._clear_clipboard()
        self._copy_to_clipboard()

        data = pyperclip.paste()

        return None if data == '' else data


class IterateIOController:

    __slots__ = (
        '_start_position',
    )

    def __init__(self, start_position: Coordinate) -> None:
        self._start_position = start_position

    def iterate_with_move_and_replace_action(
        self,
        gap_coordinate: Coordinate,
        iterate_by_axis: IterateByAxis,
        switch_value: int,
        iterate_count: int,
        start: int = 1
    ) -> None:
        '''
        Isn't checking over-resolution part
        Using when you know about what this method do
        '''

        switcher: int = 0
        movable_coordinate = self._start_position.copy()

        for i in range(1, iterate_count * switch_value + 1):
            if start <= i:
                CommonIOController.move_and_grab(movable_coordinate)
                time.sleep(settings.IO_SERVICE.CLICK_INTERVAL)

            if switch_value > switcher:
                switcher += 1
                match iterate_by_axis:
                    case IterateByAxis.X:
                        movable_coordinate.y += gap_coordinate.y
                    case IterateByAxis.Y:
                        movable_coordinate.x += gap_coordinate.x
            else:
                switcher = 1
                match iterate_by_axis:
                    case IterateByAxis.X:
                        movable_coordinate.x = self._start_position.x + gap_coordinate.x
                        movable_coordinate.y = self._start_position.y
                    case IterateByAxis.Y:
                        movable_coordinate.x = self._start_position.x
                        movable_coordinate.y = self._start_position.y + gap_coordinate.y
