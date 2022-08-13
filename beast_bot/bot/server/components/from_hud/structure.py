from pydantic import BaseModel


class LocationContent(BaseModel):

    content: list[str]
    last_update: str


class CurrentLocation(BaseModel):

    current_location: str
