from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "hrfinder"
    SECRET_KEY: str = "your-secret-key"  # Используется для JWT
    AUTH_SECRET: str = "your-auth-secret"  # Добавляем auth_secret для fastapi-users
    TESTING: bool = False  # Новый параметр
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings() 