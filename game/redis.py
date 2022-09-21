import redis
from game.environment import (
    CHARSET,
    DB,
    DECODE_RESPONSES,
    REDIS_HOST,
    REDIS_LOCAL_PORT,
)


def create_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_LOCAL_PORT,
        db=DB,
        charset=CHARSET,
        decode_responses=DECODE_RESPONSES,
    )


redis_client = create_redis_client()
