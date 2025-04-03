@echo off
chcp 65001 > nul
REM Скрипт для запуска тестов в Windows

echo Проверка доступности сервиса на http://localhost:8080...
curl -s -o nul -w "%%{http_code}" http://localhost:8080/api/v1/auth/users/me

if %ERRORLEVEL% NEQ 0 (
    echo Сервис не доступен. Убедитесь, что API запущено через docker-compose.
    exit /b 1
)

REM Проверяем, что ответ 401 (требуется авторизация), что указывает на то, что API работает
for /f %%i in ('curl -s -o nul -w "%%{http_code}" http://localhost:8080/api/v1/auth/users/me') do set HTTP_STATUS=%%i
if NOT "%HTTP_STATUS%"=="401" (
    echo API не отвечает ожидаемым образом. Код ответа: %HTTP_STATUS%
    exit /b 1
)

echo Сервис доступен. Устанавливаем зависимости для тестов...

REM Устанавливаем зависимости для тестов
pip install -q pytest requests pytest-html

REM Получаем аргументы для запуска конкретных тестов
set TEST_ARGS=%*
if "%TEST_ARGS%"=="" (
    set TEST_ARGS=tests/
)

REM Запускаем тесты
echo Запуск тестов...
python -m pytest %TEST_ARGS% -v --html=report.html --self-contained-html

REM Проверяем, был ли создан отчет
if exist report.html (
    echo Отчет о тестировании сохранен в файл report.html
)

REM Показываем отчет
echo Тесты завершены. 