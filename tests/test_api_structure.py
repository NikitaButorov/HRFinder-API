import pytest
import requests
import json
from tests.conftest import BASE_URL

def test_openapi_schema_structure():
    """Проверка структуры OpenAPI схемы"""
    response = requests.get(f"{BASE_URL}/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    
    # Проверяем наличие основных элементов схемы OpenAPI
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
    
    # Проверяем версию OpenAPI
    assert schema["openapi"].startswith("3."), "Схема OpenAPI должна быть версии 3.x"
    
    # Проверяем информацию о сервисе
    assert "title" in schema["info"]
    assert "version" in schema["info"]
    
    # Проверяем наличие важных разделов путей
    paths = schema["paths"]
    assert any("/auth/" in path for path in paths.keys()), "Отсутствуют пути для аутентификации"
    assert any("/profiles/" in path for path in paths.keys()), "Отсутствуют пути для профилей"
    
    # Сохраняем основные группы эндпоинтов для аналитики
    groups = {}
    for path in paths.keys():
        prefix = path.split("/")[1] if len(path.split("/")) > 1 else "root"
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(path)
    
    # Выводим статистику по группам эндпоинтов
    print("\nГруппы эндпоинтов API:")
    for group, endpoints in groups.items():
        print(f"- {group}: {len(endpoints)} эндпоинтов")

def test_api_health_check():
    """Проверка работоспособности API через основной эндпоинт"""
    # Проверяем доступность документации API
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200, "Документация API недоступна"

def test_error_handling():
    """Проверка корректной обработки ошибок API"""
    # Запросы с ошибками к различным эндпоинтам
    test_cases = [
        # Несуществующий эндпоинт
        {"url": f"{BASE_URL}/nonexistent-endpoint", "expected_code": 404},
        
        # Неверный метод
        {"url": f"{BASE_URL}/auth/jwt/login", "method": "PUT", "expected_code": 405},
        
        # Некорректные данные
        {"url": f"{BASE_URL}/auth/jwt/login", "method": "POST", "data": {}, "expected_code": 422}
    ]
    
    for test_case in test_cases:
        method = test_case.get("method", "GET")
        url = test_case["url"]
        expected_code = test_case["expected_code"]
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            data = test_case.get("data", {})
            response = requests.post(url, json=data)
        elif method == "PUT":
            data = test_case.get("data", {})
            response = requests.put(url, json=data)
        else:
            raise ValueError(f"Неподдерживаемый метод: {method}")
        
        assert response.status_code == expected_code, f"Ожидался код {expected_code}, получен {response.status_code} для {method} {url}"
        
        # Проверяем, что API возвращает JSON с информацией об ошибке
        try:
            error_data = response.json()
            assert "detail" in error_data or "message" in error_data, "В ответе отсутствует информация об ошибке"
        except ValueError:
            # Если ответ не в формате JSON, то это ошибка
            pytest.fail(f"Ответ API не в формате JSON для {method} {url}")

def test_content_type_headers():
    """Проверка, что API возвращает правильные заголовки Content-Type"""
    response = requests.get(f"{BASE_URL}/openapi.json")
    assert response.status_code == 200
    
    # Проверяем Content-Type для JSON
    assert "application/json" in response.headers["Content-Type"], "Некорректный Content-Type для JSON ответа"
    
    # Проверяем Content-Type для HTML (документация)
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"], "Некорректный Content-Type для HTML ответа" 