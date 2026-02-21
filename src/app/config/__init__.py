from functools import cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .celery import CeleryConfig
from .postgres import PostgresConfig
from .redis import RedisConfig


class Settings(BaseSettings):
    """Main application settings module."""

    model_config = SettingsConfigDict(
        env_file=('.env.example', '.env'),
        env_file_encoding='utf-8',
        env_prefix='APP_',
        case_sensitive=False,
        extra='ignore',
    )

    # Application settings
    debug: bool = False
    environment: str = 'development'

    # Nested settings
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig())
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig())
    celery: CeleryConfig = Field(default_factory=lambda: CeleryConfig())

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


settings = get_app_settings()
