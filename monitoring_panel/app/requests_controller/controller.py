import orjson
import requests

from typing import Any
from concurrent.futures import Future


from .structure import (
    Route,
    RoutePrefix,
    RequestEvent,
    RequestMethod,
    ConnectionRoutes
)
from .exceptions import (
    RequestError,
    RequiredFieldError,
    RequestExecutionError
)
from ..structure import Machine
from ..settings import settings
from ..services.executor import REQUESTS_EXECUTOR


REQUEST_PLACEHOLDER: str = (
    'http://{host}:{port}/{prefix}/{endpoint}'
)


class RequestsController:

    _existed_ConnectionRoutes: dict[RoutePrefix, dict[str, Route]] = None

    def __init__(self):
        self._init_existed_ConnectionRoutes()

    def _init_existed_ConnectionRoutes(cls) -> None:
        if cls._existed_ConnectionRoutes is None:
            cls._existed_ConnectionRoutes = dict()

            cls._existed_ConnectionRoutes[RoutePrefix.CONTROL] = {
                ConnectionRoutes.ControlMachine.change_status: Route(
                    endpoint=ConnectionRoutes.ControlMachine.change_status,
                    method=RequestMethod.POST,
                    required_fields=[
                        'status'
                    ]
                ),
                ConnectionRoutes.ControlMachine.execute_action: Route(
                    endpoint=ConnectionRoutes.ControlMachine.execute_action,
                    method=RequestMethod.POST,
                    required_fields=[
                        'action'
                    ]
                )
            }

    def _validate_fields(
        self,
        route: Route,
        fields: dict[str, Any]
    ) -> None:
        for req_field in route.required_fields:
            if req_field not in fields:
                raise RequiredFieldError(
                    f'"{req_field}" field should exist in params or fields of request'
                )

    def _execute_request(
        self,
        machine: Machine,
        request_event: RequestEvent,
        body: dict[str, Any],
        serialize: bool,
        timeout: int
    ) -> Any | None:

        if request_event.prefix not in self._existed_ConnectionRoutes:
            raise RequestExecutionError(
                f'Unknown "{request_event.prefix}" prefix'
            )
        available_prefix_ConnectionRoutes = self._existed_ConnectionRoutes[request_event.prefix]

        if request_event.route not in available_prefix_ConnectionRoutes:
            raise RequestExecutionError(
                f'Unknown "{request_event.route}" endpoint for "{request_event.prefix}" prefix'
            )

        route = available_prefix_ConnectionRoutes[request_event.route]

        url = REQUEST_PLACEHOLDER.format(
            host=machine.host,
            port=machine.port,
            prefix=request_event.prefix.value,
            endpoint=route.endpoint
        )

        self._validate_fields(route, route.required_fields)

        try:
            response = requests.request(
                route.method.value,
                url,
                json=body,
                params=request_event.params,
                timeout=timeout
            )
        except Exception as exception:
            raise RequestError(exception)
        else:
            if serialize is True:
                return orjson.loads(response.text)
            return response.text

    def execute(
        self,
        machine: Machine,
        request_event: RequestEvent,
        *,
        body: dict[str, Any] = dict(),
        serialize: bool = False,
        timeout: int = settings.REQUEST_TIMEOUT
    ) -> Any | None:
        return self._execute_request(
            machine, request_event,
            body, serialize, timeout
        )

    def execute_in_thread(
        self,
        machine: Machine,
        request_event: RequestEvent,
        *,
        body: dict[str, Any] = dict(),
        serialize: bool = False,
        timeout: int = settings.REQUEST_TIMEOUT
    ) -> Future[Any | None]:
        return REQUESTS_EXECUTOR.submit(
            self._execute_request,
            machine, request_event,
            body, serialize, timeout
        )
