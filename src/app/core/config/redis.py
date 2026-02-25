from pydantic import BaseModel, RedisDsn, SecretStr, computed_field


class RedisConfig(BaseModel):
    """Redis configuration."""

    # Required
    scheme: str = 'redis'
    host: str = 'localhost'
    port: int = 6379

    # Optional
    password: SecretStr | None = None
    db: int = 0

    @computed_field
    @property
    def url(self) -> RedisDsn:
        """Construct the Redis URL."""
        return RedisDsn.build(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            password=self.password.get_secret_value()
            if self.password
            else None,
            path=f'/{self.db}',
        )
