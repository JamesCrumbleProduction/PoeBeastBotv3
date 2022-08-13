from ....services.logger import BOT_LOGGER


def build_url_base(scheme: str, address: str, port: int) -> str:
    return f'{scheme}{address}:{port}/'


def staticclass(cls):

    cls._instance = cls()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls()
            return cls._instance

        BOT_LOGGER.warning(
            f'"{cls.__name__}" class is staticclass and cannot be create as instance'
        )
    cls.__new__ = __new__

    return cls
