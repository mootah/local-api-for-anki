from fastapi import APIRouter
from app.api.endpoints import yomitan

api_router = APIRouter()
api_router.include_router(yomitan.router, tags=["yomitan"])
