from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select

from .. import models, schemas, dependencies
from ..crud import create_animals_from_csv
from ..database import get_session

router = APIRouter()


@router.get("/my-animals", response_model=List[schemas.AnimalRead])
def get_my_animals(
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)
):
    statement = select(models.Animal).where(models.Animal.shelter_id == current_shelter.id)
    animals = db.exec(statement).all()
    return animals


@router.post("/upload-csv")
def upload_csv(
    file: UploadFile = File(...),
    current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
    db: Session = Depends(get_session)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type")
    animals_added = create_animals_from_csv(db, file.file, current_shelter.id)
    return {"detail": f"{animals_added} animals added successfully"}


@router.get("/", response_model=List[schemas.AnimalRead])
def read_animals(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    animals = db.exec(select(models.Animal).offset(skip).limit(limit)).all()
    return animals


@router.get("/{animal_id}", response_model=schemas.AnimalRead)
def read_animal(animal_id: int, db: Session = Depends(get_session)):
    animal = db.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.post("/", response_model=schemas.AnimalRead)
def create_new_animal(
        animal: schemas.AnimalCreate,
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)
):
    new_animal = models.Animal(
        **animal.model_dump(),
        shelter_id=current_shelter.id  # Assign shelter_id here
    )
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return new_animal


@router.put("/{animal_id}", response_model=schemas.AnimalRead)
def update_existing_animal(
        animal_id: int,
        animal: schemas.AnimalUpdate,
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)
):
    db_animal = db.get(models.Animal, animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    for key, value in animal.dict(exclude_unset=True).items():
        setattr(db_animal, key, value)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


@router.delete("/{animal_id}")
def delete_existing_animal(
        animal_id: int,
        current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
        db: Session = Depends(get_session)
):
    db_animal = db.get(models.Animal, animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found or unauthorized")
    db.delete(db_animal)
    db.commit()
    return {"detail": "Animal deleted successfully"}
