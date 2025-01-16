from typing import List, Optional
from datetime import datetime
from models.domain.profiles import Profile, ProfileBrief, ProfileWithTitle
from core.database import Database

class ProfileRepository:
    def __init__(self):
        Database.connect_to_database()
        self.collection = Database.db["profiles"]

    def _convert_dates(self, profile: dict) -> dict:
        """Конвертирует даты из MongoDB формата в datetime"""
        if profile and "experiences" in profile:
            for exp in profile["experiences"]:
                if "starts_at" in exp and exp["starts_at"]:
                    exp["starts_at"] = exp["starts_at"]
                if "ends_at" in exp and exp["ends_at"]:
                    exp["ends_at"] = exp["ends_at"]
                else:
                    exp["ends_at"] = None
        return profile

    async def find_one(self) -> Optional[Profile]:
        profile = await self.collection.find_one()
        if profile:
            profile['_id'] = str(profile['_id'])
            profile = self._convert_dates(profile)
            return Profile(**profile)
        return None

    async def find_by_identifier(self, public_identifier: str) -> Optional[Profile]:
        profile = await self.collection.find_one({"public_identifier": public_identifier})
        if profile:
            profile['_id'] = str(profile['_id'])
            profile = self._convert_dates(profile)
            return Profile(**profile)
        return None

    async def find_by_country_and_skills(
        self, 
        country: str, 
        skills: List[str],
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[ProfileBrief], int]:
        query = {
            "country_full_name": country,
            "skills": {"$all": skills}
        }
        
        # Получаем общее количество документов
        total = await self.collection.count_documents(query)
        
        # Получаем документы с пагинацией
        cursor = self.collection.find(
            query,
            {"full_name": 1, "public_identifier": 1, "_id": 0}
        ).skip(skip).limit(limit)
        
        items = await cursor.to_list(length=None)
        return items, total

    async def find_by_city_and_skills(
        self, 
        city: str, 
        skills: List[str],
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[ProfileBrief], int]:
        query = {
            "city": city,
            "skills": {"$all": skills}
        }
        
        total = await self.collection.count_documents(query)
        
        cursor = self.collection.find(
            query,
            {"full_name": 1, "public_identifier": 1, "_id": 0}
        ).skip(skip).limit(limit)
        
        items = await cursor.to_list(length=None)
        return items, total

    async def find_by_experience(
        self,
        country: Optional[str] = None,
        min_years: Optional[int] = None,
        max_years: Optional[int] = None,
        skills: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[ProfileBrief], int]:
        """
        Поиск профилей по опыту работы, стране и навыкам
        
        Args:
            country: Страна поиска (опционально)
            min_years: Минимальный опыт работы в годах (опционально)
            max_years: Максимальный опыт работы в годах (опционально)
            skills: Список требуемых навыков (опционально)
            skip: Количество пропускаемых документов
            limit: Максимальное количество возвращаемых документов
        """
        pipeline = []
        
        # Базовые фильтры
        match_conditions = {}
        
        if country:
            match_conditions["country_full_name"] = country
        
        if skills:
            match_conditions["skills"] = {"$all": skills}
        
        if match_conditions:
            pipeline.append({"$match": match_conditions})
        
        # Основной пайплайн для подсчета опыта
        pipeline.extend([
            # Разворачиваем опыт работы
            {'$unwind': {'path': '$experiences', 'preserveNullAndEmptyArrays': True}},
            
            # Вычисляем опыт для каждой позиции
            {'$addFields': {
                'years_in_position': {
                    '$divide': [
                        {'$subtract': [
                            {'$cond': [
                                {'$eq': ['$experiences.ends_at', None]},
                                {'$year': '$$NOW'},
                                {'$ifNull': ['$experiences.ends_at.year', {'$year': '$$NOW'}]}
                            ]},
                            {'$ifNull': ['$experiences.starts_at.year', {'$year': '$$NOW'}]}
                        ]},
                        1
                    ]
                }
            }},
            
            # Группируем по профилю и суммируем опыт
            {'$group': {
                '_id': '$_id',
                'public_identifier': {'$first': '$public_identifier'},
                'full_name': {'$first': '$full_name'},
                'total_experience': {'$sum': '$years_in_position'}
            }}
        ])
        
        # Фильтрация по опыту (если указаны границы)
        if min_years is not None or max_years is not None:
            experience_filter = {}
            if min_years is not None:
                experience_filter['$gte'] = min_years
            if max_years is not None:
                experience_filter['$lte'] = max_years
            
            if experience_filter:
                pipeline.append({
                    '$match': {
                        'total_experience': experience_filter
                    }
                })
        
        # Проекция нужных полей
        pipeline.append({
            '$project': {
                '_id': 0,
                'public_identifier': 1,
                'full_name': 1,
                'total_experience': 1
            }
        })
        
        # Сортировка по опыту
        pipeline.append({
            '$sort': {'total_experience': -1}
        })
        
        # Получаем общее количество
        count_pipeline = pipeline.copy()
        count_pipeline.append({'$count': 'total'})
        count_result = await self.collection.aggregate(count_pipeline).to_list(None)
        total = count_result[0]['total'] if count_result else 0
        
        # Добавляем пагинацию
        pipeline.extend([
            {'$skip': skip},
            {'$limit': limit}
        ])
        
        items = await self.collection.aggregate(pipeline).to_list(None)
        return items, total

    async def find_by_company(
        self, 
        company: str,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[ProfileWithTitle], int]:
        base_pipeline = [
            {
                "$match": {
                    "experiences.company": company
                }
            },
            {
                "$project": {
                    "full_name": 1,
                    "public_identifier": 1,
                    "experience": {
                        "$filter": {
                            "input": "$experiences",
                            "as": "exp",
                            "cond": { "$eq": ["$$exp.company", company] }
                        }
                    }
                }
            }
        ]

        # Получаем общее количество
        count_pipeline = base_pipeline.copy()
        count_pipeline.append({"$count": "total"})
        count_result = await self.collection.aggregate(count_pipeline).to_list(length=1)
        total = count_result[0]["total"] if count_result else 0

        # Добавляем пагинацию и финальную проекцию
        pipeline = base_pipeline + [
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "full_name": 1,
                    "public_identifier": 1,
                    "title": { "$arrayElemAt": ["$experience.title", 0] }
                }
            }
        ]

        items = await self.collection.aggregate(pipeline).to_list(length=None)
        return items, total

    async def advanced_search(
        self,
        skip: int = 0,
        limit: int = 10,
        **filters
    ) -> tuple[List[ProfileBrief], int]:
        query = {}
        
        if filters.get('countries'):
            query['country_full_name'] = {'$in': filters['countries']}
        if filters.get('cities'):
            query['city'] = {'$in': filters['cities']}
        if filters.get('skills'):
            query['skills'] = {'$all': filters['skills']}
        if filters.get('companies'):
            query['experiences.company'] = {'$in': filters['companies']}
        if filters.get('languages'):
            query['languages'] = {'$all': filters['languages']}
        
        # Добавляем фильтр по опыту работы, если указан
        if filters.get('experience_min') or filters.get('experience_max'):
            experience_filter = {}
            if filters.get('experience_min'):
                experience_filter['$gte'] = filters['experience_min']
            if filters.get('experience_max'):
                experience_filter['$lte'] = filters['experience_max']
            
            pipeline = [
                {'$match': query},
                {
                    '$addFields': {
                        'total_experience': {
                            '$reduce': {
                                'input': '$experiences',
                                'initialValue': 0,
                                'in': {
                                    '$add': [
                                        '$$value',
                                        {
                                            '$subtract': [
                                                {'$ifNull': [{'$ifNull': ['$$this.ends_at.year', datetime.now().year]}, datetime.now().year]},
                                                {'$ifNull': ['$$this.starts_at.year', datetime.now().year]}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                },
                {'$match': {'total_experience': experience_filter}},
            ]
            
            # Получаем общее количество
            count_pipeline = pipeline.copy()
            count_pipeline.append({'$count': 'total'})
            count_result = await self.collection.aggregate(count_pipeline).to_list(length=1)
            total = count_result[0]['total'] if count_result else 0
            
            # Добавляем пагинацию
            pipeline.extend([
                {'$skip': skip},
                {'$limit': limit},
                {
                    '$project': {
                        'full_name': 1,
                        'public_identifier': 1,
                        '_id': 0
                    }
                }
            ])
            
            items = await self.collection.aggregate(pipeline).to_list(length=None)
            return items, total
        
        # Если нет фильтров по опыту, используем простой поиск
        total = await self.collection.count_documents(query)
        
        cursor = self.collection.find(
            query,
            {'full_name': 1, 'public_identifier': 1, '_id': 0}
        ).skip(skip).limit(limit)
        
        items = await cursor.to_list(length=None)
        return items, total

    async def check_profiles_skills(
        self,
        public_identifiers: List[str],
        required_skills: List[str]
    ) -> List[dict]:
        pipeline = [
            {
                "$match": {
                    "public_identifier": {"$in": public_identifiers}
                }
            },
            {
                "$project": {
                    "full_name": 1,
                    "public_identifier": 1,
                    "has_skills": {
                        "$setIsSubset": [required_skills, "$skills"]
                    },
                    "matching_skills": {
                        "$setIntersection": [required_skills, "$skills"]
                    },
                    "_id": 0
                }
            }
        ]
        
        return await self.collection.aggregate(pipeline).to_list(None)

    async def get_skills_distribution(
        self, 
        country: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[dict], int]:
        """Получить статистику по распространенности навыков с пагинацией"""
        pipeline = []
        
        # Добавляем фильтр по стране, если указан
        if country:
            pipeline.append({'$match': {'country_full_name': country}})
        
        # Основной пайплайн для подсчета навыков
        pipeline.extend([
            {'$unwind': '$skills'},
            {'$group': {
                '_id': '$skills',
                'count': {'$sum': 1}
            }},
            {'$project': {
                '_id': 0,
                'skill': '$_id',
                'count': 1
            }},
            {'$sort': {'count': -1}}
        ])
        
        # Получаем общее количество уникальных навыков
        count_pipeline = pipeline.copy()
        count_pipeline.append({'$count': 'total'})
        count_result = await self.collection.aggregate(count_pipeline).to_list(None)
        total = count_result[0]['total'] if count_result else 0
        
        # Добавляем пагинацию
        pipeline.extend([
            {'$skip': skip},
            {'$limit': limit}
        ])
        
        items = await self.collection.aggregate(pipeline).to_list(None)
        return items, total 