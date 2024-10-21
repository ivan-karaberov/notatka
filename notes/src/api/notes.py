import logging

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from errors.api_errors import APIException

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/")
async def add_note(user_payload, note):
    try:
        pass    
    except APIException as e:
        log.info("Note don't save: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        log.error("Note don't save: %s", e)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
