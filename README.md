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