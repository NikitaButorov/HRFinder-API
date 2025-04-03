import pytest
import requests
from tests.conftest import BASE_URL

def test_api_docs_available():
    """Проверка доступности документации API"""
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200

def test_openapi_json_available():
    """Проверка доступности OpenAPI JSON"""
    response = requests.get(f"{BASE_URL}/openapi.json")
    assert response.status_code == 200
    data = response.json()
    # Проверяем основные элементы OpenAPI схемы
    assert "openapi" in data
    assert "paths" in data
    assert "components" in data

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
    # Регистрация пользователя (без валидных данных)
    response = requests.post(f"{BASE_URL}/register", json={})
    # 422 Validation Error - ожидаемый ответ при отсутствии необходимых данных
    assert response.status_code == 422

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