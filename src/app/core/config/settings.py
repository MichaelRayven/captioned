from functools import cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .celery import CeleryConfig
from .environment import Environment
from .postgres import PostgresConfig
from .redis import RedisConfig
from .s3 import S3Config


class Settings(BaseSettings):
    """Main application settings module."""

    model_config = SettingsConfigDict(
        env_file=('.env.example', '.env'),
        env_file_encoding='utf-8',
        env_nested_delimiter='_',
        env_nested_max_split=1,
        case_sensitive=False,
        extra='ignore',
    )

    # Application settings
    debug: bool = True
    environment: Environment = Environment.local

    # Nested settings
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    celery: CeleryConfig = Field(default_factory=CeleryConfig)
    s3: S3Config = Field(default_factory=S3Config)

    @model_validator(mode='after')
    def set_celery_defaults(self) -> Settings:
        """Configure Celery broker/backend urls to use Redis by default."""
        if self.celery.broker_url is None:
            self.celery.broker_url = self.redis.url

        if self.celery.result_backend is None:
            self.celery.result_backend = self.redis.url

        return self


@cache
def get_app_settings() -> Settings:
    return Settings()
