from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    POSTGRES_USER: str = "vms"
    POSTGRES_PASSWORD: str = "vms123"
    POSTGRES_DB: str = "vmsdb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    REDIS_URL: str = "redis://localhost:6379/0"

    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "***REMOVED***"
    S3_SECRET_KEY: str = "***REMOVED***"
    S3_BUCKET: str = "vms-media"
    S3_REGION: str = "us-east-1"
    S3_USE_SSL: bool = False

    JWT_SECRET: str = "***REMOVED***"
    JWT_ALG: str = "HS256"

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
