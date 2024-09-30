from models.user import User
from schemas.auth import SignUpSchema
from schemas.account import AccountDetailSchema, UpdateAccountSchema
from errors.api_errors import UserAlreadyExistsException
from utils.auth import hash_password
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

    async def update_user(self, id: int, update_data: UpdateAccountSchema):
        await self.user_repo.update(
            id=id,
            firstName=update_data.firstName,
            lastName=update_data.lastName,
            hashed_password=hash_password(update_data.password)
        )

    async def get_user_by_username(self, username: str):
        """Получает пользователя из бд"""
        return await self.user_repo.fetch_one(username=username)

    async def get_user_by_id(self, id: int) -> AccountDetailSchema | None:
        if user := await self.user_repo.fetch_one(id=id):
            account = AccountDetailSchema(
                id=user.id,
                firstName=user.firstName,
                lastName=user.lastName,
                username=user.username,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
                is_active=user.is_active
            )
            return account