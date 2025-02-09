# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Установка pytest и других тестовых зависимостей
RUN pip install pytest pytest-asyncio httpx

# Копируем весь проект
COPY . .

# Добавляем путь к модулям в PYTHONPATH
ENV PYTHONPATH=/app

# Указываем порт
EXPOSE 8000

# По умолчанию запускаем тесты
CMD ["pytest", "-v"] 