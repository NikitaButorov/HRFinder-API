from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import profiles
from core.database import Database

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

# Подключаем роутеры
app.include_router(profiles.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    # Инициализация подключения к БД при запуске
    Database.connect_to_database()

@app.on_event("shutdown")
async def shutdown():
    # Закрытие подключения к БД при остановке
    Database.close_database_connection() 