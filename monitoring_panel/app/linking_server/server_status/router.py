from fastapi import APIRouter

from .actions import (
    server_status
)

router = APIRouter()

router.add_api_route(
    path='/server_status',
    endpoint=server_status,
    methods=['GET'],
    status_code=200
)
