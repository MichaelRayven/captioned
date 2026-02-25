from pydantic import AmqpDsn, BaseModel, RedisDsn


class CeleryConfig(BaseModel):
    """Celery configuration."""

    # Time and date
    timezone: str = 'UTC'
    enable_utc: bool = True

    # These will default to Redis URL if not provided
    broker_url: RedisDsn | AmqpDsn | None = None
    result_backend: RedisDsn | AmqpDsn | None = None

    # Task settings
    task_always_eager: bool = False
    task_eager_propagates: bool = False
    task_time_limit: int = 300  # 5 minutes
    task_soft_time_limit: int = 240  # 4 minutes
    task_default_rate_limit: int | None = None
    task_acks_late: bool = True

    # Worker settings
    worker_concurrency: int = 4
    worker_prefetch_multiplier: int = 1

    # Serialization
    task_serializer: str = 'json'
    result_serializer: str = 'json'
    accept_content: list[str] = ['json']

    # Result settings
    result_expires: int = 3600  # 1 hour

    # Optional task routes
    task_routes: dict[str, str] | None = None
