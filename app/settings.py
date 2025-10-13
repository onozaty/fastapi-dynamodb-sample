import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数から読み込まれるアプリケーション設定。"""

    # ログ設定
    log_format: str = "json"  # "json" or "text"

    # DynamoDB設定
    dynamodb_endpoint_url: str | None = None
    dynamodb_aws_access_key_id: str | None = None
    dynamodb_aws_secret_access_key: str | None = None
    dynamodb_region: str | None = None
    dynamodb_items_table_name: str = "items"

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
