from pathlib import Path
import sys
import unittest
from unittest.mock import AsyncMock, patch


API_ROOT = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API_ROOT))

from app.infrastructure.storage.redis import RedisClient


class RedisClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_init_uses_settings_and_sets_client(self) -> None:
        fake_client = AsyncMock()
        fake_client.ping = AsyncMock()

        with patch("app.infrastructure.storage.redis.Redis", return_value=fake_client) as redis_cls:
            client = RedisClient()
            await client.init()

        redis_cls.assert_called_once_with(
            host=client.settings.redis_host,
            port=client.settings.redis_port,
            password=client.settings.redis_password,
            db=client.settings.redis_db,
            decode_responses=True,
        )
        fake_client.ping.assert_awaited_once()
        self.assertIs(client.client, fake_client)


if __name__ == "__main__":
    unittest.main()
