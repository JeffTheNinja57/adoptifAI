from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select

from app.core.security import get_api_key
from app.main import SessionDep
from app.models.models import (
    Animal, AnimalCreate, AnimalUpdate, AnimalResponse,
    AnimalType, HealthStatus, Shelter
)
from app.services.description.generator import generate_description

router = APIRouter()


# List Animals Endpoint
@router.get("/", response_model=List[AnimalResponse])
async def list_animals(
        session: SessionDep,
        shelter_id: Optional[int] = None,
        animal_type: Optional[AnimalType] = None,
        min_age: Optional[float] = None,
        max_age: Optional[float] = None,
        health: Optional[HealthStatus] = None,
        target_audience: Optional[str] = None,
        offset: int = 0,
        limit: int = Query(default=20, le=100),
):
    query = select(Animal)
    if shelter_id:
        query = query.where(Animal.shelter_id == shelter_id)
    if animal_type:
        query = query.where(Animal.animal_type == animal_type)
    if min_age is not None:
        query = query.where(Animal.age >= min_age)
    if max_age is not None:
        query = query.where(Animal.age <= max_age)
    if health:
        query = query.where(Animal.health == health)
    if target_audience:
        query = query.where(Animal.target_audience.contains(target_audience))

    animals = session.exec(query.offset(offset).limit(limit)).all()
    return animals


# Create Animal Endpoint
@router.post("/", response_model=AnimalResponse)
async def create_animal(
        animal: AnimalCreate,
        session: SessionDep,
        shelter: Shelter = Depends(get_api_key),
        generate_desc: bool = Query(True)
):
    db_animal = Animal.model_validate(animal)
    db_animal.shelter_id = shelter.id

    if generate_desc:
        try:
            description = await generate_description(db_animal)
            db_animal.description_en = description
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate description: {str(e)}")

    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal


# List Shelter Animals Endpoint
@router.get("/shelter", response_model=List[AnimalResponse])
async def list_shelter_animals(
        session: SessionDep,
        shelter: Shelter = Depends(get_api_key),
        offset: int = 0,
        limit: int = Query(default=20, le=100),
):
    query = select(Animal).where(Animal.shelter_id == shelter.id)
    animals = session.exec(query.offset(offset).limit(limit)).all()
    return animals


# Update Animal Endpoint
@router.patch("/{animal_id}", response_model=AnimalResponse)
async def update_animal(
        animal_id: int,
        animal: AnimalUpdate,
        session: SessionDep,
        shelter: Shelter = Depends(get_api_key)
):
    db_animal = session.get(Animal, animal_id)
    if not db_animal or db_animal.shelter_id != shelter.id:
        raise HTTPException(status_code=404, detail="Animal not found")

    animal_data = animal.model_dump(exclude_unset=True)
    for key, value in animal_data.items():
        setattr(db_animal, key, value)

    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal


# Generate Animal Description Endpoint
@router.post("/{animal_id}/generate-description")
async def generate_animal_description(
        animal_id: int,
        session: SessionDep,
        shelter: Shelter = Depends(get_api_key)
):
    # Fetch the animal from the database
    animal = session.get(Animal, animal_id)

    # Check if the animal exists and belongs to the requesting shelter
    if not animal or animal.shelter_id != shelter.id:
        raise HTTPException(status_code=404, detail="Animal not found")

    try:
        description = await generate_description(animal)
        animal.description_en = description

        # Save the updated animal to the database
        session.add(animal)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate description: {str(e)}")

    return {"success": True, "description": animal.description_en}


# Delete Animal Endpoint
@router.delete("/{animal_id}")
async def delete_animal(
        animal_id: int,
        session: SessionDep,
        shelter: Shelter = Depends(get_api_key)
):
    db_animal = session.get(Animal, animal_id)
    if not db_animal or db_animal.shelter_id != shelter.id:
        raise HTTPException(status_code=404, detail="Animal not found")

    session.delete(db_animal)
    session.commit()
    return {"message": "Animal deleted successfully"}
