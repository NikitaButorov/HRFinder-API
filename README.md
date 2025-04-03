# HRFinder API

API для поиска и анализа профилей LinkedIn.

## Запуск с использованием Docker

### Требования
- Docker
- Docker Compose

### Шаги для запуска

1. Клонируйте репозиторий
```bash
git clone <url-репозитория>
cd HRFinder-API
```

2. Запустите проект с помощью Docker Compose
```bash
docker-compose up --build
```

3. Доступ к API
- API будет доступен по адресу: http://localhost:8000
- Через Nginx: http://localhost:8080
- Документация API доступна по адресу: http://localhost:8080/docs
- OpenAPI схема: http://localhost:8080/openapi.json

### Учетные данные по умолчанию
- Email: admin@example.com
- Пароль: admin

## Разработка

Для локальной разработки без Docker:

1. Установите зависимости
```bash
pip install -r requirements.txt
pip install -e .
```

2. Запустите сервер
```bash
uvicorn src.main:app --reload
```

## Запуск тестов

Для запуска тестов необходимо иметь запущенный сервис API через Docker Compose или напрямую.

### В Windows:
```bash
# Запуск всех тестов
run_tests.bat

# Запуск конкретного теста или модуля
run_tests.bat tests/test_api_availability.py
run_tests.bat tests/test_api_structure.py::test_api_health_check
```

### В Linux/MacOS:
```bash
# Дать права на выполнение скрипта
chmod +x run_tests.sh

# Запуск всех тестов
./run_tests.sh

# Запуск конкретного теста или модуля
./run_tests.sh tests/test_api_availability.py
./run_tests.sh tests/test_api_structure.py::test_api_health_check
```

### Доступные тесты:

1. **Тесты доступности API** (`test_api_availability.py`):
   - Проверка доступности документации
   - Проверка доступности различных эндпоинтов
   - Проверка требования авторизации для защищенных эндпоинтов

2. **Тесты структуры API** (`test_api_structure.py`):
   - Проверка соответствия API спецификации OpenAPI
   - Проверка наличия необходимых эндпоинтов
   - Анализ структуры API

3. **Тесты безопасности** (`test_api_security.py`):
   - Проверка защиты эндпоинтов требующих авторизацию
   - Проверка отклонения неверных токенов
   - Тесты на XSS и SQL-инъекции
   - Проверка ограничения частоты запросов

4. **Тесты производительности** (`test_api_performance.py`):
   - Тесты времени отклика API
   - Тесты параллельных запросов

### Отчет о тестировании

После запуска тестов создается HTML-отчет `report.html` с подробной информацией о результатах тестирования.

## Важные примечания

### Настройка Nginx

Для корректной работы документации API (Swagger UI) необходимо настроить Nginx для проксирования запросов к `/docs` и `/openapi.json`. Пример конфигурации есть в файле `nginx/nginx.conf`:

```nginx
location ~ ^/(docs|redoc|openapi.json) {
    proxy_pass http://fastapi_app;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
}
``` 