from enum import Enum
from pydantic import BaseModel

from PySide6.QtWidgets import QToolButton


class ControlEvent(Enum):

    DOOR: str = 'DOOR'
    PORTAL: str = 'PORTAL'
    INTO_HO: str = 'INTO_HO'
    PAUSE: str = 'PAUSE'
    RESUME: str = 'RESUME'
    INTO_FOUNDER_HO: str = 'INTO_FOUNDER_HO'


class EventSide(Enum):
    IDLE_SIDE: str = 'IDLE_SIDE'
    WORKER_SIDE: str = 'WORKER_SIDE'


class ControlEventButton(BaseModel):

    event: ControlEvent
    button: QToolButton
    event_side: EventSide = None

    class Config:
        arbitrary_types_allowed = 'allow'
