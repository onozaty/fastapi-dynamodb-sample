import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # DynamoDB settings
    dynamodb_endpoint_url: str | None = None
    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
