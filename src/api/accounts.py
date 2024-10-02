from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Query
from fastapi.exceptions import HTTPException

from schemas.auth import PayloadSchema
from dependencies.auth import get_current_auth_user
from errors.api_errors import APIException
from services.user import UserService
from services.auth import AuthService
from repositories.user import UserRepository
from schemas.account import AccountDetailSchema, UpdateAccountSchema, \
                        UpdatePasswordSchema, AllAccountsSchema

router = APIRouter()


@router.get("/me", response_model=AccountDetailSchema)
async def get_me(payload: PayloadSchema = Depends(get_current_auth_user)):
    """Получение данных о текущем аккаунте"""
    try:
        return await UserService(UserRepository).get_formatted_user_by_id(payload.sub)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed attempt to retrieve data"
        )


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_account(
    update_data: UpdateAccountSchema,
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Обновление своего аккаунта"""
    try:
        await UserService(UserRepository).update_user(payload.sub, update_data)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed update account"
        )


@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    update_password_data: UpdatePasswordSchema,
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Обновление пароля аккаунта"""
    try:
        await UserService(UserRepository).update_password(
            id=payload.sub,
            update_data=update_password_data
        )
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed update password"
        )


@router.get("/accounts", response_model=AllAccountsSchema)
async def get_all_accounts(
    page: Annotated[int, Query(ge=1)],
    page_size: Annotated[int, Query(ge=1, le=100)],
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Получение всех аккаунтов"""
    try:
        return await UserService(UserRepository).get_all_accounts(
            page=page,
            page_size=page_size,
            role=payload.role
        )
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get accounts"
        )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_account(
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Мягкое удаление аккаунта"""
    try:
        await AuthService().soft_delete_account(payload)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed delete account"
        )