from pydantic import BaseModel, Field, HttpUrl, SecretStr


class S3Config(BaseModel):
    endpoint_url: HttpUrl
    access_key_id: str
    secret_key: SecretStr
    bucket_name: str

    presigned_url_expiry: int = 3600
    max_file_size_bytes: int = 500 * 1024**2  # 500 MB

    # Limits per https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
    part_size_bytes: int = Field(
        default=10 * 1024**2, ge=5 * 1024**2, le=5 * 1024**3
    )
    max_part_number: int = Field(default=10000, ge=1, le=10000)

    allowed_content_types: list[str] = [
        'video/mp4',
    ]
