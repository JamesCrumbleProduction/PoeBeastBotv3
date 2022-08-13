from enum import Enum
from typing import Any
from pydantic import BaseModel, root_validator

from .helpers import build_url_base, staticclass
from ....settings import settings


class Service(Enum):
    SHARE_DATA: str = 'SHARE_DATA'
    LINKING_SERVER: str = 'LINKING_SERVER'


SERVICE_DESTINATIONS: dict[Service, str] = {
    Service.SHARE_DATA: build_url_base(
        settings.SHARE_DATA_SERVICE.SCHEME,
        settings.SHARE_DATA_SERVICE.ADDRESS,
        settings.SHARE_DATA_SERVICE.PORT
    ),
    Service.LINKING_SERVER: build_url_base(
        settings.LINKING_SERVER.SCHEME,
        settings.LINKING_SERVER.ADDRESS,
        settings.LINKING_SERVER.PORT
    )
}


class RequestMethod(Enum):
    GET: str = 'GET'
    PUT: str = 'PUT'
    POST: str = 'POST'
    PATCH: str = 'PATCH'


class RouteMeta(BaseModel):
    path: list[str]
    method: RequestMethod
    required_fields: list[str] = list()

    @root_validator
    def _validate_required_fields(cls, kwargs: dict[str, Any]) -> dict[str, Any]:
        method: RequestMethod = kwargs.get('method')
        required_fields = kwargs.get('required_fields')

        if method not in (
            RequestMethod.GET,
            RequestMethod.PATCH
        ) and not required_fields:
            raise NotImplementedError(
                f'Request "{method.value}" method should have required_fields but required_fields is empty'
            )

        return kwargs


@staticclass
class Routes:

    @staticclass
    class LinkingServer:

        prefixes: list[str] = []

        @staticclass
        class Data:
            prefixes: list[str] = ['data']

            available_statuses: str = 'available_statuses'
            beasts_statuses: str = 'beasts_statuses'
            extended_mode_status: str = 'extended_mode_status'

        @staticclass
        class Control:
            prefixes: list[str] = ['control']

            register_machine: str = 'register_machine'
            update_machine_status: str = 'update_machine_status'
            available_machines: str = 'available_machines'
            call_worked_to_pausing: str = 'call_worked_to_pausing'
            idles_to_founder: str = 'idles_to_founder'

        @staticclass
        class ServerStatus:
            prefixes: list[str] = ['status']

            server_status: str = 'server_status'

    @staticclass
    class ShareData:
        prefixes: list[str] = []

        get_content: str = 'get_content'
