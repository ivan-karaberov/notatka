from typing import Annotated
from datetime import datetime

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


class PayloadSchema(BaseModel):
    sub: int
    role: str


class SessionSchema(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime