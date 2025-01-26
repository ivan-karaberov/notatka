import logging

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from schemas.note import NoteCreateSchema, NotePartialUpdateSchema
from dependencies.note import NoteDependency
from dependencies.auth import PayloadDependency
from errors.api_errors import APIException

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/")
async def add_note(
    user_payload: PayloadDependency,
    note: NoteCreateSchema,
    note_service: NoteDependency
):
    try:
        note_id = await note_service.add_note(user_payload, note)
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
    note_id: int, user_payload: PayloadDependency, note_service: NoteDependency
):
    try:
        return await note_service.get_note_by_id(user_payload, note_id)
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
    note_id: int,
    note_update: NotePartialUpdateSchema,
    user_payload: PayloadDependency,
    note_service: NoteDependency
):
    try:
        return await note_service.update_note(user_payload, note_id, note_update)
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
async def delete_note(
    note_id: int,
    user_payload: PayloadDependency,
    note_service: NoteDependency
):
    try:
        return await note_service.delete_note(user_payload, note_id)
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