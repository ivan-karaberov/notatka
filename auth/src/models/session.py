from sqlalchemy import Integer, String, ForeignKey, DateTime, TIMESTAMP, func, \
                Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Session(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    session_uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now()
    )
    is_deactivated: Mapped[bool] = mapped_column(Boolean, default=False, server_default="False")
    expires_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    # Опционально: связь с моделью User
    user = relationship("User", back_populates="sessions")