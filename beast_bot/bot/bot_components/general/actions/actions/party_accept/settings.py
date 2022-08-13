from pydantic import BaseSettings


class Settings(BaseSettings):

    AWAIT_TO_CHECK_CONDITION_INTERVAL: float = 0.3


settings = Settings()
