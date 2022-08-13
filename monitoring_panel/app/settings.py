import logging

from pydantic import BaseSettings


class Settings(BaseSettings):

    PORT: int = 4000
    HOST: str = '0.0.0.0'

    LOGGING_LEVEL: int = logging.DEBUG
    LOGGING_FILENAME: str = 'logging'

    WORKERS: int = 3

    AUTO_SWITCH_AFTER_ALL_EVENT: bool = True
    EXTENDED_NETWORK_MODE: bool = True

    REQUEST_TIMEOUT: int = 1  # Seconds

    CAPTURING_BEASTS: list[str] = [
        'Fenumal Plagued Arachnid [Split an Item in Two]',
        'Craicic Chimeral [Imprint of a Magic Item]'
    ]


settings = Settings()
