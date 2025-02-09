import pytest
from httpx import AsyncClient
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """Тест входа в систему"""
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
    print(f"Login test response status: {response.status_code}")
    print(f"Login test response body: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data