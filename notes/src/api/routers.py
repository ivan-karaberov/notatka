from fastapi import APIRouter

from .note import router as notes_router

router = APIRouter()

router.include_router(notes_router, prefix="/notes", tags=['Notes'])