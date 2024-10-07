from models.user import User
from schemas.auth import SignUpSchema
from schemas.account import *
from errors.api_errors import UserAlreadyExistsException, \
                    UnauthorizedUserException, UsernameAlreadyExistsException
from utils.auth import hash_password, validate_password
from utils.repository import AbstractRepository


class UserService:
    def __init__(self, user_repo: AbstractRepository) -> None:
        self.user_repo = user_repo()

    async def create_user(
        self, signup_data: SignUpSchema, role_name: str = "User"
    ) -> int:
        """Создает пользователя в бд"""
        if existing_user := await self.get_user_by_username(signup_data.username):
            raise UserAlreadyExistsException

        user = User(
            firstName=signup_data.firstName,
            lastName=signup_data.lastName,
            username=signup_data.username,
            hashed_password=hash_password(signup_data.password),
            role=role_name
        )

        return await self.user_repo.add_one(user)

    async def admin_create_account(
        self, user: AdminCreateAccountSchema, user_role: str
    ):
        """Создает пользователя в бд с заданной ролью"""
        if user_role != "Admin":
            raise UnauthorizedUserException

        signup_data = SignUpSchema(**user.__dict__)
        await self.create_user(signup_data, role_name=user.role)

    async def update_user(self, id: int, update_data: UpdateAccountSchema):
        """Обновляет пользователя в бд"""
        await self.user_repo.update(
            id=id,
            firstName=update_data.firstName,
            lastName=update_data.lastName
        )

    async def update_username(self, id: int, update_username: str):
        """Обновляет username пользователя в бд"""
        user = await self.get_user_by_username(update_username)
        if user:
            raise UsernameAlreadyExistsException
        
        await self.user_repo.update(
            id=id,
            username=update_username
        )

    async def update_password(self, id: int, update_data: UpdatePasswordSchema):
        """Обновляет пароль пользователя в бд"""
        user = await self.get_user_by_id(id)
        if not validate_password(
            password=update_data.old_password,
            hashed_password=user.hashed_password
        ):
            raise UnauthorizedUserException

        await self.user_repo.update(
            id=id,
            hashed_password=hash_password(update_data.new_password)
        )

    async def get_user_by_username(self, username: str):
        """Получает пользователя из бд"""
        return await self.user_repo.fetch_one(username=username)

    async def get_user_by_id(self, id: int):
        """Получает пользователя по id"""
        return  await self.user_repo.fetch_one(id=id)

    async def get_formatted_user_by_id(self, id: int) -> AccountDetailSchema | None:
        """Получает пользователя в преобразованом формате"""
        if user := await self.get_user_by_id(id=id):
            return AccountDetailSchema(**user.__dict__)

    async def get_all_accounts(
        self,
        page: int,
        page_size: int,
        role: str
    ) -> list[AccountDetailSchema]:
        """Получает все зарегестрированные аккаунты"""
        if role != "Admin":
            raise UnauthorizedUserException
    
        total_pages, accounts = await self.user_repo.fetch_paginated(
            page=page,
            page_size=page_size,
        )
        return AllAccountsSchema(
            accounts=[AccountDetailSchema(**account.__dict__) for account in accounts],
            total_pages=total_pages
        )

    async def deactivate_account(self, id: int):
        """Деактивация аккаунта"""
        await self.user_repo.update(id=id, is_active=False)
        