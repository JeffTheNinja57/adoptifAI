from sqlalchemy.orm import Session
from backend.app import models, schemas

# Shelter CRUD

def get_shelter_by_email(db: Session, email: str):
    return db.query(models.Shelter).filter(models.Shelter.contact_email == email).first()

def create_shelter(db: Session, shelter: schemas.ShelterCreate):
    db_shelter = models.Shelter(
        name=shelter.name,
        location=shelter.location,
        contact_email=shelter.contact_email,
        password=shelter.password,
        api_key=shelter.api_key
    )
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

def update_shelter(db: Session, db_shelter: models.Shelter, shelter_update: schemas.ShelterUpdate):
    for key, value in shelter_update.dict(exclude_unset=True).items():
        setattr(db_shelter, key, value)
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

# Animal CRUD

def get_animal_by_id(db: Session, animal_id: int):
    return db.query(models.Animal).filter(models.Animal.id == animal_id).first()

def get_animals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Animal).offset(skip).limit(limit).all()

def create_animal(db: Session, animal: schemas.AnimalCreate):
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def update_animal(db: Session, db_animal: models.Animal, animal_update: schemas.AnimalUpdate):
    for key, value in animal_update.dict(exclude_unset=True).items():
        setattr(db_animal, key, value)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def delete_animal(db: Session, db_animal: models.Animal):
    db.delete(db_animal)
    db.commit()

def create_animals_from_csv(db: Session, file, shelter_id: int):
    import csv
    reader = csv.DictReader(file)
    animals_added = 0
    for row in reader:
        animal_data = schemas.AnimalCreate(**row)
        animal_data.shelter_id = shelter_id
        create_animal(db, animal_data)
        animals_added += 1
    return animals_added
