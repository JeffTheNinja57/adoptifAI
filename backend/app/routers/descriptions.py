from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, dependencies
from backend.app.database import get_session
from backend.app.generator import generate_description
from backend.app.chunked import generate_descriptions_batch

router = APIRouter()

@router.post("/animals/{animal_id}/generate-description")
async def generate_animal_description(animal_id: int, current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    if not current_shelter.api_key:
        raise HTTPException(status_code=400, detail="API key not set")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id, models.Animal.shelter_id == current_shelter.id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    description = await generate_description(animal)
    animal.description_en = description
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return {"description": description}

@router.post("/animals/generate-descriptions-batch")
async def generate_descriptions_for_all(current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    if not current_shelter.api_key:
        raise HTTPException(status_code=400, detail="API key not set")
    animals = db.query(models.Animal).filter(models.Animal.shelter_id == current_shelter.id).all()
    await generate_descriptions_batch(db, animals)
    return {"detail": "Descriptions generated successfully"}

# For translations, you need to implement the translation function (not provided)
