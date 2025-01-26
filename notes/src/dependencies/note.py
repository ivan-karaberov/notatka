from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.db_helper import db_helper
from services.note import NoteService


DBSessionDependency = Annotated[AsyncSession, Depends(db_helper.get_session_dependency)]


def note_service(session: DBSessionDependency) -> NoteService:
    return NoteService(session=session)


NoteDependency = Annotated[NoteService, Depends(note_service)]
