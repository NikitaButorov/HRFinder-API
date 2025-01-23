from typing import List, Optional
from src.models.domain.profiles import Profile, ProfileBrief, ProfileWithTitle
from src.repositories import ProfileRepository
from src.models.domain.pagination import PaginatedResponse

class ProfileService:
    def __init__(self):
        self._repository = ProfileRepository()

    async def get_profile(self) -> Optional[Profile]:
        return await self._repository.find_one()

    async def get_profile_by_identifier(self, public_identifier: str) -> Optional[Profile]:
        return await self._repository.find_by_identifier(public_identifier)

    async def search_by_country_and_skills(
        self,
        country: str,
        skills: List[str],
        page: int = 1,
        size: int = 10
    ) -> PaginatedResponse[ProfileBrief]:
        skip = (page - 1) * size
        items, total = await self._repository.find_by_country_and_skills(
            country, skills, skip=skip, limit=size
        )
        
        pages = (total + size - 1) // size  # округление вверх
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def search_by_city_and_skills(
        self,
        city: str,
        skills: List[str],
        page: int = 1,
        size: int = 10
    ) -> PaginatedResponse[ProfileBrief]:
        skip = (page - 1) * size
        items, total = await self._repository.find_by_city_and_skills(
            city, skills, skip=skip, limit=size
        )
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def search_by_experience(
        self,
        country: Optional[str] = None,
        min_years: Optional[int] = None,
        max_years: Optional[int] = None,
        skills: Optional[List[str]] = None,
        sort_by_experience: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> PaginatedResponse[ProfileBrief]:
        """
        Поиск профилей по опыту работы и навыкам
        
        Args:
            country: Страна поиска (опционально)
            min_years: Минимальный опыт работы в годах (опционально)
            max_years: Максимальный опыт работы в годах (опционально)
            skills: Список требуемых навыков (опционально)
            sort_by_experience: Сортировка по опыту работы: 'asc' - по возрастанию, 'desc' - по убыванию (опционально)
            page: Номер страницы
            size: Размер страницы
        """
        skip = (page - 1) * size
        items, total = await self._repository.find_by_experience(
            country=country,
            min_years=min_years,
            max_years=max_years,
            skills=skills,
            sort_by_experience=sort_by_experience,
            skip=skip,
            limit=size
        )
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def search_by_company(
        self,
        company: str,
        page: int = 1,
        size: int = 10
    ) -> PaginatedResponse[ProfileWithTitle]:
        skip = (page - 1) * size
        items, total = await self._repository.find_by_company(
            company, skip=skip, limit=size
        )
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def advanced_search(
        self,
        page: int = 1,
        size: int = 10,
        **filters
    ) -> PaginatedResponse[ProfileBrief]:
        skip = (page - 1) * size
        items, total = await self._repository.advanced_search(
            skip=skip,
            limit=size,
            **filters
        )
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def check_profiles_skills(
        self,
        public_identifiers: List[str],
        required_skills: List[str]
    ) -> List[dict]:
        """
        Проверяет наличие требуемых навыков у группы профилей
        
        Returns:
            List[dict]: Список профилей с информацией о соответствии навыкам
            Каждый элемент содержит:
            - full_name: имя профиля
            - public_identifier: идентификатор профиля
            - has_skills: имеет ли все требуемые навыки
            - matching_skills: список совпадающих навыков
        """
        return await self._repository.check_profiles_skills(
            public_identifiers,
            required_skills
        )

    async def get_skills_distribution(
        self, 
        country: Optional[str] = None,
        skills: Optional[List[str]] = None,
        page: int = 1,
        size: int = 10
    ) -> PaginatedResponse[dict]:
        """
        Получить статистику по распространенности навыков с пагинацией
        
        Args:
            country: Опциональный фильтр по стране
            skills: Опциональный фильтр по списку навыков
            page: Номер страницы
            size: Размер страницы
        """
        skip = (page - 1) * size
        items, total = await self._repository.get_skills_distribution(
            country=country,
            skills=skills,
            skip=skip,
            limit=size
        )
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        ) 