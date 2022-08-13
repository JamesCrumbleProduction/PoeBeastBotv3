import numpy as np

from pydantic import BaseModel


class ValidatedTemplateData(BaseModel):
    location_x: np.ndarray
    location_y: np.ndarray
    height: int
    width: int

    class Config:
        arbitrary_types_allowed = 'allow'


class Region(BaseModel):
    width: int
    height: int
    left: int
    top: int


class Coordinate(BaseModel):
    x: int
    y: int

    def tuple_format(self) -> tuple[int, int]:
        return self.x, self.y
