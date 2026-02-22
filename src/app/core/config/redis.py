from pydantic import RedisDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    """Redis configuration."""

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.sample'),
        env_file_encoding='utf-8',
        env_prefix='REDIS_',
        extra='ignore',
        case_sensitive=False,
    )

    # Required
    scheme: str = 'redis'
    host: str = 'localhost'
    port: int = 6379

    # Optional
    password: SecretStr | None = None
    db: int = 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def url(self) -> RedisDsn:
        """Construct the Redis URL."""
        return RedisDsn.build(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            password=self.password.get_secret_value() if self.password else None,
            path=f'/{self.db}',
        )
