from typing import Optional, Any, Dict
from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser
from pydantic import EmailStr, Field, computed_field, BaseModel, model_validator
from enum import Enum
from beanie import Document
from pymongo import IndexModel, ASCENDING
from bson import ObjectId

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class CustomBaseUser(schemas.BaseUser[str]):
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, data: Any) -> Any:
        """Преобразование ObjectId в строку"""
        if isinstance(data, dict):
            # Преобразуем _id в id если есть
            if "_id" in data:
                data["id"] = str(data.pop("_id"))
            # Преобразуем существующий id если это ObjectId
            elif "id" in data and isinstance(data["id"], ObjectId):
                data["id"] = str(data["id"])
        return data

    class Config:
        json_encoders = {ObjectId: str}

class UserRead(CustomBaseUser):
    role: UserRole
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, User):
            # Преобразуем ObjectId в строку при сериализации
            obj_dict = obj.model_dump()
            obj_dict["id"] = str(obj_dict["id"])
            return super().model_validate(obj_dict, *args, **kwargs)
        return super().model_validate(obj, *args, **kwargs)

    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    role: UserRole = UserRole.USER
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False

class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[UserRole] = None

class User(BeanieBaseUser, Document):
    email: EmailStr = Field(unique=True, index=True)  # Явно определяем email как поле
    role: UserRole = Field(default=UserRole.USER)
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False

    @classmethod
    async def by_email(cls, email: str):
        """Поиск пользователя по email"""
        return await cls.find_one({"email": email})

    def __str__(self) -> str:
        """Строковое представление пользователя"""
        return f"User(id={str(self.id)}, email={self.email})"

    def model_dump(self, *args, **kwargs) -> Dict:
        """Сериализация модели в словарь"""
        d = super().model_dump(*args, **kwargs)
        # Преобразуем ObjectId в строку
        if "id" in d and isinstance(d["id"], ObjectId):
            d["id"] = str(d["id"])
        return d

    @property
    def mongo_id(self) -> str:
        """Возвращает строковое представление ID для API"""
        return str(self.id)

    class Settings:
        name = "users"
        use_state_management = True
        indexes = [
            "email",  # Создаем индекс для email
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "string",
                "role": UserRole.USER,
            }
        }
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        use_enum_values = True 