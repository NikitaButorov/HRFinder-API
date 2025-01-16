from fastapi import APIRouter

router = APIRouter()

from .endpoints import profiles
router.include_router(profiles.router) 