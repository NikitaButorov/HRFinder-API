from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

class DateInfo(BaseModel):
    day: int
    month: int
    year: int

    class Config:
        from_attributes = True

class Experience(BaseModel):
    company: str
    title: str
    starts_at: Optional[Union[datetime, DateInfo]] = None
    ends_at: Optional[Union[datetime, DateInfo]] = None
    company_linkedin_profile_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True

class Education(BaseModel):
    starts_at: Optional[DateInfo] = None
    ends_at: Optional[DateInfo] = None
    field_of_study: Optional[str] = None
    degree_name: Optional[str] = None
    school: Optional[str] = None
    school_linkedin_profile_url: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True

class Extra(BaseModel):
    github_profile_id: Optional[str] = None
    twitter_profile_id: Optional[str] = None
    facebook_profile_id: Optional[str] = None

    class Config:
        from_attributes = True

class InferredSalary(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None

    class Config:
        from_attributes = True

class Profile(BaseModel):
    public_identifier: str
    profile_pic_url: Optional[str] = None
    background_cover_image_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: str
    occupation: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    country: Optional[str] = None
    country_full_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    experiences: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    languages: Optional[List[str]] = []
    accomplishment_organisations: Optional[List[dict]] = []
    accomplishment_publications: Optional[List[dict]] = []
    accomplishment_honors_awards: Optional[List[dict]] = []
    accomplishment_patents: Optional[List[dict]] = []
    accomplishment_courses: Optional[List[dict]] = []
    accomplishment_projects: Optional[List[dict]] = []
    accomplishment_test_scores: Optional[List[dict]] = []
    volunteer_work: Optional[List[dict]] = []
    certifications: Optional[List[dict]] = []
    connections: Optional[float] = None
    people_also_viewed: Optional[List[dict]] = []
    recommendations: Optional[List[dict]] = []
    activities: Optional[List[dict]] = []
    similarly_named_profiles: Optional[List[dict]] = []
    articles: Optional[List[dict]] = []
    groups: Optional[List[dict]] = []
    extra: Optional[Extra] = None
    skills: Optional[List[str]] = []
    inferred_salary: Optional[InferredSalary] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    industry: Optional[str] = None
    interests: Optional[List[str]] = []
    personal_numbers: Optional[List[str]] = []
    personal_emails: Optional[List[str]] = []
    github: Optional[str] = None
    facebook: Optional[str] = None

    class Config:
        from_attributes = True

class ProfileBrief(BaseModel):
    full_name: str
    public_identifier: str

    class Config:
        from_attributes = True

class ProfileWithTitle(ProfileBrief):
    title: Optional[str] = None

    class Config:
        from_attributes = True 