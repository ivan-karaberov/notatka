from fastapi import APIRouter

from schemas.user import SingUpSchema

router = APIRouter()


@router.post("/signup")
async def signup(user: SingUpSchema):
    pass