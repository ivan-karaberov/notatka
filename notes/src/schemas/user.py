from typing import Annotated

from pydantic import BaseModel, Field


class UserPayloadSchema(BaseModel):
    sub: int
    role: Annotated[str, Field(max_length=8)]
    session_uuid: str
    is_refresh: bool