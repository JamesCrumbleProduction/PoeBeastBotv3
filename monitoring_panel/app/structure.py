from enum import Enum
from pydantic import BaseModel

from .settings import settings


MACHINE_PLACEHOLDER: str = '{name}: {status}'


MachineStatus = Enum(
    'MachineStatus',
    dict(
        **{
            f'FOUNDER ({beast})': f'FOUNDER ({beast})'
            for beast in settings.CAPTURING_BEASTS
        },
        WORKING='WORKING',
        PAUSED='PAUSED',
        PAUSING='PAUSING',
        FOUNDER_AVAILABLE='FOUNDER_AVAILABLE',
        ERROR='ERROR',
        OUT_OF_MAPS='OUT_OF_MAPS',
        OUT_OF_SCARABS='OUT_OF_SCARABS',
        HUD_PROBLEM='HUD_PROBLEM',
        IDLE_MEMBER='IDLE_MEMBER'
    )
)


class Machine(BaseModel):
    name: str
    host: str
    port: int
    status: MachineStatus

    def is_idle_member(self) -> bool:
        return self.status is MachineStatus.IDLE_MEMBER

    def extended_output_format(self) -> str:
        return (
            ' - (worker)'
            if not self.is_idle_member()
            else ' - (idle)'
        ) if settings.EXTENDED_NETWORK_MODE is True else ''

    def output_format(self) -> str:
        return MACHINE_PLACEHOLDER.format(
            name=self.name,
            status=self.status.value
        )
