from numpy import ndarray
from pydantic import BaseModel


class CompiledTemplate(BaseModel):
    label: str
    template_data: ndarray

    class Config:
        arbitrary_types_allowed = 'allow'
