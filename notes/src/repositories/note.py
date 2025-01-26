from sqlalchemy.ext.asyncio import AsyncSession

from models.note import Note
from repositories.repository import SQLAlchemyRepository

class NoteRepository[T](SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Note)
