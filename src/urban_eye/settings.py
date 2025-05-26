from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    MINIO_AWS_ACCESS_KEY_ID: str = "minioadmin"
    MINIO_SECRET_ACCESS_KEY: str = "minioadmin"

    REDIS_HOST: str = "redis"  # Имя сервиса из Docker Compose
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Экземпляр настроек
settings = Settings()
