import logging

from models.user_emails import UserEmail
from utils.repository import AbstractRepository
from errors.api_errors import EmailNotFoundException

log = logging.getLogger(__name__)


class EmailService:
    def __init__(self, email_repo: AbstractRepository) -> None:
        self.email_repo = email_repo()

    async def get_by_user_id(self, user_id: int):
        """Получает запись по user_id"""
        try:
            return await self.email_repo.fetch_one(user_id=user_id)
        except Exception as e:
            log.error("Email not received: %s", e)

    async def get_by_email(self, email: str):
        """Получает запись по email"""
        try:
            return await self.email_repo.fetch_one(email=email)
        except Exception as e:
            log.error("Email not received: %s", e)

    async def add_email(self, user_id: int, email: str) -> int:
        """Добавляет почту для пользователя в таблицу"""
        user_email = UserEmail(
            user_id = user_id,
            email = email
        )
        try:
            return await self.email_repo.add_one(user_email)
        except Exception as e:
            log.error("Email not add: %s", e)

    async def confirm_email(self, email: str):
        """Обновляет статус почты в таблице"""
        email = await self.get_by_email(email)
        try:
            await self.email_repo.update(
                id=email.id,
                is_confirmed=True
            )
        except Exception as e:
            log.error("Email not updated: %s", e)

    async def delete_email(self, user_id: int):
        """Удаляет email пользователя"""
        email = await self.email_repo.fetch_one(user_id=user_id)

        if not email:
            raise EmailNotFoundException

        try:
            await self.email_repo.delete(email)
        except Exception as e:
            log.error("Email not deleted: %s", e)