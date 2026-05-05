from pathlib import Path
import sys
import unittest
from unittest.mock import patch


API_ROOT = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API_ROOT))

from app.infrastructure.storage.cos import COSClient


class CosClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_init_skips_when_configuration_is_incomplete(self) -> None:
        client = COSClient()
        client.settings.cos_secret_id = None
        client.settings.cos_secret_key = None
        client.settings.cos_region = None
        client.settings.cos_bucket = None

        with patch("app.infrastructure.storage.cos.CosS3Client") as cos_client_cls:
            await client.init()

        cos_client_cls.assert_not_called()
        self.assertFalse(client.is_configured)


if __name__ == "__main__":
    unittest.main()
