from fastapi import APIRouter, Depends
from models.domain.users import UserRead, UserCreate, UserUpdate
from core.auth import auth_backend, fastapi_users, get_user_manager

router = APIRouter(prefix="/auth", tags=["auth"])

# Создаем роутер только с нужными эндпоинтами
auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
users_router = fastapi_users.get_users_router(
    UserRead,
    UserUpdate,
)

router.include_router(
    auth_router,
    prefix="/jwt"
)

router.include_router(
    register_router,
)

# Добавляем только /me эндпоинты
router.include_router(
    users_router,
    prefix="/users",
    include_in_schema=False,  # Скрываем остальные эндпоинты из документации
)

# Явно добавляем только нужные эндпоинты
router.add_api_route(
    "/users/me",
    users_router.routes[0].endpoint,  # GET /me
    methods=["GET"],
    response_model=UserRead,
)

router.add_api_route(
    "/users/me",
    users_router.routes[1].endpoint,  # PATCH /me
    methods=["PATCH"],
    response_model=UserRead,
) 