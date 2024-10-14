from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, validator


class BaseSignSchema(BaseModel):
    username: Annotated[str, Field(max_length=32)]
    password: Annotated[str, Field(min_length=6)]

    @validator('username')
    def lowercase_username(cls, v):
        return v.lower()


class SignUpSchema(BaseSignSchema):
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]


class SignInSchema(BaseSignSchema):
    pass


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class PayloadSchema(BaseModel):
    sub: int
    role: Annotated[str, Field(max_length=8)]
    session_uuid: str
    is_refresh: bool


class SessionSchema(BaseModel):
    session_uuid: str
    user_id: int
    refresh_token: str
    expires_at: datetime