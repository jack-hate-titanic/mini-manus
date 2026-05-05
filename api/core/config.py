'''
Author: 悦者生存 1002783067@qq.com
Date: 2026-05-01 22:02:48
LastEditors: 悦者生存 1002783067@qq.com
LastEditTime: 2026-05-03 19:37:41
FilePath: /mini-manus/api/core/config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import AliasChoices, Field
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    env: str = "development"
    log_level: str = "INFO"
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    cors_allow_credentials: bool = True

    # 数据库配置
    sql_alchemy_database_uri: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/manus",
        validation_alias=AliasChoices("SQL_ALCHEMY_DATABASE_URI", "SQLALCHEMY_DATABASE_URI"),
    )

    # redis配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    # COS腾讯云对象存储配置
    cos_secret_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("COS_SECRET_ID", "TENCENT_CLOUD_SECRET_ID"),
    )
    cos_secret_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("COS_SECRET_KEY", "TENCENT_CLOUD_SECRET_KEY"),
    )
    cos_region: str | None = Field(
        default=None,
        validation_alias=AliasChoices("COS_REGION", "TENCENT_CLOUD_REGION"),
    )
    cos_bucket: str | None = Field(
        default=None,
        validation_alias=AliasChoices("COS_BUCKET", "COS_BUCKET_NAME", "TENCENT_CLOUD_BUCKET_NAME"),
    )
    cos_scheme: str = Field(
        default="https",
        validation_alias=AliasChoices("COS_SCHEME"),
    )

    @property
    def sync_sqlalchemy_database_uri(self) -> str:
        url = make_url(self.sql_alchemy_database_uri)
        if url.drivername == "postgresql+asyncpg":
            url = url.set(drivername="postgresql+psycopg2")
        return url.render_as_string(hide_password=False)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings 
