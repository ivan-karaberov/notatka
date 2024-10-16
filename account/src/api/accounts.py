import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status, Query, Body
from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from schemas.auth import PayloadSchema
from dependencies.auth import get_current_auth_user
from services.user import UserService
from services.auth import AuthService
from services.email import EmailService
from repositories.user import UserRepository
from repositories.email import UserEmailRepository
from schemas.account import *

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/me", response_model=AccountDetailSchema)
async def get_me(payload: PayloadSchema = Depends(get_current_auth_user)):
    """Получение данных о текущем аккаунте"""
    try:
        return await UserService(UserRepository).get_formatted_user_by_id(payload.sub)
    except Exception as e:
        log.error("Failed attempt to retrieve data: %s", e)
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
    except Exception as e:
        log.error("Failed update account: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed update account"
        )


@router.put("/update_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    update_username: str = Body(embed=True),
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Обновление своего ника"""
    try:
        await UserService(UserRepository).update_username(payload.sub, update_username)
    except Exception as e:
        log.error("Failed update username: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed update username"
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
    except Exception as e:
        log.error("Failed update password: %s", e)
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
    except Exception as e:
        log.error("Failed get accounts: %s", e)
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
    except Exception as e:
        log.error("Failed delete account: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed delete account"
        )


@router.post("/new", status_code=status.HTTP_204_NO_CONTENT)
async def admin_create_account(
    user: AdminCreateAccountSchema,
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Создание аккаунта администратором"""
    try:
        await UserService(UserRepository).admin_create_account(user, payload.role)
    except Exception as e:
        log.error("Failed create account: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed create account"
        )


@router.post("/add_email", status_code=status.HTTP_204_NO_CONTENT)
async def add_email(
    email: EmailStr = Body(embed=True),
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Добавление email к аккаунту"""
    try:
        await UserService(UserRepository).add_email(payload.sub, email)
    except Exception as e:
        log.error("Failed add email: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add email"
        )


@router.post(f"/{MessageType.confirmation_email.value}", status_code=status.HTTP_204_NO_CONTENT)
async def confirmation_email(email: EmailStr, token: str):
    """Подтверждение email"""
    try:
        await UserService(UserRepository).confirmation_email(email, token)
    except Exception as e:
        log.error("Failed confirmation email: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed confirmation email"
        )


@router.delete("/email", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email(
    payload: PayloadSchema = Depends(get_current_auth_user)
):
    """Удаляет email пользователя"""
    try:
        await EmailService(UserEmailRepository).delete_email(payload.sub)
    except Exception as e:
        log.error("Failed delete email: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed delete email"
        )


@router.post("/forgot_password", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_reset(
    email: EmailStr
):
    """Создание заявки на восстановление пароля"""
    try:
        await UserService(UserRepository).forgot_password(email)
    except Exception as e:
        log.error("Password reset failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )


@router.post("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(reset_password: ResetPasswordSchema):
    """Обновление пароля"""
    try:
        await UserService(UserRepository).reset_password(
            email=reset_password.email,
            password=reset_password.password,
            token=reset_password.token
        )
    except Exception as e:
        log.error("Password reset failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
