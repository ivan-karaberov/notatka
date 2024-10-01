from datetime import datetime, timedelta

import jwt
import bcrypt

from core.config import settings
from core.redis.redis_helper import jwt_black_list
from schemas.auth import PayloadSchema, TokenPairSchema


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
    payload.is_refresh = False
    access_token=encode_jwt(payload.model_dump())
    
    payload.is_refresh = True
    refresh_token=encode_jwt(
        payload=payload.model_dump(),
        expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
    )

    return TokenPairSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
