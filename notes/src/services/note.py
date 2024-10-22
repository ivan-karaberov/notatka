import logging

from schemas.note import *
from schemas.user import UserPayloadSchema
from repositories.note import NoteRepository
from errors.api_errors import NoteNotSavedException, NoteNotFoundException, \
    UserNotHavePermissions, NoteNotUpdatedException, NoteNotDeletedException

log = logging.getLogger(__name__)


class NoteService:
    def __init__(self) -> None:
        self.note_repo = NoteRepository()

    async def add_note(
        self, user_payload: UserPayloadSchema, note: NoteCreateSchema
    ) -> int:
        """Добавляет заметку, для указанного пользователя и возвращает ее id"""
        try:
            note_id = await self.note_repo.add_note(
                user_id=user_payload.sub,
                note=note
            )
            return note_id
        except Exception as e:
            log.error("Note don't save: %s", e)
            raise NoteNotSavedException

    async def get_note_by_id(
        self, user_payload: UserPayloadSchema, note_id: int
    ) -> NoteSchema:
        """Получает указанную заметку"""
        note = await self.note_repo.fetch_note_by_id(note_id=note_id)

        if note is None:
            raise NoteNotFoundException

        if note.user_id != user_payload.sub:
            raise UserNotHavePermissions

        return note

    async def update_note(
        self, user_payload: UserPayloadSchema, note_id: int, note_update: NotePartialUpdateSchema
    ) -> NoteSchema:
        """Обновляет указанную заметку"""
        note = await self.note_repo.fetch_note_by_id(note_id=note_id)
        if note is None:
            raise NoteNotFoundException
        
        if note.user_id != user_payload.scheme:
            raise UserNotHavePermissions        

        try:
            await self.note_repo.update_note(note, note_update, partial=True)
        except Exception as e:
            log.error("Note note updated: %s", e)
            raise NoteNotUpdatedException

    async def delete_note(
        self, user_payload: UserPayloadSchema, note_id: int
    ) -> bool:
        """Удаляет заметку с указанным note_id"""
        note = await self.user_repo.fetch_note_by_id(note_id=note_id)

        if note is None:
            raise NoteNotFoundException

        if note.user_id != user_payload.sub:
            raise UserNotHavePermissions

        try:
            return await self.user_payload.delete_note(note=note)
        except Exception as e:
            log.error("Note not deleted: %s", e)
            raise NoteNotDeletedException
