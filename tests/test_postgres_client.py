from pathlib import Path
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


API_ROOT = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API_ROOT))

from app.infrastructure.storage.postgres import PostgresClient


class PostgresClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_init_uses_project_settings_and_builds_session_factory(self) -> None:
        fake_conn = AsyncMock()
        fake_begin_ctx = AsyncMock()
        fake_begin_ctx.__aenter__.return_value = fake_conn
        fake_begin_ctx.__aexit__.return_value = None

        fake_engine = MagicMock()
        fake_engine.begin.return_value = fake_begin_ctx

        fake_session_factory = MagicMock()

        with patch("app.infrastructure.storage.postgres.create_async_engine", return_value=fake_engine) as create_engine:
            with patch("app.infrastructure.storage.postgres.async_sessionmaker", return_value=fake_session_factory) as sessionmaker_cls:
                client = PostgresClient()
                await client.init()

        create_engine.assert_called_once_with(client.settings.sql_alchemy_database_uri, echo=False)
        sessionmaker_cls.assert_called_once_with(autoflush=False, bind=fake_engine)
        fake_conn.execute.assert_awaited_once()
        self.assertIs(client.session_factory, fake_session_factory)


if __name__ == "__main__":
    unittest.main()
