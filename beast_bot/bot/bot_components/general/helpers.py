import time

from enum import Enum
from dataclasses import dataclass
from httpx._exceptions import ConnectTimeout, ReadTimeout

from .requests_controller import Routes, Service, RequestsController
from ...services.logger import BOT_LOGGER


def static_dataclass(static_dataclass):

    def wrapper():
        nonlocal static_dataclass

        static_dataclass = dataclass(static_dataclass)

        def __new__(cls, *args, **kwargs):
            return cls

        static_dataclass.__new__ = __new__

        return static_dataclass
    return wrapper()


def wait_monitoring_server_connection() -> None:
    BOT_LOGGER.info('Trying to connect to the linking server...')

    while True:
        try:

            if response_data := RequestsController.execute(
                Service.LINKING_SERVER,
                Routes.LinkingServer.ServerStatus.server_status,
                serialize=True,
                exc_info=False,
                raise_condition=True
            ):
                response_data: dict[str, str]
                if response_data.get('status') is not None:
                    BOT_LOGGER.info('Connected !!!. Starting to data init')
                    break

        except (ConnectTimeout, TimeoutError, ReadTimeout) as exception:
            BOT_LOGGER.info(
                f'Linking server doesn\'t responsing... Part of exception: {exception}'
            )

        BOT_LOGGER.info('New request will execute in 2 seconds...')
        time.sleep(2)


def build_machine_statuses() -> Enum:

    statuses: list[str] = RequestsController.execute(
        Service.LINKING_SERVER,
        Routes.LinkingServer.Data.available_statuses,
        serialize=True
    )['statuses']

    return Enum(
        'MachineStatus', {
            status: status
            for status in statuses
        }
    )


def build_beasts_statuses(statuses_enum: Enum) -> dict[str, Enum]:
    return {
        beast_label: statuses_enum(status)
        for beast_label, status in RequestsController.execute(
            Service.LINKING_SERVER,
            Routes.LinkingServer.Data.beasts_statuses,
            serialize=True
        )['statuses'].items()
    }


def get_extended_mode_status() -> bool:
    return RequestsController.execute(
        Service.LINKING_SERVER,
        Routes.LinkingServer.Data.extended_mode_status,
        serialize=True
    )
