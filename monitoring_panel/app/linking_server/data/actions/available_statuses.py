from ..structure import ResponseStatuses
from ....structure import MachineStatus


async def available_statuses() -> ResponseStatuses:
    return ResponseStatuses(
        statuses=[
            status
            for status in MachineStatus
        ]
    )
