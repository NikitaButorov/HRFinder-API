from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import get_settings
from typing import Optional

settings = get_settings()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def connect_to_database(cls):
        """Connect to MongoDB database."""
        if not cls.client:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            print("Connected to MongoDB.")

    @classmethod
    def close_database_connection(cls):
        """Закрытие соединения с базой данных"""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            print("MongoDB connection closed.")

    @classmethod
    async def get_db(cls) -> AsyncIOMotorDatabase:
        """Получить объект базы данных"""
        if cls.db is None:
            cls.connect_to_database()
        return cls.db