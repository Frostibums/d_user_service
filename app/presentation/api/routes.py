from fastapi import APIRouter

from app.presentation.api.v1.endpoints import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
