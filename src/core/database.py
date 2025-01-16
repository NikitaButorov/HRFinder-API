from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database as MongoDatabase
from typing import Optional
from .config import get_settings

settings = get_settings()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[MongoDatabase] = None

    @classmethod
    def connect_to_database(cls):
        try:
            if not cls.client:
                cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
                cls.db = cls.client[settings.MONGODB_DB_NAME]
                # Проверяем подключение более простым способом
                cls.client.server_info()
                print("Successfully connected to MongoDB Atlas")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    def close_database_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None