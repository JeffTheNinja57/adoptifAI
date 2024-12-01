from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import models, dependencies, translate
from ..database import get_session

router = APIRouter()


@router.post("/animals/{animal_id}/generate-translation")
async def generate_translation(
        animal_id: int,
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)):
    animal = db.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    translation = translate.translation_function(animal.description_en)
    if translation == "":
        raise HTTPException(status_code=404, detail="Translation function does not work yet")
    animal.description_nl = translation
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return {"description in NL": translation}
