from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, Boolean, String, LargeBinary, DateTime, \
                        TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .session import Session
    from .user_emails import UserEmail

class User(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    firstName: Mapped[str] = mapped_column(String(50), nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='True')
    role: Mapped[str] = mapped_column(String(8), nullable=False)
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")
    email: Mapped["UserEmail"] = relationship("UserEmail", back_populates="user", uselist=False)