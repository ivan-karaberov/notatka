from typing import Annotated, Optional, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, validator

from .auth import SignUpSchema


class AccountDetailSchema(BaseModel):
    id: int
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    role: Annotated[str, Field(max_length=8)]
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool

    @validator('username')
    def lowercase_username(cls, v):
        return v.lower()


class AllAccountsSchema(BaseModel):
    accounts: List[AccountDetailSchema]
    total_pages: int


class UpdateAccountSchema(BaseModel):
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class AdminCreateAccountSchema(SignUpSchema):
    role: Annotated[str, Field(max_length=8)]


class MessageType(Enum):
    confirmation_email = "confirmation_email"
    password_recovery = "password_recovery"


class ConfirmationCodeMessageSchema(BaseModel):
    recipient: str
    recipient_name: str
    message: str
    message_type: str