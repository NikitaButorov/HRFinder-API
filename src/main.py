from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError
from fastapi_users import FastAPIUsers
from bson import ObjectId

from .api.v1.endpoints import profiles, auth, users
from src.core.database import Database
from src.core.config import get_settings
from src.models.domain.users import User, UserRole, UserRead, UserCreate
from src.core.auth import (
    current_active_user,
    get_user_manager,
    create_user_manager,
    fastapi_users,
    auth_backend
)

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    try:
        if not Database.client:  # Проверяем, не инициализирована ли уже БД (для тестов)
            # Инициализация подключения к БД
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = client[settings.MONGODB_DB_NAME]
            
            Database.client = client
            Database.db = db
            
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
        if not Database.client:  # Только если БД не была инициализирована
            raise e

    yield  # Здесь приложение работает

    # Shutdown
    if Database.client and not settings.TESTING:  # Не закрываем соединение в тестах
        Database.close_database_connection()

# Создаем экземпляр FastAPIUsers
fastapi_users = FastAPIUsers[User, ObjectId](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="HR Finder API",
    description="API для поиска и анализа профилей LinkedIn",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем роутеры аутентификации до других роутеров
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1/auth",
    tags=["auth"]
)

# Затем добавляем остальные роутеры
app.include_router(
    profiles.router,
    prefix="/api/v1",
    dependencies=[Depends(fastapi_users.current_user(active=True))]
)

app.include_router(
    users.router,
    prefix="/api/v1",
) 