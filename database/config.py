from motor.motor_asyncio import AsyncIOMotorClient
import certifi

uri = "mongodb+srv://admin:admin@hrfinder.rt8ed.mongodb.net/?retryWrites=true&w=majority&appName=HRFinder"

# Создаем клиент с корректными параметрами
client = AsyncIOMotorClient(
    uri,
    tlsCAFile=certifi.where(),
    tls=True,
    tlsAllowInvalidCertificates=True  # Используем этот параметр вместо ssl_cert_reqs
)

db = client.HRFinder
collection = db["profiles"]

async def check_connection():
    try:
        await client.admin.command('ping')
        print("Успешное подключение к MongoDB!")
    except Exception as e:
        print(f"Ошибка подключения к MongoDB: {e}")