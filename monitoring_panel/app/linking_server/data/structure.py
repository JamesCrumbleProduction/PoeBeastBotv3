from pydantic import BaseModel

from ...structure import MachineStatus


class ResponseStatuses(BaseModel):

    statuses: list[MachineStatus]


class ResponseBeastsStatuses(BaseModel):

    statuses: dict[str, str]
