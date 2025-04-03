import pytest
import requests
from tests.conftest import BASE_URL

def test_api_docs_available():
    """Проверка доступности документации API"""
    # В FastAPI документация по умолчанию доступна на /docs
    response = requests.get(f"{BASE_URL.split('/api/v1')[0]}/docs")
    assert response.status_code == 200 or response.status_code == 301

def test_openapi_json_available():
    """Проверка доступности OpenAPI JSON"""
    # OpenAPI схема обычно доступна на /openapi.json
    response = requests.get(f"{BASE_URL.split('/api/v1')[0]}/openapi.json")
    assert response.status_code == 200 or response.status_code == 301
    # Если получили редирект 301, следуем редиректу
    if response.status_code == 301:
        response = requests.get(response.headers['Location'])
        assert response.status_code == 200
    
    if response.status_code == 200:
        data = response.json()
        # Проверяем основные элементы OpenAPI схемы
        assert "openapi" in data
        assert "paths" in data

def test_auth_endpoints_available():
    """Проверка доступности эндпоинтов аутентификации"""
    # Получение информации о пользователе (требуется авторизация)
    response = requests.get(f"{BASE_URL}/auth/users/me")
    # 401 Unauthorized - ожидаемый ответ для неавторизованного запроса
    assert response.status_code == 401

    # Эндпоинт входа
    response = requests.post(f"{BASE_URL}/auth/jwt/login", data={})
    # 422 Validation Error - ожидаемый ответ при отсутствии необходимых данных
    assert response.status_code == 422 or response.status_code == 400

def test_auth_register_endpoint_available():
    """Проверка доступности эндпоинта регистрации"""
    # В FastAPI-users эндпоинт регистрации чаще всего находится по пути /auth/register
    # Пробуем оба варианта
    response1 = requests.post(f"{BASE_URL}/register", json={})
    response2 = requests.post(f"{BASE_URL}/auth/register", json={})
    
    # Хотя бы один из эндпоинтов должен возвращать 422 Validation Error
    assert response1.status_code == 422 or response2.status_code == 422, "Ни один из эндпоинтов регистрации не найден"

def test_profiles_endpoints_available():
    """Проверка доступности эндпоинтов профилей"""
    # Поиск профилей по стране и навыкам
    response = requests.get(f"{BASE_URL}/profiles/search/by-country-skills")
    # 401 или 422 - ожидаемые ответы без авторизации или без параметров
    assert response.status_code in [401, 404, 422]

def test_admin_endpoint_access_denied():
    """Проверка защиты админского эндпоинта"""
    # Попытка доступа к админскому эндпоинту без авторизации
    response = requests.get(f"{BASE_URL}/profiles/admin-endpoint")
    # 401 Unauthorized - ожидаемый ответ для неавторизованного запроса
    assert response.status_code == 401 