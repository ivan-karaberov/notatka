from typing import Annotated

from pydantic import BaseModel, Field


class SignUpSchema(BaseModel):
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    password: str


class SignInSchema(BaseModel):
    username: Annotated[str, Field(max_length=32)]
    password: str


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
