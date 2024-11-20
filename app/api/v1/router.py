from fastapi import APIRouter
from app.api.v1.endpoints import animals, shelters

# Create main v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    animals.router,
    prefix="/animals",
    tags=["animals"]
)

api_router.include_router(
    shelters.router,
    prefix="/shelters",
    tags=["shelters"]
)