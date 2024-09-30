import uuid
from datetime import datetime, timedelta

from schemas.auth import SignInSchema, TokenPairSchema, PayloadSchema, \
                            SessionSchema, RefreshTokenSchema
from services.user import UserService
from services.session import SessionService
from repositories.user import UserRepository
from repositories.session import SessionRepository
from errors.api_errors import UnauthorizedUserException, InvalidRefreshTokenException
from utils.auth import generate_auth_token_pair, get_payload_from_token, \
                        get_user_from_payload, validate_password
from core.config import settings
from core.redis.redis_helper import jwt_black_list

class AuthService:
    def __init__(self):
        self.user_service = UserService(UserRepository)
        self.session_service = SessionService(SessionRepository)

    async def get_auth_token_pair(self, signin_data: SignInSchema) -> TokenPairSchema:
        """Генерирует пару токенов и создает запись об открытии сессии"""
        user = await self.user_service.get_user_by_username(signin_data.username)
        if (not user) or (user.is_active is False):
            raise UnauthorizedUserException

        if not validate_password(signin_data.password, user.hashed_password):
            raise UnauthorizedUserException

        session_uuid = str(uuid.uuid4())

        payload = PayloadSchema(
            sub=user.id,
            role=user.role,
            session_uuid=session_uuid,
            is_refresh=False
        )
        tokens: TokenPairSchema = generate_auth_token_pair(payload)

        session_detail = SessionSchema(
            user_id=user.id,
            refresh_token=tokens.refresh_token,
            expires_at=datetime.utcnow()+timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes),
            session_uuid=session_uuid
        )

        await self.session_service.create_session(session_detail)

        return tokens

    async def signout(self, payload: PayloadSchema):
        """Закрывает сессию и добавляет токен в черный список"""
        jwt_black_list.set(payload.session_uuid, payload.sub, ex=settings.auth_jwt.access_token_expire_minutes*60)
        await self.session_service.deactivate_session(payload.session_uuid)

    async def refresh_token(self, refresh_token: RefreshTokenSchema) -> TokenPairSchema:
        try:
            payload: dict = get_payload_from_token(refresh_token)
            payload_detail: PayloadSchema = get_user_from_payload(payload, True)
            session_detail = await self.session_service.get_session_by_uuid(
                session_uuid=payload_detail.session_uuid
            )
            
            if session_detail.is_deactivated:
                raise InvalidRefreshTokenException
            
            if session_detail.refresh_token == refresh_token:
                tokens: TokenPairSchema = generate_auth_token_pair(payload_detail)
                await self.session_service.update_refresh_token(
                    session_id=session_detail.id,
                    refresh_token = tokens.refresh_token,
                    expires_at=datetime.utcnow()+timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
                )
                return tokens
            
            raise InvalidRefreshTokenException
        except Exception as e:
            raise InvalidRefreshTokenException

    def validate_token(self, token: str) -> PayloadSchema:
        payload: dict = get_payload_from_token(token)
        return get_user_from_payload(payload)