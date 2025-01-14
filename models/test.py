from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class DateInfo(BaseModel):
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

class Experience(BaseModel):
    starts_at: Optional[DateInfo] = None
    ends_at: Optional[DateInfo] = None
    company: Optional[str] = None
    company_linkedin_profile_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None

class Education(BaseModel):
    starts_at: Optional[DateInfo] = None
    ends_at: Optional[DateInfo] = None
    field_of_study: Optional[str] = None
    degree_name: Optional[str] = None
    school: Optional[str] = None
    school_linkedin_profile_url: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None

class Extra(BaseModel):
    github_profile_id: Optional[str] = None
    twitter_profile_id: Optional[str] = None
    facebook_profile_id: Optional[str] = None

class InferredSalary(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None

class ProfileBrief(BaseModel):
    full_name: str
    public_identifier: str

    class Config:
        from_attributes = True

class Profile(BaseModel):
    public_identifier: Optional[str] = None
    profile_pic_url: Optional[str] = None
    background_cover_image_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    occupation: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    country: Optional[str] = None
    country_full_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    experiences: Optional[List[Experience]] = []
    education: Optional[List[Education]] = []
    languages: Optional[List[str]] = []
    accomplishment_organisations: Optional[List] = []
    accomplishment_publications: Optional[List] = []
    accomplishment_honors_awards: Optional[List] = []
    accomplishment_patents: Optional[List] = []
    accomplishment_courses: Optional[List] = []
    accomplishment_projects: Optional[List] = []
    accomplishment_test_scores: Optional[List] = []
    volunteer_work: Optional[List] = []
    certifications: Optional[List] = []
    connections: Optional[float] = None
    people_also_viewed: Optional[List] = []
    recommendations: Optional[List] = []
    activities: Optional[List] = []
    similarly_named_profiles: Optional[List] = []
    articles: Optional[List] = []
    groups: Optional[List] = []
    extra: Optional[Extra] = None
    skills: Optional[List[str]] = []
    inferred_salary: Optional[InferredSalary] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    industry: Optional[str] = None
    interests: Optional[List] = []
    personal_numbers: Optional[List] = []
    personal_emails: Optional[List] = []
    github: Optional[str] = None
    facebook: Optional[str] = None

    class Config:
        from_attributes = True

class ProfileWithTitle(BaseModel):
    full_name: str
    public_identifier: str
    title: str

    class Config:
        from_attributes = True