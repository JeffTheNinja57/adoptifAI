from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .. import models, dependencies
from ..database import get_session
from ..generator import generate_description
from ..chunked import generate_descriptions_batch

router = APIRouter()


@router.post("/animals/{animal_id}/generate-description")
async def generate_animal_description(
        animal_id: int,
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)
):
    if not current_shelter.api_key:
        raise HTTPException(status_code=400, detail="API key not set")
    animal = db.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    # Pass the api_key to the generate_description function
    description = await generate_description(animal, current_shelter.api_key)
    animal.description_en = description
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return {"description": description}


@router.post("/animals/generate-descriptions-batch")
async def generate_descriptions_for_all(
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)):
    if not current_shelter.api_key:
        raise HTTPException(status_code=400, detail="API key not set")
    stmt = select(models.Animal).where(models.Animal.shelter_id == current_shelter.id)
    animals = db.exec(stmt).all()
    await generate_descriptions_batch(db, animals)
    return {"detail": "Descriptions generated successfully"}
