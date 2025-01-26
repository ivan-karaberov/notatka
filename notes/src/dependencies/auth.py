import json
import requests
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from schemas.user import UserPayloadSchema
from errors.api_errors import InvalidTokenException, TokenExpiredException, ReceivingTokenException


def get_current_token_payload(
    token: str = Depends(APIKeyHeader(name="X-API-Key"))
) -> UserPayloadSchema | None:
    """Получает токен и возвращает его payload"""
    try:
        payload = requests.get("http://localhost:8001/api/authentication/validate", params={"accessToken": token})
    except Exception as e:
        raise ReceivingTokenException
    
    match payload.status_code:
        case 200: return UserPayloadSchema(**json.loads(payload.content))
        case 401: raise InvalidTokenException
        case 403: raise TokenExpiredException

    raise ReceivingTokenException

PayloadDependency = Annotated[UserPayloadSchema, Depends(get_current_token_payload)]