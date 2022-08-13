from fastapi import APIRouter

from .structure import ExecutableActionsResponse
from .actions import (
    change_status,
    execute_action,
    get_executable_actions
)


router = APIRouter()

router.add_api_route(
    path='/change_status',
    endpoint=change_status,
    methods=['POST'],
    status_code=200
)
router.add_api_route(
    path='/execute_action',
    endpoint=execute_action,
    methods=['POST'],
    status_code=200
)
router.add_api_route(
    path='/get_executable_actions',
    endpoint=get_executable_actions,
    methods=['GET'],
    status_code=200,
    response_model=ExecutableActionsResponse
)
