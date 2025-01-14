from typing import List

from pydantic import BaseModel

from models.test import Profile

def GetFirstName(profile: Profile):
    return {
        "first_name": profile.first_name  # Здесь передаем экземпляр профиля
    }

# Функция для получения всех имен
def all_names(profiles: List[Profile]):
    return [GetFirstName(profile) for profile in profiles]