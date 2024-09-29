from datetime import datetime, timedelta

from schemas.auth import SignInSchema, TokenPairSchema, PayloadSchema, \
                            SessionSchema
from services.user import UserService
from services.session import SessionService
from repositories.user import UserRepository
from repositories.session import SessionRepository
from errors.api_errors import UnauthorizedUserException
from utils.auth import generate_auth_token_pair
from core.config import settings


class AuthService:
    def __init__(self):
        self.user_service = UserService(UserRepository)
        self.session_service = SessionService(SessionRepository)

    async def get_auth_token_pair(self, signin_data: SignInSchema) -> TokenPairSchema:
        user = await self.user_service.get_user_by_username(signin_data.username)
        if (not user) or (user.is_active is False):
            raise UnauthorizedUserException

        payload = PayloadSchema(
            sub=user.id,
            role=user.role
        )
        tokens: TokenPairSchema = generate_auth_token_pair(payload)

        session_detail = SessionSchema(
            user_id=user.id,
            refresh_token=tokens.refresh_token,
            expires_at=datetime.utcnow()+timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
        )
        await self.session_service.create_session(session_detail)

        return tokens
