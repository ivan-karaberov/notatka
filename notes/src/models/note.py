from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Note(Base):
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=True)
