from fastapi import Depends
from fastapi.security import APIKeyHeader

from utils.auth import get_payload_from_token, get_user_from_payload


def get_current_token_payload(
    token: str = Depends(APIKeyHeader(name="X-API-Key"))
) -> dict:
    """Получает токен и возвращает его payload"""
    return get_payload_from_token(token)


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload)
) -> int | None:
    """Парсит payload полученный из токена"""
    return get_user_from_payload(payload)
