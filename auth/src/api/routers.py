from fastapi import APIRouter

from .auth import router as auth_router
from .accounts import router as accounts_router

router = APIRouter()

router.include_router(auth_router, prefix="/authentication", tags=['Authentication'])
router.include_router(accounts_router, prefix="/accounts", tags=['Accounts'])