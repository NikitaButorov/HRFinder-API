import logging
from fastapi import FastAPI, APIRouter, HTTPException, Query
from models.test import Profile, ProfileBrief, ProfileWithTitle
from database.config import collection, check_connection
from typing import List
from datetime import datetime

app = FastAPI()
router = APIRouter()

@app.on_event("startup")
async def startup_event():
    await check_connection()

@router.get("/profile", response_model=Profile)
async def get_profile():
    profile = await collection.find_one()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile['_id'] = str(profile['_id'])
    return Profile(**profile)

@router.get("/profile/{public_identifier}", response_model=Profile)
async def get_profile_by_identifier(public_identifier: str):
    profile = await collection.find_one({"public_identifier": public_identifier})
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile['_id'] = str(profile['_id'])
    return Profile(**profile)

@router.get("/profis by country adn skills", response_model=List[ProfileBrief])
async def search_profiles(
    country: str,
    skills: List[str] = Query(..., description="List of required skills")
):
    query = {
        "country_full_name": country,
        "skills": {"$all": skills}
    }
    
    profiles = await collection.find(
        query,
        {"full_name": 1, "public_identifier": 1, "_id": 0}
    ).to_list(length=None)
    
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found matching criteria")
        
    return profiles

@router.get("/profis by city and skills", response_model=List[ProfileBrief])
async def search_profiles_by_city(
    city: str,
    skills: List[str] = Query(..., description="List of required skills")
):
    query = {
        "city": city,
        "skills": {"$all": skills}
    }
    
    profiles = await collection.find(
        query,
        {"full_name": 1, "public_identifier": 1, "_id": 0}
    ).to_list(length=None)
    
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found matching criteria")
        
    return profiles

@router.get("/profis by country and experience", response_model=List[ProfileBrief])
async def search_profiles_by_experience(
    country: str,
    min_years: int = Query(..., description="Minimum years of experience required"),
    skills: List[str] = Query(..., description="List of required skills")
):
    pipeline = [
        {
            "$match": {
                "country_full_name": country,
                "experiences": {"$exists": True, "$ne": []},
                "skills": {"$all": skills}
            }
        },
        {
            "$project": {
                "full_name": 1,
                "public_identifier": 1,
                "total_experience": {
                    "$reduce": {
                        "input": "$experiences",
                        "initialValue": 0,
                        "in": {
                            "$add": [
                                "$$value",
                                {
                                    "$subtract": [
                                        {"$ifNull": [{"$ifNull": ["$$this.ends_at.year", datetime.now().year]}, datetime.now().year]},
                                        {"$ifNull": [{"$ifNull": ["$$this.starts_at.year", datetime.now().year]}, datetime.now().year]}
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "$match": {
                "total_experience": {"$gte": min_years}
            }
        },
        {
            "$project": {
                "full_name": 1,
                "public_identifier": 1,
                "_id": 0
            }
        }
    ]
    
    profiles = await collection.aggregate(pipeline).to_list(length=None)
    
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found matching criteria")
        
    return profiles

@router.get("/profis by company", response_model=List[ProfileWithTitle])
async def search_profiles_by_company(
    company: str
):
    pipeline = [
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
        },
        {
            "$project": {
                "full_name": 1,
                "public_identifier": 1,
                "title": { "$arrayElemAt": ["$experience.title", 0] }
            }
        }
    ]
    
    profiles = await collection.aggregate(pipeline).to_list(length=None)
    
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found matching criteria")
        
    return profiles

app.include_router(router)