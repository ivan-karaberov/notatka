from typing import List

from models.user import User
from schemas.auth import SignUpSchema
from errors.api_errors import UserAlreadyExistsException
from utils.auth import hash_password


class UserService:
    def __init__(self, user_repo) -> None:
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

    async def get_user_by_username(self, username: str):
        """Получает пользователя из бд"""
        return await self.user_repo.fetch_one(username=username)
