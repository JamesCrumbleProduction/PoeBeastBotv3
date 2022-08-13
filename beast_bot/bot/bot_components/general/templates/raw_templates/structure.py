from pydantic import BaseModel


class RawTemplate(BaseModel):
    label: str
    path: str

    class Config:
        arbitrary_types_allowed = 'allow'
