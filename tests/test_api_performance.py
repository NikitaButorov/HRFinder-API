import pytest
import requests
import time
from statistics import mean, stdev
from tests.conftest import BASE_URL

@pytest.mark.performance
def test_api_response_time():
    """Тест времени отклика API"""
    # Используем эндпоинт авторизации, который должен отвечать с 401 для неавторизованного запроса
    url = f"{BASE_URL}/auth/users/me"
    
    # Сделаем 5 замеров времени запроса
    response_times = []
    for _ in range(5):
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        
        assert response.status_code == 401
        response_times.append(end_time - start_time)
    
    # Рассчитываем среднее время ответа и стандартное отклонение
    avg_time = mean(response_times)
    std_time = stdev(response_times) if len(response_times) > 1 else 0
    
    # Выводим информацию о времени ответа
    print(f"\nВремя ответа API:")
    print(f"Среднее: {avg_time:.3f} сек")
    print(f"Стандартное отклонение: {std_time:.3f} сек")
    print(f"Минимальное: {min(response_times):.3f} сек")
    print(f"Максимальное: {max(response_times):.3f} сек")
    
    # Проверяем, что среднее время ответа меньше 1 секунды
    assert avg_time < 1.0, f"Среднее время ответа ({avg_time:.3f} сек) превышает 1 секунду"

@pytest.mark.performance
def test_concurrent_requests():
    """Тест производительности при параллельных запросах"""
    # Используем эндпоинт авторизации, который должен отвечать с 401 для неавторизованного запроса
    url = f"{BASE_URL}/auth/users/me"
    
    import concurrent.futures
    
    # Функция для запроса
    def make_request():
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        return end_time - start_time, response.status_code
    
    # Запускаем 10 параллельных запросов
    num_requests = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # Анализируем результаты
    response_times = [r[0] for r in results]
    status_codes = [r[1] for r in results]
    
    # Проверяем, что все запросы возвращают ожидаемый статус
    assert all(code == 401 for code in status_codes), "Не все запросы вернули ожидаемый статус 401"
    
    # Выводим статистику
    avg_time = mean(response_times)
    max_time = max(response_times)
    
    print(f"\nВремя ответа при {num_requests} параллельных запросах:")
    print(f"Среднее: {avg_time:.3f} сек")
    print(f"Максимальное: {max_time:.3f} сек")
    
    # Проверяем производительность
    assert avg_time < 2.0, f"Среднее время ответа ({avg_time:.3f} сек) при параллельных запросах слишком велико" 