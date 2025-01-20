from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.models import Profile, ProfileBrief, ProfileWithTitle, PaginatedResponse
from src.services import ProfileService

router = APIRouter(prefix="/profiles", tags=["profiles"])
profile_service = ProfileService()

@router.get("", response_model=Profile)
async def get_profile():
    profile = await profile_service.get_profile()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/{public_identifier}", response_model=Profile)
async def get_profile_by_identifier(public_identifier: str):
    profile = await profile_service.get_profile_by_identifier(public_identifier)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/search/by-country-skills", response_model=PaginatedResponse[ProfileBrief])
async def search_profiles(
    country: str,
    skills: List[str] = Query(...),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):
    """
    Поиск профилей по стране и навыкам с пагинацией
    - **country**: Страна поиска
    - **skills**: Список требуемых навыков
    - **page**: Номер страницы (начиная с 1)
    - **size**: Количество элементов на странице (от 1 до 100)
    """
    result = await profile_service.search_by_country_and_skills(
        country, skills, page=page, size=size
    )
    if not result.items:
        raise HTTPException(
            status_code=404,
            detail="No profiles found matching criteria"
        )
    return result

@router.get("/search/by-city-skills", response_model=PaginatedResponse[ProfileBrief])
async def search_profiles_by_city(
    city: str,
    skills: List[str] = Query(..., description="Список требуемых навыков"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):
    """
    Поиск профилей по городу и навыкам с пагинацией
    - **city**: Город поиска
    - **skills**: Список требуемых навыков
    - **page**: Номер страницы (начиная с 1)
    - **size**: Количество элементов на странице (от 1 до 100)
    """
    result = await profile_service.search_by_city_and_skills(
        city, skills, page=page, size=size
    )
    if not result.items:
        raise HTTPException(
            status_code=404,
            detail="No profiles found matching criteria"
        )
    return result

@router.get("/search/by-experience", response_model=PaginatedResponse[ProfileBrief])
async def search_profiles_by_experience(
    country: Optional[str] = None,
    min_years: Optional[int] = Query(None, ge=0, description="Минимальный опыт работы в годах"),
    max_years: Optional[int] = Query(None, ge=0, description="Максимальный опыт работы в годах"),
    skills: Optional[List[str]] = Query(None, description="Список требуемых навыков"),
    sort_by_experience: Optional[str] = Query(None, description="Сортировка по опыту работы: 'asc' - по возрастанию, 'desc' - по убыванию"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):
    """
    Поиск профилей по опыту работы, стране и навыкам с пагинацией
    - **country**: Страна поиска (опционально)
    - **min_years**: Минимальный опыт работы в годах (опционально)
    - **max_years**: Максимальный опыт работы в годах (опционально)
    - **skills**: Список требуемых навыков (опционально)
    - **sort_by_experience**: Сортировка по опыту работы: 'asc' - по возрастанию, 'desc' - по убыванию (опционально)
    - **page**: Номер страницы (начиная с 1)
    - **size**: Количество элементов на странице (от 1 до 100)
    """
    result = await profile_service.search_by_experience(
        country=country,
        min_years=min_years,
        max_years=max_years,
        skills=skills,
        sort_by_experience=sort_by_experience,
        page=page,
        size=size
    )
    if not result.items:
        raise HTTPException(
            status_code=404,
            detail="No profiles found matching criteria"
        )
    return result

@router.get("/search/by-company", response_model=PaginatedResponse[ProfileWithTitle])
async def search_profiles_by_company(
    company: str,
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):
    """
    Поиск профилей по компании с пагинацией
    - **company**: Название компании
    - **page**: Номер страницы (начиная с 1)
    - **size**: Количество элементов на странице (от 1 до 100)
    """
    result = await profile_service.search_by_company(
        company, page=page, size=size
    )
    if not result.items:
        raise HTTPException(
            status_code=404,
            detail="No profiles found matching criteria"
        )
    return result

@router.get("/search/advanced", response_model=PaginatedResponse[ProfileBrief])
async def advanced_search(
    countries: Optional[List[str]] = Query(None),
    cities: Optional[List[str]] = Query(None),
    skills: Optional[List[str]] = Query(None),
    experience_min: Optional[int] = Query(None),
    experience_max: Optional[int] = Query(None),
    companies: Optional[List[str]] = Query(None),
    languages: Optional[List[str]] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    """
    Расширенный поиск профилей с пагинацией
    """
    result = await profile_service.advanced_search(
        countries=countries,
        cities=cities,
        skills=skills,
        experience_min=experience_min,
        experience_max=experience_max,
        companies=companies,
        languages=languages,
        page=page,
        size=size
    )
    return result

@router.get("/batch/skills-check")
async def check_profiles_skills(
    public_identifiers: List[str] = Query(...),
    required_skills: List[str] = Query(...)
):
    """Проверить наличие навыков у группы профилей"""
    return await profile_service.check_profiles_skills(
        public_identifiers, required_skills
    )

@router.get("/analytics/skills-distribution", response_model=PaginatedResponse[dict])
async def get_skills_distribution(
    country: Optional[str] = None,
    skills: Optional[List[str]] = Query(None, description="Фильтр по списку навыков"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):
    """
    Получить статистику по распространенности навыков с пагинацией
    - **country**: Опциональный фильтр по стране
    - **skills**: Опциональный фильтр по списку навыков
    - **page**: Номер страницы (начиная с 1)
    - **size**: Количество элементов на странице (от 1 до 100)
    """
    return await profile_service.get_skills_distribution(
        country=country,
        skills=skills,
        page=page,
        size=size
    )