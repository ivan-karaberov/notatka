from fastapi import APIRouter

from .notes import router as notes_router

router = APIRouter()

router.include_router(notes_router, prefix="/notes", tags=['Notes'])