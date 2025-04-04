# HRFinder API

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-brightgreen)
![MongoDB](https://img.shields.io/badge/MongoDB-3.3.0+-orange)

HRFinder API — это мощный инструмент для поиска и анализа профилей LinkedIn, разработанный для HR-специалистов и рекрутеров. API предоставляет удобный программный интерфейс для поиска кандидатов по различным критериям, таким как страна, город, навыки, опыт работы и компания.

## 🚀 Возможности

- **Поиск профилей по различным критериям:**
  - По стране и навыкам
  - По городу и навыкам
  - По опыту работы
  - По компании
  - Расширенный поиск с комбинацией параметров

- **Аналитические функции:**
  - Анализ распределения навыков
  - Групповая проверка навыков у профилей

- **Пагинация результатов поиска**
- **Авторизация и аутентификация через JWT**
- **Разграничение доступа на основе ролей (ADMIN, USER)**

## 🔧 Технологии

- **FastAPI** — современный веб-фреймворк для Python
- **MongoDB** — NoSQL база данных
- **Beanie** — ODM для MongoDB
- **FastAPI Users** — система авторизации и аутентификации
- **Docker & Docker Compose** — контейнеризация и оркестрация
- **Nginx** — обратный прокси-сервер

## 📋 Требования

- Python 3.10+
- Docker и Docker Compose (для запуска через контейнеры)
- MongoDB (при разработке без Docker)

## 🔌 Запуск проекта

### С использованием Docker (рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/hrfinder-api.git
   cd hrfinder-api
   ```

2. Запустите с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. API будет доступно по адресу:
   - API напрямую: http://localhost:8000
   - Через Nginx: http://localhost:8080
   - Документация: http://localhost:8080/docs
   - OpenAPI схема: http://localhost:8080/openapi.json

### Локальная разработка (без Docker)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/hrfinder-api.git
   cd hrfinder-api
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. Запустите сервер разработки:
   ```bash
   uvicorn src.main:app --reload
   ```

4. API будет доступно по адресу http://localhost:8000

### Учетные данные по умолчанию
- Email: admin@example.com
- Пароль: admin

## 🧪 Тестирование

Для запуска тестов необходимо иметь запущенный сервис API:

### В Windows:
```bash
run_tests.bat
```

### В Linux/MacOS:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Запуск конкретных тестов:
```bash
# Windows
run_tests.bat tests/test_api_availability.py

# Linux/MacOS
./run_tests.sh tests/test_api_structure.py::test_api_health_check
```

После запуска тестов создается HTML-отчет `report.html` с подробной информацией о результатах.

## 📚 Документация API

Полная документация API доступна через Swagger UI после запуска сервера по адресу `/docs`.

## 📦 Основные эндпоинты

### Авторизация
- `POST /api/v1/auth/register` — Регистрация нового пользователя
- `POST /api/v1/auth/jwt/login` — Получение JWT токена

### Профили
- `GET /api/v1/profiles/{public_identifier}` — Получение профиля по идентификатору
- `GET /api/v1/profiles/search/by-country-skills` — Поиск по стране и навыкам
- `GET /api/v1/profiles/search/by-city-skills` — Поиск по городу и навыкам
- `GET /api/v1/profiles/search/by-experience` — Поиск по опыту работы
- `GET /api/v1/profiles/search/by-company` — Поиск по компании
- `GET /api/v1/profiles/search/advanced` — Расширенный поиск профилей
- `GET /api/v1/profiles/batch/skills-check` — Проверка навыков у группы профилей
- `GET /api/v1/profiles/analytics/skills-distribution` — Анализ распределения навыков

## 🛠️ Структура проекта
├── .github/ # Конфигурация GitHub Actions
├── nginx/ # Конфигурация Nginx
├── src/ # Исходный код
│ ├── api/ # API эндпоинты
│ ├── core/ # Ядро приложения
│ ├── models/ # Модели данных
│ ├── repositories/ # Взаимодействие с БД
│ ├── services/ # Бизнес-логика
│ └── main.py # Точка входа
├── tests/ # Тесты
├── .gitignore # Исключения Git
├── docker-compose.yml # Конфигурация Docker Compose
├── Dockerfile # Инструкции для сборки образа
├── requirements.txt # Зависимости проекта
├── requirements-dev.txt # Зависимости для разработки
├── setup.py # Установка пакета
├── run_tests.sh # Скрипт запуска тестов (Linux)
└── run_tests.bat # Скрипт запуска тестов (Windows)


## 📝 Лицензия

Этот проект лицензирован под [MIT License](LICENSE).

## 🤝 Вклад в проект

Вклады приветствуются! Пожалуйста, ознакомьтесь с руководством по вкладу перед отправкой pull request.
