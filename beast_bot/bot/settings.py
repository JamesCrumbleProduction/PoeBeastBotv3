import os
import socket
import orjson
import logging

from pydantic import BaseSettings, validator

from .helpers import get_source_fields


SAVE_SETTINGS: bool = True
SAVE_SETTINGS_FILENAME: str = 'saved_settings.json'
SAVE_SETTINGS_PATH: str = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    SAVE_SETTINGS_FILENAME
)


class ShareDataServiceSettings(BaseSettings):

    PORT: int = 50000
    SCHEME: str = 'http://'
    ADDRESS: str = socket.gethostbyname(socket.gethostname())

    PORTAL_PREFIX: str = 'TownPortal'


class BotServerSettings(BaseSettings):

    PORT: int = 4001
    HOST: str = '0.0.0.0'


class LinkingServerSettings(BaseSettings):

    PORT: int = 4000
    SCHEME: str = 'http://'
    ADDRESS: str = '127.0.0.1'


class IOServiceSettings(BaseSettings):

    CLICK_INTERVAL: float = 0.1


class LoggingSettings(BaseSettings):

    LEVEL: int = logging.DEBUG
    FILENAME: str = 'logging.log'
    CLEAR_FILE_SIZE_LIMIT: int = 10  # in megabytes


class Settings(BaseSettings):

    WORKERS: int = 3
    REQUEST_TIMEOUT: int = 1  # seconds

    AUTO_UPDATE: bool = True

    VM_NAME: str = 'v3.18'  # Machine name (showing in monitoring panel)
    # should be feeled when NOTIFY_BY_MESSAGE was enabled
    PARTY_LEADER_NICKNAME: str = ''
    INGAME_CHAR_NAME: str = ''  # using for chat command etc.
    IS_PARTY_MEMBER: bool = True

    NOTIFY_BY_SOUND: bool = False
    NOTIFY_BY_MESSAGE: bool = False
    MESSAGE_PLACEHOLDER: str = 'hey I found {beast}'

    # SHARE DATA HUD PLUGIN SHOULD BE TURNED ON
    SHARE_DATA_PORTAL_VALIDATOR: bool = True

    # When True your bot can unlock party accept loop when get "WORKING" status
    PARTY_ACCEPT_LOCK: bool = False

    LINKING_SERVER = LinkingServerSettings()
    LOGGING = LoggingSettings()
    BOT_SERVER = BotServerSettings()
    IO_SERVICE = IOServiceSettings()
    SHARE_DATA_SERVICE = ShareDataServiceSettings()

    @validator('MESSAGE_PLACEHOLDER', check_fields=True)
    def __validate_message_placeholder(cls, value: str) -> str:
        fields = get_source_fields(value)

        if 'beast' in fields and len(fields) == 1:
            return value

        raise ValueError(
            'MESSAGE_PLACEHOLDER should have only one "{beast}" placeholder'
        )

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
