import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

class RedisClient:
    _pool = None

    @classmethod
    def get_client(cls):
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True,
                password=REDIS_PASSWORD
            )
        return redis.Redis(connection_pool=cls._pool) 