import logging
from functools import lru_cache

from core.config import get_settings
from qcloud_cos import CosConfig, CosS3Client


logger = logging.getLogger(__name__)


class COSClient:
    def __init__(self):
        self.settings = get_settings()
        # 1. 初始化COS客户端
        self._client: CosS3Client | None = None

    @property
    def is_configured(self) -> bool:
        return all(
            [
                self.settings.cos_secret_id,
                self.settings.cos_secret_key,
                self.settings.cos_region,
                self.settings.cos_bucket,
            ]
        )

    async def init(self) -> None:
        if self._client is not None:
            logger.info("COS client already initialized.")
            return

        if not self.is_configured:
            logger.info("COS configuration is incomplete. Skipping COS initialization.")
            return

        try:
            # 2. 创建COS客户端并连接
            config = CosConfig(
                Region=self.settings.cos_region,
                SecretId=self.settings.cos_secret_id,
                SecretKey=self.settings.cos_secret_key,
                Scheme=self.settings.cos_scheme,
            )
            self._client = CosS3Client(config)
            logger.info("Connected to COS successfully.")
        except Exception as e:
            logger.error(f"Error during COS client initialization: {e}")
            self._client = None
            raise

    async def close(self) -> None:
        if self._client is not None:
            self._client = None
            logger.info("COS client connection closed.")

        get_cos_client.cache_clear()

    @property
    def client(self):
        if not self._client:
            raise Exception("COS client is not initialized. Call init() first.")
        return self._client


@lru_cache()
def get_cos_client() -> COSClient:
    return COSClient()
