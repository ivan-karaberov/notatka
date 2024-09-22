from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, Boolean, String, LargeBinary, DateTime, \
                        TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user_roles import user_roles
if TYPE_CHECKING:
    from .role import Role

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
    roles: Mapped[List["Role"]] = relationship("Role", secondary=user_roles, back_populates="users")