from fastapi import APIRouter

from .structure import CurrentLocation, LocationContent
from .actions import (
    update_location_content,
    update_current_location,
    get_location_content,
    get_current_location
)


router = APIRouter()

router.add_api_route(
    path='/update_location_content',
    endpoint=update_location_content,
    methods=['POST'],
    status_code=200
)
router.add_api_route(
    path='/update_current_location',
    endpoint=update_current_location,
    methods=['POST'],
    status_code=200
)
router.add_api_route(
    path='/get_location_content',
    endpoint=get_location_content,
    methods=['GET'],
    status_code=200,
    response_model=LocationContent | None
)
router.add_api_route(
    path='/get_current_location',
    endpoint=get_current_location,
    methods=['GET'],
    status_code=200,
    response_model=CurrentLocation | None
)
