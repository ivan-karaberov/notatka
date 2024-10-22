import logging

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from services.note import NoteService
from schemas.user import UserPayloadSchema
from errors.api_errors import APIException

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/")
async def add_note(user_payload: UserPayloadSchema, note: NoteCreateSchema):
    try:
        note_id = await NoteService().add_note(user_payload, note)
        return {"note_id": note_id}
    except APIException as e:
        log.info("Note not saved: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        log.error("Note not saved: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note not saved"
        )

    
@router.get("/")
async def get_note_by_id(
    note_id: int, user_payload: UserPayloadSchema
):
    try:
        return await NoteService().get_note_by_id(user_payload, note_id)
    except APIException as e:
        log.info("Note not received: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        log.error("Note not received: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note not received"
        )
    

@router.patch("/")
async def patch_note(
    note_id: int, note_update: NoteUpdateSchema, user_payload: UserPayloadSchema
):
    try:
        return await NoteService().update_note(user_payload, note_id, note_update)
    except APIException as e:
        log.info("Note not updated: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        log.error("Note not updated: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note not updated"
        )


@router.delete("/")
async def delete_note(note_id: int, user_payload: UserPayloadSchema):
    try:
        return await NoteService().delete_note(user_payload, note_id)
    except APIException as e:
        log.info("Note not deleted: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        log.error("Note not deleted: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note not deleted"
        )