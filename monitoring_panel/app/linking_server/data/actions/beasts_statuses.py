from ..structure import ResponseBeastsStatuses
from ....settings import settings
from ....structure import MachineStatus


async def beasts_statuses() -> ResponseBeastsStatuses:
    return ResponseBeastsStatuses(statuses={
        capturing_beast: status.value
        for capturing_beast in settings.CAPTURING_BEASTS
        for status in MachineStatus
        if capturing_beast in status.value
    })
