from fastapi import APIRouter
from app.api.endpoints import yomitan, fastwq

api_router = APIRouter()
api_router.include_router(yomitan.router, tags=["yomitan"])
api_router.include_router(fastwq.router, tags=["fastwq"])
