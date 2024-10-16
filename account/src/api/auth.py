import logging

from fastapi import APIRouter, status, HTTPException, Depends

from schemas.auth import SignUpSchema, SignInSchema, TokenPairSchema, \
                            RefreshTokenSchema, PayloadSchema
from services.user import UserService
from services.auth import AuthService
from repositories.user import UserRepository
from errors.api_errors import APIException
from dependencies.auth import get_current_auth_user

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_data: SignUpSchema):
    """Регистрация нового аккаунта"""
    try:
        user_id = await UserService(UserRepository).create_user(signup_data)
        return {"user_id": user_id}
    except Exception as e:
        log.error("Failed signup: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed signup"
        )


@router.post("/signin", response_model=TokenPairSchema)
async def signin(signin_data: SignInSchema):
    """Получение новой пары jwt пользователя"""
    try:
        return await AuthService().get_auth_token_pair(signin_data)
    except Exception as e:
        log.error("Failed signin: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed signin"
        )


@router.put("/signout", status_code=status.HTTP_204_NO_CONTENT)
async def signout(
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Выход из аккаунта"""
    try:
        await AuthService().signout(payload)
    except Exception as e:
        log.error("Failed signout: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed signout"
            )


@router.get("/validate", response_model=PayloadSchema)
async def validate(accessToken: str):
    """Интроспекция токена"""
    try:
        return await AuthService().validate_token(accessToken)
    except Exception as e:
        log.error("Failed validation: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed validation"
        )



@router.post("/refresh", response_model=TokenPairSchema)
async def refresh(refreshToken: RefreshTokenSchema):
    """Обновление пары токенов"""
    try:
        return await AuthService().refresh_token(refreshToken.refresh_token)
    except Exception as e:
        log.error("Failed refresh: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed refresh"
        )
