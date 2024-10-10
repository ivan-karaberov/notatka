from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .user import User


class UserEmail(Base):
    __tablename__ = "user_emails"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), \
                                                unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship("Users", back_populates="email")