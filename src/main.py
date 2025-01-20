from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from api.v1.endpoints import profiles, auth, users
from core.database import Database
from core.config import get_settings
from models.domain.users import User, UserRole
from core.auth import current_active_user, get_user_manager, create_user_manager

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="HR Finder API",
    description="API для поиска и анализа профилей LinkedIn",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def create_admin_if_not_exists():
    """Создает администратора, если он не существует"""
    admin_email = "admin@example.com"
    admin_password = "admin"  # В продакшене используйте безопасный пароль

    try:
        # Создаем менеджер пользователей
        user_manager = await create_user_manager()
        
        # Создаем администратора
        admin = await user_manager.create_admin(admin_email, admin_password)
        print(f"Admin user ready with email: {admin_email}")
        
    except Exception as e:
        print(f"Error with admin user: {str(e)}")

@app.on_event("startup")
async def startup():
    try:
        # Инициализация подключения к БД
        Database.connect_to_database()
        
        # Инициализация Beanie для работы с пользователями
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # Инициализируем все модели
        await init_beanie(
            database=db,
            document_models=[User]
        )

        print("Database initialized successfully")

        # Создаем администратора при запуске
        await create_admin_if_not_exists()
        
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise e

@app.on_event("shutdown")
async def shutdown():
    Database.close_database_connection()

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1")
app.include_router(
    profiles.router,
    prefix="/api/v1",
    dependencies=[Depends(current_active_user)]  # Требуем аутентификацию для всех эндпоинтов profiles
)
app.include_router(
    users.router,
    prefix="/api/v1",
) 