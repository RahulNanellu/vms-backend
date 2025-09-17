# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Core ---
    POSTGRES_USER: str = "vms"
    POSTGRES_PASSWORD: str  # no default
    POSTGRES_DB: str = "vmsdb"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://redis:6379/0"

    # --- MinIO (S3-compatible) ---
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str  # no default
    S3_SECRET_KEY: str  # no default
    S3_BUCKET: str = "vms-media"
    S3_REGION: str = "us-east-1"
    S3_USE_SSL: bool = False

    # --- Auth ---
    JWT_SECRET: str  # no default
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MIN: int = 60 * 24

settings = Settings()
