from pydantic import BaseModel

from ....panel_data import MachineStatus


class Machine(BaseModel):

    name: str
    host: str
    port: int
    status: MachineStatus
