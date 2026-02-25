from pydantic import BaseModel, PostgresDsn, SecretStr, computed_field


class PostgresConfig(BaseModel):
    """PostgreSQL database configuration."""

    # Required
    scheme: str = 'postgresql+asyncpg'
    host: str
    port: int = 5432
    user: str
    password: SecretStr
    database: str

    # Optional
    pool_size: int = 5
    pool_max_overflow: int = 10
    echo: bool = False

    @computed_field
    @property
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
