from datetime import datetime, timedelta

import jwt
import bcrypt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from core.config import settings
from core.redis.redis_helper import jwt_black_list
from schemas.auth import PayloadSchema, TokenPairSchema
from errors.api_errors import TokenExpiredException, InvalidTokenException


def encode_jwt(
    payload: dict,
    private_key = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algoritm: str = settings.auth_jwt.algorithm
): 
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=algoritm
    )


def hash_password(password: str, rounds: int = 12) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds))


def validate_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )


def generate_auth_token_pair(payload: PayloadSchema):
    payload_dict = payload.model_dump()

    access_token=encode_jwt(payload_dict)
    refresh_token=encode_jwt(
        payload=payload_dict,
        expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
    )

    return TokenPairSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

def get_payload_from_token(token: str) -> dict:
    """Извлекает payload из токена"""
    try:
        return decode_jwt(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise InvalidTokenException


def get_user_from_payload(payload: dict) -> PayloadSchema:
    sub = payload.get("sub")
    role = payload.get("role")
    session_uuid = payload.get("session_uuid")

    if (sub is None) or (role is None) or (session_uuid is None):
        raise InvalidTokenException


    if jwt_black_list.get(session_uuid):
        raise InvalidTokenException

    return PayloadSchema(
        sub=sub,
        role=role,
        session_uuid=session_uuid
    )