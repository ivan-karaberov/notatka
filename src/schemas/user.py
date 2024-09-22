from typing import Annotated

from pydantic import BaseModel, Field


class SingUpSchema(BaseModel):
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    password: str
