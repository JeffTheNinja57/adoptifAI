from fastapi import APIRouter

from backend.app.routers import auth, animals, shelters, descriptions

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(animals.router, prefix="/animals", tags=["animals"])
api_router.include_router(shelters.router, prefix="/shelters", tags=["shelters"])
api_router.include_router(descriptions.router, tags=["descriptions"])
