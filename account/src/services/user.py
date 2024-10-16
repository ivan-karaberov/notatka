import uuid

from models.user import User
from schemas.auth import SignUpSchema
from schemas.account import *
from errors.api_errors import *
from utils.auth import hash_password, validate_password
from utils.repository import AbstractRepository
from core.config import settings
from core.redis.redis_helper import redis_helper
from services.email import EmailService
from repositories.email import UserEmailRepository
from services.notifications import NotificationService


class UserService:
    def __init__(self, user_repo: AbstractRepository) -> None:
        self.user_repo = user_repo()
        self.email_service = EmailService(UserEmailRepository)

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
        update_username = update_username.lower()

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
        return await self.user_repo.fetch_one(username=username.lower())

    async def get_user_by_id(self, id: int):
        """Получает пользователя по id"""
        return  await self.user_repo.fetch_one(id=id)

    async def get_formatted_user_by_id(self, id: int) -> AccountDetailSchema | None:
        """Получает пользователя в преобразованом формате"""
        if user := await self.user_repo.fetch_one_with_relationships(['email'], id=id):
            user_dict = user.__dict__
            if user.email:
                user_dict['email'] = EmailDetailSchema(
                    email=user.email.email,
                    is_confirmed=user.email.is_confirmed
                )
            return AccountDetailSchema(**user_dict)

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
        
    async def add_email(self, user_id: int, email: str):
        """Добавляет email пользователю и отправляет ссылку подтверждения"""
        user_taken = await self.user_repo.fetch_one_with_relationships(['email'], id=user_id)
        email_taken = await self.email_service.get_by_email(email)
        message_type = MessageType.confirmation_email

        if not user_taken.email and not email_taken:
            await self.email_service.add_email(user_id, email)
            await self.__generate_code_and_send_email(user_id, email, message_type)
            return
        
        if user_taken.email:
            redis_taken = await redis_helper.get_email_confirmation_code(
                key=user_taken.email.email,
                category=message_type.value
            )

            if not user_taken.email.is_confirmed and not redis_taken:
                await self.__generate_code_and_send_email(
                    user_id=user_id,
                    email=user_taken.email.email,
                    message_type=message_type
                )
                return
            elif redis_taken:
                raise ConfirmationCodeAlreadySentException

        if user_taken:
            raise UserAlreadyLinkedEmailException

        if email_taken:
            raise EmailAlreadyExistsException

    async def __generate_code_and_send_email(
        self, user_id: int, email: str, message_type: MessageType
    ):
        """Генерирует код подтверждения и отправляет сообщение на почту"""
        token = str(uuid.uuid4())
        await redis_helper.add_email_confirmation_code(
            key=email,
            category=message_type.value,
            val=token,
            expiration=settings.app.confirmation_code_expire_minutes*60
        )
        await self.__send_сonfirmation_email(user_id, email, token, message_type)

    async def __send_сonfirmation_email(
        self, user_id: int, email: str, token: str, message_type: MessageType
    ):
        """Формирует сообщение и отправляет его на почту"""
        user = await self.get_user_by_id(user_id)
        app_url = settings.app.get_url()

        message = ConfirmationCodeMessageSchema(
            recipient=email,
            recipient_name=user.firstName,
            message=f"http://{app_url}/{message_type.value}?email={email}&token={token}",
            message_type=message_type.value
        )

        async with NotificationService() as notification_service:
            await notification_service.send_message(message)

    async def confirmation_email(self, email: str, token: str):
        """Подтверждает email"""
        code = await redis_helper.get_email_confirmation_code(
            key=email,
            category=MessageType.confirmation_email.value
        )
        original_token = code.decode('utf-8')
        
        if original_token == token:
            await self.email_service.confirm_email(email)
            await redis_helper.delete_email_confirmation_code(
                key=email,
                category=MessageType.confirmation_email.value
            )
            return True
        
        raise ConfirmationCodeIncorrectException

    async def forgot_password(self, email: str):
        """Создает заявку на смену пароля"""
        redis_taken = await redis_helper.get_email_confirmation_code(
            key=email,
            category=MessageType.password_recovery.value
        )
        if redis_taken:
            raise ConfirmationCodeAlreadySentException

        email_taken = await self.email_service.get_by_email(email)
        if not email_taken or not email_taken.is_confirmed:
            raise EmailNotFoundException
        
        await self.__generate_code_and_send_email(
            user_id=email_taken.user_id,
            email=email,
            message_type=MessageType.password_recovery
        )
    
    async def reset_password(self, email: str, password: str, token: str):
        """Устанавливает новый пароль"""
        email_taken = await self.email_service.get_by_email(email)
        if not email_taken or not email_taken.is_confirmed:
            raise EmailNotFoundException

        code = await redis_helper.get_email_confirmation_code(
            key=email,
            category=MessageType.password_recovery.value
        )

        original_token = code.decode('utf-8')
        if original_token == token:
            await self.user_repo.update(
                id=email_taken.user_id,
                hashed_password=hash_password(password)
            )
            return True

        raise ConfirmationCodeIncorrectException