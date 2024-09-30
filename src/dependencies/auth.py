from fastapi import Depends
from fastapi.security import APIKeyHeader
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from utils.auth import decode_jwt
from errors.api_errors import TokenExpiredException, InvalidTokenException
from schemas.auth import PayloadSchema

def get_current_token_payload(
    token: str = Depends(APIKeyHeader(name="X-API-Key"))
) -> dict:
    """Получает токен и возвращает его payload"""
    try:
        return decode_jwt(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise InvalidTokenException


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload)
) -> int | None:
    """Парсит payload полученный из токена"""
    sub = payload.get("sub")
    role = payload.get("role")
    session_uuid = payload.get("session_uuid")

    if (sub is None) or (role is None) or (session_uuid is None):
        raise InvalidTokenException

    return PayloadSchema(
        sub=sub,
        role=role,
        session_uuid=session_uuid
    )