# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и настройки проекта
COPY requirements.txt setup.py ./

# Копируем весь проект
COPY . .

# Устанавливаем зависимости и сам проект в режиме разработки
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Добавляем путь к модулям в PYTHONPATH
ENV PYTHONPATH=/app

# Указываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 