import pytest
import requests
from typing import Dict, Any

# URL для тестов - используем nginx на порту 8080
BASE_URL = "http://localhost:8080/api/v1"

# Информация о сервисе
SERVICE_INFO = {
    "title": "HR Finder API",
    "version": "1.0.0",
    "description": "API для поиска и анализа профилей LinkedIn"
}

# Вспомогательная функция для проверки доступности сервиса
def is_api_running() -> bool:
    try:
        # Проверяем доступность API через любой доступный без авторизации эндпоинт
        # auth/users/me всегда вернет 401 для неавторизованного запроса, что подтверждает работу API
        response = requests.get(f"{BASE_URL}/auth/users/me", timeout=2)
        return response.status_code == 401
    except requests.RequestException:
        return False

@pytest.fixture(scope="session")
def base_url() -> str:
    """Возвращает базовый URL для тестов"""
    # Проверяем, что API запущено
    if not is_api_running():
        pytest.skip("API не запущено. Запустите сервис перед запуском тестов.")
    
    return BASE_URL 