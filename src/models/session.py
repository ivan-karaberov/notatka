from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Session(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    # Опционально: связь с моделью User
    user = relationship("User", back_populates="sessions")