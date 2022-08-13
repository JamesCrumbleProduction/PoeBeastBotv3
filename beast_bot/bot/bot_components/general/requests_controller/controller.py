import httpx
import orjson

from typing import Any
from concurrent.futures import Future

from .routes_meta import ROUTES_META
from .exceptions import RequestError, RequiredFieldError
from .structure import Service, RouteMeta, SERVICE_DESTINATIONS
from ....settings import settings
from ....services.logger import REQUESTS_LOGGER
from ....services.executor import REQUESTS_EXECUTOR


def build_url(service: Service, route_path: list[str]) -> str:
    return f'{SERVICE_DESTINATIONS[service]}{"/".join(route_path)}'


def validate_fields(
    route_meta: RouteMeta,
    params: dict[str, Any],
    body: dict[str, Any]
) -> None:
    for req_field in route_meta.required_fields:
        if req_field not in body and req_field not in params:
            raise RequiredFieldError(
                f'"{req_field}" field should exist '
                f'in params or body of "{route_meta.path[-1]}" route endpoint'
            )


class RequestsController:

    @staticmethod
    def _execute_request(
        service: Service,
        endpoint: str,
        params: dict[str, Any],
        body: dict[str, Any],
        serialize: bool,
        timeout: int,
        exc_info: bool,
        raise_condition: bool
    ) -> Any | None:

        route_meta = ROUTES_META.get(service, endpoint)
        validate_fields(route_meta, params, body)
        route_url = build_url(service, route_meta.path)

        try:
            with httpx.Client() as client:
                response = client.request(
                    route_meta.method.value,
                    route_url,
                    params=params or None,
                    json=body or None,
                    timeout=timeout
                )
        except Exception as exception:
            if raise_condition is True:
                raise exception

            REQUESTS_LOGGER.warning(
                f'{RequestError(exception)}... URL: {route_url}', exc_info=exc_info
            )
        else:
            if serialize is True:
                return orjson.loads(response.text)
            return response.text

    @staticmethod
    def execute(
        service: Service,
        endpoint: str,
        *,
        params: dict[str, Any] = dict(),
        body: dict[str, Any] = dict(),
        serialize: bool = False,
        timeout: int = settings.REQUEST_TIMEOUT,
        exc_info: bool = True,
        raise_condition: bool = False
    ) -> Any | None:
        return RequestsController._execute_request(
            service, endpoint, params,
            body, serialize, timeout, exc_info, raise_condition
        )

    @staticmethod
    def execute_in_thread(
        service: Service,
        endpoint: str,
        *,
        params: dict[str, Any] = dict(),
        body: dict[str, Any] = dict(),
        serialize: bool = False,
        timeout: int = settings.REQUEST_TIMEOUT,
        exc_info: bool = True,
        raise_condition: bool = False
    ) -> Future:
        return REQUESTS_EXECUTOR.submit(
            RequestsController._execute_request,
            service, endpoint, params, body, serialize,
            timeout, exc_info, raise_condition
        )
