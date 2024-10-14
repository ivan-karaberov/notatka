import aioredis

from core.config import settings


class RedisHelper:
    def __init__(self, host: str, port: int):
        self.jwt_tokens = aioredis.from_url(
            f"redis://{host}:{port}/0"
        )
        self.confirmation_codes = aioredis.from_url(
            f"redis://{host}:{port}/1"
        )

    async def add_token_to_black_list(self, key: str, val: str, expiration: int
    ):
        await self.jwt_tokens.set(f"black_list:{key}", val, ex=expiration)

    async def get_token_from_black_list(self, key: str):
        return await self.jwt_tokens.get(f"black_list:{key}")

    async def add_email_confirmation_code(
        self, key: str, category: str, val: str, expiration: int
    ):
        await self.confirmation_codes.set(f"{category}:{key}", val, ex=expiration)

    async def get_email_confirmation_code(self, key: str, category: str):
        return await self.confirmation_codes.get(f"{category}:{key}")

    async def delete_email_confirmation_code(self, key: str, category: str):
        await self.confirmation_codes.delete(f"{category}:{key}")


redis_helper = RedisHelper(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT
)