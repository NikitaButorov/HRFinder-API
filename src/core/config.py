from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://admin:admin@hrfinder.rt8ed.mongodb.net/HRFinder"
    MONGODB_DB_NAME: str = "HRFinder"
    SECRET_KEY: str = secrets.token_urlsafe(32)  # Генерируем безопасный ключ

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 