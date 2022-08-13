import socket
import logging

from pydantic import BaseSettings, validator

from .helpers import get_source_fields


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
    FILENAME: str = 'logging'
    CLEAR_FILE_SIZE_LIMIT: int = 10  # in megabytes


class Settings(BaseSettings):

    WORKERS: int = 3
    REQUEST_TIMEOUT: int = 1  # seconds

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


settings = Settings()
