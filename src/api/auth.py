from fastapi import APIRouter, status, HTTPException

from schemas.auth import SignUpSchema, SignInSchema, TokenPairSchema, \
                            RefreshTokenSchema
from services.user import UserService
from services.auth import AuthService
from repositories.user import UserRepository
from errors.api_errors import APIException

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_data: SignUpSchema):
    """Регистрация нового аккаунта"""
    try:
        return await UserService(UserRepository).create_user(signup_data)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed signup"
        )


@router.post("/signin", response_model=TokenPairSchema)
async def signin(signin_data: SignInSchema):
    """Получение новой пары jwt пользователя"""
    try:
        return await AuthService().get_auth_token_pair(signin_data)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed signin"
            )


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