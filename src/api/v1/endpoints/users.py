from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from bson import ObjectId

from src.models.domain.users import User, UserRole, UserRead
from src.core.auth import get_admin_user, get_user_manager
from src.core.database import Database

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UpdateRoleRequest(BaseModel):
    new_role: UserRole

@router.put("/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: str,
    role_update: UpdateRoleRequest,
    current_user: User = Depends(get_admin_user),
    user_manager = Depends(get_user_manager)
):
    """
    Изменить роль пользователя (только для администраторов)
    """
    # Получаем пользователя по ID
    user = await user_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Запрещаем менять роль самому себе
    if str(user.id) == str(current_user.id):
        raise HTTPException(
            status_code=400,
            detail="Cannot change your own role"
        )

    # Обновляем роль пользователя через MongoDB напрямую
    db = await Database.get_db()
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": role_update.new_role}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Failed to update user role"
        )
    
    # Получаем обновленного пользователя
    updated_user = await user_manager.get(user_id)
    return updated_user

@router.get("/", response_model=List[UserRead])
async def list_users(
    current_user: User = Depends(get_admin_user),
    user_manager = Depends(get_user_manager)
):
    """
    Получить список всех пользователей (только для администраторов)
    """
    db = await Database.get_db()
    users_collection = db["users"]
    
    users = []
    async for user_data in users_collection.find():
        # Преобразуем _id в id для правильной сериализации
        user_data["id"] = str(user_data.pop("_id"))
        users.append(UserRead(**user_data))
    
    return users 