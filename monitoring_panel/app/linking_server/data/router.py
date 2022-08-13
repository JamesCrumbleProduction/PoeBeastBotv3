from fastapi import APIRouter

from .structure import (
    ResponseStatuses,
    ResponseBeastsStatuses
)
from .actions import (
    beasts_statuses,
    available_statuses,
    extended_mode_status
)

router = APIRouter()

router.add_api_route(
    path='/available_statuses',
    endpoint=available_statuses,
    methods=['GET'],
    status_code=200,
    response_model=ResponseStatuses
)
router.add_api_route(
    path='/beasts_statuses',
    endpoint=beasts_statuses,
    methods=['GET'],
    status_code=200,
    response_model=ResponseBeastsStatuses
)
router.add_api_route(
    path='/extended_mode_status',
    endpoint=extended_mode_status,
    methods=['GET'],
    status_code=200
)
