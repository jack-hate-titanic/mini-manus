import logging
from functools import lru_cache
from redis.asyncio import Redis
from core.config import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.settings = get_settings()
        self._client: Redis | None = None

    async def init(self) -> None:
        # 1. 判断客户端是否存在，如果存在表示已经连接上了，不需要重复连接
        if self._client is not None:
            logger.info("Redis client already initialized.")
            return

        try:
            # 2.创建redis客户端并连接
            self._client = Redis(
                host=self.settings.redis_host,
                port=self.settings.redis_port,
                password=self.settings.redis_password,
                db=self.settings.redis_db,
                decode_responses=True,
            )

            # 3.测试连接是否成功
            await self._client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.error(f"Error during Redis client initialization: {e}")
            self._client = None
            raise

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("Redis client connection closed.")

        # 关闭以后清除缓存
        get_redis_client.cache_clear()

    @property
    def client(self):
        if not self._client:
            raise Exception("Redis client is not initialized. Call init() first.")
        return self._client


@lru_cache()
def get_redis_client() -> RedisClient:
    return RedisClient()
