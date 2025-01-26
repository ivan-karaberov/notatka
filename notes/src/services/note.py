import logging

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.note import *
from schemas.user import UserPayloadSchema
from models.note import Note
from repositories.note import NoteRepository
from errors.api_errors import NoteNotSavedException, NoteNotFoundException, \
    UserNotHavePermissions, NoteNotUpdatedException, NoteNotDeletedException

log = logging.getLogger(__name__)


class NoteService:
    def __init__(self, session: AsyncSession) -> None:
        self.note_repo = NoteRepository(session=session)

    async def add_note(
        self, user_payload: UserPayloadSchema, note: NoteCreateSchema
    ) -> int:
        """Добавляет заметку, для указанного пользователя и возвращает ее id"""
        try:
            obj = Note(
                user_id=user_payload.sub,
                title=note.title,
                body=note.body
            )
            note_id = await self.note_repo.add_one(obj)

            if note_id is None:
                raise NoteNotSavedException

            return note_id
        except Exception as e:
            log.error("Note don't save: %s", e)
            raise NoteNotSavedException

    async def get_note_by_id(
        self, user_payload: UserPayloadSchema, note_id: int
    ) -> NoteSchema:
        """Получает указанную заметку"""
        note = await self.note_repo.fetch_one(id=note_id)

        if note is None:
            raise NoteNotFoundException

        if note.user_id != user_payload.sub:
            raise UserNotHavePermissions

        return note

    async def update_note(
        self, user_payload: UserPayloadSchema, note_id: int, note_update: NotePartialUpdateSchema
    ) -> NoteSchema:
        """Обновляет указанную заметку"""
        note = await self.note_repo.fetch_one(id=note_id)
        if note is None:
            raise NoteNotFoundException
        
        if note.user_id != user_payload.sub:
            raise UserNotHavePermissions        

        try:
            if update_data_dict := note_update.model_dump(exclude_unset=True):
                updated_note = await self.note_repo.update(id=note.id, **update_data_dict)
                if updated_note is None:
                    raise NoteNotUpdatedException
                return updated_note
        except Exception as e:
            log.error("Note note updated: %s", e)
            raise NoteNotUpdatedException

    async def delete_note(
        self, user_payload: UserPayloadSchema, note_id: int
    ) -> bool:
        """Удаляет заметку с указанным note_id"""
        note = await self.note_repo.fetch_one(id=note_id)

        if note is None:
            raise NoteNotFoundException

        if note.user_id != user_payload.sub:
            raise UserNotHavePermissions

        try:
            return await self.note_repo.delete(note)
        except Exception as e:
            log.error("Note not deleted: %s", e)
            raise NoteNotDeletedException
