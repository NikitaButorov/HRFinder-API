#!/bin/bash
# Скрипт для запуска тестов

# Проверяем, запущен ли сервис
echo "Проверка доступности сервиса на http://localhost:8080..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/v1/docs

if [ $? -ne 0 ]; then
    echo "Сервис не доступен. Убедитесь, что API запущено через docker-compose."
    exit 1
fi

echo "Сервис доступен. Устанавливаем зависимости для тестов..."

# Устанавливаем зависимости для тестов
pip install -q pytest requests pytest-html

# Получаем аргументы для запуска конкретных тестов
if [ $# -eq 0 ]; then
    TEST_ARGS="tests/"
else
    TEST_ARGS="$@"
fi

# Запускаем тесты
echo "Запуск тестов..."
python -m pytest $TEST_ARGS -v --html=report.html --self-contained-html

# Проверяем, был ли создан отчет
if [ -f "report.html" ]; then
    echo "Отчет о тестировании сохранен в файл report.html"
fi

# Показываем отчет
echo "Тесты завершены." 