from ....settings import settings


async def extended_mode_status() -> bool:
    return settings.EXTENDED_NETWORK_MODE
