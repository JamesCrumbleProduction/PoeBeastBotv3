from pydantic import BaseSettings


class Settings(BaseSettings):

    HUD_PROBLEM_TIMEOUT: float = 10.0
    INIT_TAB_CONTENT_INTERVAL: float = 0.1
    ENTER_TO_INTERVAL: float = 0.1
    GRAB_CONTENT_CLIPBOARD_INTERBAL: float = 0.05
    GRAB_CONTENT_TIMEOUT: float = 5.5
    CHECK_MAP_CONTENT_INTERVAL: float = 0.1
    WAIT_UNTIL_NOT_IN_LOCATION_INTEVAL: float = 0.1
    ENTER_INTO_PORTAL_INTERVAL: float = 0.3
    PARTY_ACCEPT_INTERVAL: float = 1.0


settings = Settings()
