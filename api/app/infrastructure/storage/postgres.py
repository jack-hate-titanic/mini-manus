import logging
from functools import lru_cache

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession
from core.config import get_settings

logger = logging.getLogger(__name__)


class PostgresClient:
    def __init__(self):
        # 1. 初始化数据库连接
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None
        self.settings = get_settings()

    async def init(self) -> None:
        # 2. 初始化postgresql数据库连接
        if self._engine is not None:
            logger.info("PostgreSQL client already initialized.")
            return
        try:
            self._engine = create_async_engine(self.settings.sql_alchemy_database_uri, echo=False)
            self._session_factory = async_sessionmaker(autoflush=False, bind=self._engine)
            async with self._engine.begin() as conn:
                # 检查是否安装了uuid，如果没有安装则安装
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
                logger.info("Connected to PostgreSQL successfully.")
        except Exception as e:
            logger.error(f"Error during PostgreSQL client initialization: {e}")
            self._engine = None
            self._session_factory = None
            raise

    async def close(self) -> None:
        # 3. 关闭数据库连接
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("PostgreSQL client connection closed.")

        get_postgres_client.cache_clear()

    @property
    def session_factory(self):
        if not self._session_factory:
            raise Exception("PostgreSQL client is not initialized. Call init() first.")
        return self._session_factory


@lru_cache()
def get_postgres_client() -> PostgresClient:
    return PostgresClient()

async def get_db_session() -> AsyncSession:
    db = get_postgres_client()
    session_factory = db.session_factory
    async with session_factory() as session:
        try:
            yield session
            await session.commit()  
        except Exception as _:
            await session.rollback()
            raise 
