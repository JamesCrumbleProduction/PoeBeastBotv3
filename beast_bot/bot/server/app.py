from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .components import (
    control_router,
    from_hud_router
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)

app.include_router(
    control_router,
    prefix='/control',
    tags=['Control']
)
app.include_router(
    from_hud_router,
    prefix='/from_hud',
    tags=['From Hud Data']
)
