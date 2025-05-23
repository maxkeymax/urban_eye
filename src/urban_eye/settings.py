from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    MINIO_AWS_ACCESS_KEY_ID: str = 'minioadmin'
    MINIO_SECRET_ACCESS_KEY: str = 'minioadmin'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Экземпляр настроек
settings = Settings()