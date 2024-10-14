import uuid
from datetime import datetime, timedelta

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from schemas.auth import SignInSchema, TokenPairSchema, PayloadSchema, \
                            SessionSchema, RefreshTokenSchema
from services.user import UserService
from services.session import SessionService
from repositories.user import UserRepository
from repositories.session import SessionRepository
from errors.api_errors import UnauthorizedUserException, \
    InvalidRefreshTokenException, InvalidTokenException, TokenExpiredException
from utils.auth import generate_auth_token_pair, validate_password
from core.config import settings
from core.redis.redis_helper import jwt_black_list
from utils.auth import decode_jwt

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
        """Генерирует новую пару jwt токенов"""
        try:
            payload: dict = self.get_payload_from_token(refresh_token)
            payload_detail: PayloadSchema = await self.get_user_from_payload(payload, True)
            session_detail = await self.session_service.get_session_by_uuid(
                session_uuid=payload_detail.session_uuid
            )
            
            if session_detail.is_deactivated or session_detail.refresh_token != refresh_token:
                raise InvalidRefreshTokenException
            

            tokens: TokenPairSchema = generate_auth_token_pair(payload_detail)
            await self.session_service.update_refresh_token(
                session_id=session_detail.id,
                refresh_token = tokens.refresh_token,
                expires_at=datetime.utcnow()+timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
            )
            return tokens
        except Exception as e:
            raise InvalidRefreshTokenException

    async def validate_token(self, token: str) -> PayloadSchema:
        """Валидация токена"""
        payload: dict = self.get_payload_from_token(token)
        return await self.get_user_from_payload(payload)

    async def soft_delete_account(self, payload: PayloadSchema):
        sessions = await self.session_service.get_all_active_sessions(payload.sub)
        
        sessions_id = [session.id for session in sessions]

        print(sessions_id, payload.sub)

        await self.session_service.deactivate_sessions(sessions_id)
        await self.user_service.deactivate_account(payload.sub)


    def get_payload_from_token(self, token: str) -> dict:
        """Извлекает payload из токена"""
        try:
            return decode_jwt(token=token)
        except ExpiredSignatureError:
            raise TokenExpiredException
        except InvalidTokenError:
            raise InvalidTokenException


    async def get_user_from_payload(self, payload: dict, refresh=False) -> PayloadSchema:
        """Извлекает полезную нагрузку из payload"""
        sub = payload.get("sub")
        role = payload.get("role")
        session_uuid = payload.get("session_uuid")
        is_refresh = payload.get("is_refresh")

        if not all([sub, role, session_uuid]) or is_refresh is None:
            raise InvalidTokenException

        user = await self.user_service.get_user_by_id(sub)

        if jwt_black_list.get(session_uuid) or (not user.is_active):
            raise InvalidTokenException

        # Если мы ожидали accessToken а нам передали refreshToken
        if (not refresh) and is_refresh:
            raise InvalidTokenException

        return PayloadSchema(
            sub=sub,
            role=role,
            session_uuid=session_uuid,
            is_refresh=is_refresh
        )
