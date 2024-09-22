from sqlalchemy import Integer, Boolean, String, LargeBinary, DateTime, \
                        TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Role(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)