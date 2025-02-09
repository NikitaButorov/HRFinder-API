import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_profile_unauthorized(client: AsyncClient):
    """Тест получения профиля без авторизации"""
    response = await client.get("/api/v1/profiles")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_profile(client: AsyncClient, admin_token: str):
    """Тест получения профиля с авторизацией"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get("/api/v1/profiles", headers=headers)
    assert response.status_code in [200, 404]  # 404 если профиль не найден

@pytest.mark.asyncio
async def test_search_profiles_by_country_skills(client: AsyncClient, admin_token: str):
    """Тест поиска профилей по стране и навыкам"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get(
        "/api/v1/profiles/search/by-country-skills",
        headers=headers,
        params={
            "country": "Russia",
            "skills": ["Python", "FastAPI"],
            "page": 1,
            "size": 10
        }
    )
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data

@pytest.mark.asyncio
async def test_advanced_search(client: AsyncClient, admin_token: str):
    """Тест расширенного поиска профилей"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get(
        "/api/v1/profiles/search/advanced",
        headers=headers,
        params={
            "countries": ["Russia", "USA"],
            "skills": ["Python"],
            "experience_min": 2,
            "experience_max": 10,
            "page": 1,
            "size": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data 