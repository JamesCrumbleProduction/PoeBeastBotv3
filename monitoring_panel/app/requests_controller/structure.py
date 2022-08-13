from enum import Enum
from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel, root_validator


class RoutePrefix(Enum):
    CONTROL: str = 'control'


class RequestMethod(Enum):
    GET: str = 'GET'
    POST: str = 'POST'


class RequestEvent(BaseModel):
    prefix: RoutePrefix
    route: str
    params: dict[str, str]


class Route(BaseModel):
    endpoint: str
    method: RequestMethod
    required_fields: list[str] = None

    @root_validator
    def _validate_required_fields(cls, kwargs: dict[str, Any]) -> dict[str, Any]:
        method: RequestMethod = kwargs.get('method')
        required_fields = kwargs.get('required_fields')

        if method == RequestMethod.POST and required_fields is None:
            raise NotImplementedError(
                f'Post method should have required_fields but required_fields is "{required_fields}"'
            )

        return kwargs


@dataclass
class ConnectionRoutes:

    @dataclass
    class ControlMachine:
        change_status: str = 'change_status'
        execute_action: str = 'execute_action'
