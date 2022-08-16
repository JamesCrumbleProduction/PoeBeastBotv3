import os
import orjson
import logging

from pydantic import BaseSettings

SAVE_SETTINGS: bool = True
SAVE_SETTINGS_FILENAME: str = 'saved_settings.json'
SAVE_SETTINGS_PATH: str = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    SAVE_SETTINGS_FILENAME
)


class Settings(BaseSettings):

    PORT: int = 4000
    HOST: str = '0.0.0.0'

    LOGGING_LEVEL: int = logging.DEBUG
    LOGGING_FILENAME: str = 'logging.log'
    LOGGING_CLEAR_FILE_SIZE_LIMIT: int = 10  # in megabytes

    WORKERS: int = 3

    AUTO_SWITCH_AFTER_ALL_EVENT: bool = True
    EXTENDED_NETWORK_MODE: bool = True

    REQUEST_TIMEOUT: int = 1  # Seconds

    CAPTURING_BEASTS: list[str] = [
        'Fenumal Plagued Arachnid [Split an Item in Two]',
        'Craicic Chimeral [Imprint of a Magic Item]'
    ]

    def save_settings(self) -> None:
        if not SAVE_SETTINGS:
            return

        with open(SAVE_SETTINGS_PATH, 'w') as handle:
            handle.write(self.json())


settings = Settings()

if SAVE_SETTINGS is True:
    if os.path.exists(SAVE_SETTINGS_PATH):
        with open(SAVE_SETTINGS_PATH, 'r') as handle:
            settings = Settings(**orjson.loads(handle.read()))
