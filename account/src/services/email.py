from models.user_emails import UserEmail
from utils.repository import AbstractRepository
from errors.api_errors import EmailNotFoundException


class EmailService:
    def __init__(self, email_repo: AbstractRepository) -> None:
        self.email_repo = email_repo()

    async def get_by_user_id(self, user_id: int):
        """Получает запись по user_id"""
        return await self.email_repo.fetch_one(user_id=user_id)

    async def get_by_email(self, email: str):
        """Получает запись по email"""
        return await self.email_repo.fetch_one(email=email)

    async def add_email(self, user_id: int, email: str) -> int:
        """Добавляет почту для пользователя в таблицу"""
        user_email = UserEmail(
            user_id = user_id,
            email = email
        )
        return await self.email_repo.add_one(user_email)

    async def confirm_email(self, email: str):
        """Обновляет статус почты в таблице"""
        email = await self.get_by_email(email)
        await self.email_repo.update(
            id=email.id,
            is_confirmed=True
        )

    async def delete_email(self, user_id: int):
        """Удаляет email пользователя"""
        email = await self.email_repo.fetch_one(user_id=user_id)

        if not email:
            raise EmailNotFoundException

        await self.email_repo.delete(email)
