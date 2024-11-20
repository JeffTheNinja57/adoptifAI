import csv
import secrets
from io import StringIO
from typing import List

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlmodel import select

from app.core.security import get_api_key
from app.main import SessionDep
from app.models.models import (
    Shelter, ShelterBase, ShelterResponse,
    Animal, AnimalType, HealthStatus
)

router = APIRouter()


# Register Shelter Endpoint
@router.post("/register")
async def register_shelter(
        shelter: ShelterBase,
        session: SessionDep
):
    """Register a new shelter"""
    db_shelter = Shelter(
        name=shelter.name,
        location=shelter.location,
        contact_email=shelter.contact_email,
        api_key=secrets.token_urlsafe(32)
    )
    session.add(db_shelter)
    session.commit()
    session.refresh(db_shelter)

    # Return with API key (only shown once)
    return {
        "shelter_id": db_shelter.id,
        "api_key": db_shelter.api_key,
        "message": "Save your API key - it won't be shown again!"
    }


# Import Animals from CSV Endpoint
@router.post("/import-animals")
async def import_animals_csv(
        session: SessionDep,
        file: UploadFile = File(...),
        shelter: Shelter = Depends(get_api_key)
):
    """Import animals from CSV file"""
    content = await file.read()
    csv_data = StringIO(content.decode())
    animals_to_add = []
    csv_reader = csv.DictReader(csv_data)

    for row in csv_reader:
        try:
            animal = Animal(
                shelter_id=shelter.id,
                name=row['name'],
                animal_type=AnimalType(row['animal_type'].lower()),
                age=float(row['age']),
                color=row['color'],
                months_in_shelter=int(row['months_in_shelter']),
                behavior=row['behavior'],
                health=HealthStatus(row['health'].lower()),
                vaccinated=row['vaccinated'].lower() == 'true',
                target_audience=row['target_audience']
            )
            animals_to_add.append(animal)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")

    session.add_all(animals_to_add)
    session.commit()

    return {
        "message": f"Successfully imported {len(animals_to_add)} animals",
        "shelter_id": shelter.id
    }


@router.post("/", response_model=ShelterResponse)
async def create_shelter(
        shelter: ShelterBase,
        session: SessionDep
):
    """Create a new shelter and generate API key"""
    db_shelter = Shelter.model_validate(shelter)
    db_shelter.api_key = secrets.token_urlsafe(32)

    session.add(db_shelter)
    session.commit()
    session.refresh(db_shelter)

    # Return shelter info with API key (only shown once)
    return {
        **db_shelter.model_dump(exclude={"api_key"}),
        "api_key": db_shelter.api_key  # Include API key in creation response
    }


@router.get("/", response_model=List[ShelterResponse])
async def list_shelters(
        session: SessionDep,
        skip: int = 0,
        limit: int = 100
):
    """List all shelters (public info only)"""
    query = select(Shelter).offset(int(skip)).limit(int(limit))
    shelters = session.exec(query).all()

    # Add animal count to each shelter
    for shelter in shelters:
        shelter.animal_count = len(shelter.animals)

    return shelters


@router.get("/me", response_model=ShelterResponse)
async def get_current_shelter(
        session: SessionDep = Depends(SessionDep),
        shelter: Shelter = Depends(get_api_key)
):
    """Get current shelter based on API key"""
    shelter.animal_count = len(shelter.animals)
    return shelter


@router.post("/import-descriptions")
async def import_descriptions_csv(
        file: UploadFile = File(...),
        session: SessionDep = None,
        shelter: Shelter = Depends(get_api_key)
):
    """Import descriptions from CSV file"""
    content = await file.read()
    csv_data = StringIO(content.decode())

    updated_count = 0
    csv_reader = csv.DictReader(csv_data)

    for row in csv_reader:
        animal = session.exec(
            select(Animal)
            .where(Animal.id == int(row['animal_id']))
            .where(Animal.shelter_id == shelter.id)
        ).first()

        if animal:
            animal.description_en = row['description']
            session.add(animal)
            updated_count += 1

    session.commit()

    return {
        "message": f"Successfully updated {updated_count} descriptions",
        "shelter_id": shelter.id
    }
