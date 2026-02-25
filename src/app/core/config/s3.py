from pydantic import BaseModel, HttpUrl, SecretStr


class S3Config(BaseModel):
    endpoint_url: HttpUrl
    access_key_id: str
    secret_key: SecretStr
    bucket_name: str

    presigned_url_expiry: int = 3600
    max_file_size_bytes: int = 500 * 1024 * 1024  # 500 MB
    # part_size_bytes should be at least 5 MB
    # max_part_number should be at most 10000
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
    part_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    max_part_number: int = 10000
    allowed_content_types: list[str] = [
        'image/jpeg',
        'image/png',
        'image/webp',
        'video/mp4',
        'video/quicktime',
        'video/x-msvideo',
    ]
