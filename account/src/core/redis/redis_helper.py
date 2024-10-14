import redis

from core.config import settings

jwt_black_list = redis.Redis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    db=0
)

confirmations_codes = redis.Redis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    db=1
)