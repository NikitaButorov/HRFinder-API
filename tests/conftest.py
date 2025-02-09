from typing import AsyncGenerator
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.main import app, create_admin_if_not_exists
from src.core.database import Database
from src.core.config import Settings
from src.models.domain.users import User
import os
from urllib.parse import urlencode

# Получаем настройки для тестов
test_settings = Settings(
    MONGODB_URL=os.getenv("MONGODB_URL", "mongodb://mongodb:27017"),
    MONGODB_DB_NAME=os.getenv("MONGODB_DB_NAME", "hrfinder_test"),
    TESTING=True,
    SECRET_KEY=os.getenv("SECRET_KEY", "test-secret-key"),
    AUTH_SECRET=os.getenv("AUTH_SECRET", "test-auth-secret")
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db(event_loop):
    """Initialize database connection"""
    asyncio.set_event_loop(event_loop)
    client = AsyncIOMotorClient(test_settings.MONGODB_URL)
    db = client[test_settings.MONGODB_DB_NAME]
    
    try:
        await db.command("dropDatabase")
    except Exception as e:
        print(f"Error dropping database: {e}")
    
    await init_beanie(
        database=db,
        document_models=[User]
    )
    
    Database.client = client
    Database.db = db
    
    # Создаем админа используя функцию из main.py
    await create_admin_if_not_exists()
    
    yield db
    
    try:
        await db.command("dropDatabase")
    except Exception as e:
        print(f"Error dropping database: {e}")
    client.close()

@pytest.fixture(scope="session")
async def client(db) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client"""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        follow_redirects=True
    ) as ac:
        yield ac

@pytest.fixture(scope="session")
async def admin_token(client: AsyncClient) -> str:
    """Get admin authentication token"""
    form_data = urlencode({
        "username": "admin@example.com",
        "password": "admin"
    })
    
    response = await client.post(
        "/api/v1/auth/jwt/login",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        content=form_data
    )
    
    print(f"Admin login response status: {response.status_code}")
    print(f"Admin login response body: {response.text}")
    
    assert response.status_code == 200
    return response.json()["access_token"]