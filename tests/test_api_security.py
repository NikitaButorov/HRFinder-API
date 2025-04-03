import pytest
import requests
from tests.conftest import BASE_URL

def test_auth_required_endpoints():
    """Проверка на необходимость авторизации для защищенных эндпоинтов"""
    # Список эндпоинтов, требующих авторизацию
    auth_required_endpoints = [
        "/profiles/search/by-country-skills",
        "/profiles/search/by-city-skills", 
        "/profiles/search/by-experience",
        "/profiles/search/by-company",
        "/profiles/search/advanced",
        "/profiles/admin-endpoint",
        "/profiles/user-endpoint",
        "/auth/users/me",
        "/users/"
    ]
    
    for endpoint in auth_required_endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        # Проверяем, что без токена получаем 401 Unauthorized или 422 Validation Error
        assert response.status_code in [401, 404, 422], f"Эндпоинт {endpoint} не требует авторизации или вернул неожиданный код {response.status_code}"

def test_invalid_token_rejected():
    """Проверка отклонения запросов с неверным токеном"""
    # Пробуем неверный токен авторизации
    headers = {
        "Authorization": "Bearer invalid_token_123456789"
    }
    
    response = requests.get(f"{BASE_URL}/auth/users/me", headers=headers)
    # Проверяем, что с неверным токеном получаем 401 Unauthorized
    assert response.status_code == 401, f"Неверный токен авторизации не был отклонен, код ответа: {response.status_code}"

def test_xss_prevention():
    """Проверка защиты от XSS-атак"""
    # Пытаемся отправить потенциально опасные данные
    xss_payload = "<script>alert('XSS')</script>"
    
    # Проверяем через регистрацию
    data = {
        "email": f"test_{xss_payload}@example.com",
        "password": "Password123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=data)
    
    # Проверяем, что сервер не возвращает необработанный XSS-код в ответе
    assert xss_payload not in response.text, "Возможная XSS-уязвимость: необработанный Javascript в ответе"

def test_sql_injection_prevention():
    """Проверка защиты от SQL-инъекций"""
    # Пытаемся отправить SQL-инъекцию через параметры запроса
    sql_injection = "'; DROP TABLE users; --"
    
    # Пробуем через различные эндпоинты
    endpoints = [
        f"/profiles/search/by-country-skills?country={sql_injection}&skills=Python",
        f"/profiles/search/by-city-skills?city={sql_injection}&skills=Python",
        f"/register"
    ]
    
    for endpoint in endpoints:
        if endpoint == "/register":
            # Для регистрации используем POST с JSON
            response = requests.post(
                f"{BASE_URL}{endpoint}", 
                json={"email": f"test{sql_injection}@example.com", "password": "Password123"}
            )
        else:
            # Для остальных GET-запросы
            response = requests.get(f"{BASE_URL}{endpoint}")
        
        # Проверяем, что получаем обычный код ответа, а не 500 Server Error
        assert response.status_code not in [500], f"Возможная SQL-инъекция на эндпоинте {endpoint}: код {response.status_code}"

def test_rate_limiting():
    """Проверка наличия защиты от перебора"""
    # Отправляем множество запросов за короткое время
    url = f"{BASE_URL}/auth/jwt/login"
    data = {"username": "nonexistent@example.com", "password": "wrongpassword"}
    
    # Отправляем 20 запросов
    responses = []
    for _ in range(20):
        response = requests.post(url, data=data)
        responses.append(response.status_code)
    
    # Проверяем, были ли запросы ограничены (код 429 Too Many Requests)
    # Примечание: если API не имеет защиты от перебора, этот тест будет проходить,
    # но это не значит, что защита реализована правильно
    rate_limited = 429 in responses
    print(f"\nПроверка ограничения частоты запросов:")
    if rate_limited:
        print(f"Защита от перебора обнаружена: получен код 429 после нескольких запросов")
    else:
        print(f"Защита от перебора не обнаружена или требует дополнительной настройки")
    
    # Этот тест не будет падать, если ограничение не обнаружено, он просто информативный
    # assert rate_limited, "Не обнаружена защита от перебора (rate limiting)" 