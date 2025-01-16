from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://admin:admin@hrfinder.rt8ed.mongodb.net/HRFinder"
    MONGODB_DB_NAME: str = "HRFinder"

@lru_cache()
def get_settings():
    return Settings() 