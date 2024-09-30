from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class AccountDetailSchema(BaseModel):
    id: int
    lastName: Annotated[str, Field(max_length=50)]
    firstName: Annotated[str, Field(max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    role: Annotated[str, Field(max_length=8)]
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool