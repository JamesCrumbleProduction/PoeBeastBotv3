from pydantic import BaseSettings


class Settings(BaseSettings):

    LOCATION_CHECK_RATE: float = 0.5


settings = Settings()
