from pydantic import BaseModel


class ExecutableActionsResponse(BaseModel):

    actions: list[str]
