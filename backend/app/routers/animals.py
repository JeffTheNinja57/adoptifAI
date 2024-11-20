from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from backend.app import models, schemas, dependencies
from backend.app.database import get_session
from backend.app.crud import (
    get_animal_by_id,
    get_animals,
    create_animal,
    update_animal,
    delete_animal,
    create_animals_from_csv
)

router = APIRouter()

@router.get("/", response_model=List[schemas.AnimalRead])
def read_animals(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    animals = get_animals(db, skip=skip, limit=limit)
    return animals

@router.get("/{animal_id}", response_model=schemas.AnimalRead)
def read_animal(animal_id: int, db: Session = Depends(get_session)):
    animal = get_animal_by_id(db, animal_id=animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@router.post("/", response_model=schemas.AnimalRead)
def create_new_animal(animal: schemas.AnimalCreate, current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    animal.shelter_id = current_shelter.id
    new_animal = create_animal(db, animal)
    return new_animal

@router.put("/{animal_id}", response_model=schemas.AnimalRead)
def update_existing_animal(animal_id: int, animal: schemas.AnimalUpdate, current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal or db_animal.shelter_id != current_shelter.id:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    updated_animal = update_animal(db, db_animal, animal)
    return updated_animal

@router.delete("/{animal_id}")
def delete_existing_animal(animal_id: int, current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal or db_animal.shelter_id != current_shelter.id:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    delete_animal(db, db_animal)
    return {"detail": "Animal deleted successfully"}

@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...), current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type")
    animals_added = create_animals_from_csv(db, file.file, current_shelter.id)
    return {"detail": f"{animals_added} animals added successfully"}
