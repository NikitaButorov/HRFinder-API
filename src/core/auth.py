from typing import Optional, Any
from fastapi import Depends, Request, HTTPException
from fastapi_users import FastAPIUsers, schemas, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from beanie import PydanticObjectId
from bson import ObjectId

from src.models.domain.users import User, UserRole, UserCreate
from src.core.config import get_settings

settings = get_settings()

class UserManager(BaseUserManager[User, ObjectId]):
    reset_password_token_secret = settings.AUTH_SECRET
    verification_token_secret = settings.AUTH_SECRET
    user_db_model = User

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None
    ) -> User:
        """Create a user in database."""
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role"] = UserRole.USER

        created_user = await self.user_db.create(user_dict)
        return created_user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    def parse_id(self, value: str) -> ObjectId:
        """Преобразует строковый ID в ObjectId"""
        try:
            return ObjectId(value)
        except Exception as e:
            raise ValueError("Invalid ID format") from e

    async def get(self, id: Any) -> Optional[User]:
        """Получает пользователя по ID"""
        try:
            if isinstance(id, str):
                id = self.parse_id(id)
            user = await self.user_db.get(id)
            if user:
                # Преобразуем ID в строку при возврате
                user.id = str(user.id)
            return user
        except ValueError:
            return None

    async def create_admin(self, email: str, password: str) -> User:
        """Создает администратора"""
        user_create = UserCreate(
            email=email,
            password=password,
            role=UserRole.ADMIN,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
        
        # Проверяем существование пользователя
        existing_user = await self.user_db.get_by_email(email)
        if existing_user is not None:
            return existing_user
            
        # Создаем нового пользователя
        user = await self.create(user_create)
        return user

class CustomBeanieUserDatabase(BeanieUserDatabase):
    async def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        user = await self.user_model.find_one({"email": email})
        return user

async def get_user_db():
    """Get user database."""
    yield CustomBeanieUserDatabase(User)

async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager."""
    yield UserManager(user_db)

async def create_user_manager():
    async for db in get_user_db():
        return UserManager(db)

bearer_transport = BearerTransport(tokenUrl="/api/v1/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    """Get JWT strategy."""
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, ObjectId](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

def get_user_by_role(*roles: UserRole):
    async def get_user(user: User = Depends(current_active_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return user
    return get_user

get_admin_user = get_user_by_role(UserRole.ADMIN)
get_regular_user = get_user_by_role(UserRole.USER, UserRole.ADMIN) 