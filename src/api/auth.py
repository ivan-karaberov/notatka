from fastapi import APIRouter, status

from schemas.user import SignUpSchema, SignInSchema
from schemas.auth import TokenPairSchema, RefreshTokenSchema
from services.user import UserService
from repositories.user import UserRepository

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_data: SignUpSchema):
    """Регистрация нового аккаунта"""
    try:
        return await UserService(UserRepository).create_user(signup_data)
    except Exception as e:
        print(f"ERROR > {e}")

@router.post("/signin", response_model=TokenPairSchema)
async def signin(user: SignInSchema):
    """Получение новой пары jwt пользователя"""
    return user


@router.put("/signout")
async def signout():
    """Выход из аккаунта"""
    pass


@router.get("/validate")
async def validate(accessToken: str):
    """Интроспекция токена"""
    pass


@router.post("/refresh")
async def refresh(refreshToken: RefreshTokenSchema):
    """Обновление пары токенов"""
    pass