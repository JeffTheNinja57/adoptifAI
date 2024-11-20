from backend.app import models, schemas, dependencies
from backend.app.crud import update_shelter
from backend.app.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/me", response_model=schemas.ShelterRead)
def read_current_shelter(current_shelter: models.Shelter = Depends(dependencies.get_current_shelter)):
    return current_shelter


@router.put("/me", response_model=schemas.ShelterRead)
def update_current_shelter(shelter_update: schemas.ShelterUpdate,
                           current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
                           db: Session = Depends(get_session)):
    updated_shelter = update_shelter(db, current_shelter, shelter_update)
    return updated_shelter
