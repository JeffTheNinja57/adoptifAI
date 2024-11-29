from fastapi import APIRouter

from . import auth, animals, shelters, descriptions, translations

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(animals.router, prefix="/animals", tags=["animals"])
api_router.include_router(shelters.router, prefix="/shelters", tags=["shelters"])
api_router.include_router(descriptions.router, tags=["descriptions"])
api_router.include_router(translations.router, tags=["translations"])
