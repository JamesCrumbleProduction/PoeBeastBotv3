from pydantic import BaseModel, validator

from .helpers import parse_str_vector_to_dict
from ...structure import Coordinate


class Vector2D(BaseModel):

    x: float
    y: float


class Vector3D(Vector2D):

    z: float


class Entity(BaseModel):

    bounds_center_pos: Vector3D
    grid_pos: Vector2D
    pos: Vector3D
    on_screen_position: Vector2D
    distance_to_player: float
    additional_info: str

    @validator(
        'pos',
        'grid_pos',
        'bounds_center_pos',
        'on_screen_position',
        pre=True
    )
    def _validate_vectors(cls, value: str) -> dict[str, str]:
        return parse_str_vector_to_dict(value)

    @validator('distance_to_player', pre=True)
    def _validate_distance_to_player(cls, value: str) -> float:
        return float(value.replace(',', '.'))

    def screen_coordinate(self) -> Coordinate:
        return Coordinate(
            x=self.on_screen_position.x,
            y=self.on_screen_position.y
        )
