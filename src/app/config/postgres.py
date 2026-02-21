from pydantic import Field, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """PostgreSQL database configuration."""

    model_config = SettingsConfigDict(
        env_file=('.env.example', '.env'),
        env_file_encoding='utf-8',
        env_prefix='POSTGRES_',
        extra='ignore',
        case_sensitive=False,
    )

    # Required
    scheme: str = 'postgresql+asyncpg'
    host: str = Field(default=...)
    port: int = 5432
    user: str = Field(default=...)
    password: SecretStr = Field(default=...)
    database: str = Field(default=...)

    # Optional
    pool_size: int = 5
    pool_max_overflow: int = 10
    echo: bool = False

    @property
    @computed_field
    def url(self) -> PostgresDsn:
        """Construct the database URL."""
        return PostgresDsn.build(
            scheme=self.scheme,
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.database,
        )
