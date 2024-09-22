from sqlalchemy import Integer, Boolean, String, LargeBinary, DateTime, \
                        TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    firstname: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32),unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
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