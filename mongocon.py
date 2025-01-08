from pymongo import MongoClient
import json


MONGO_URI = "mongodb+srv://admin:admin@hrfinder.rt8ed.mongodb.net/?retryWrites=true&w=majority&appName=HRFinder"


client = MongoClient(MONGO_URI)


db = client["HRFinder"]
collection = db["profiles"]


with open("combined.json", "r", encoding="utf-8") as file:
    data = json.load(file)


if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Данные успешно загружены в MongoDB!")
