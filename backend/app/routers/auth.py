from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.app import models, schemas, dependencies
from backend.app.database import get_session
from backend.app.crud import get_shelter_by_email, create_shelter

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", response_model=schemas.ShelterRead)
def register_shelter(shelter: schemas.ShelterCreate, db: Session = Depends(get_session)):
    existing_shelter = get_shelter_by_email(db, email=shelter.contact_email)
    if existing_shelter:
        raise HTTPException(status_code=400, detail="Email already registered")
    shelter.password = get_password_hash(shelter.password)
    new_shelter = create_shelter(db, shelter)
    return new_shelter

@router.post("/login")
def login(shelter: schemas.LoginSchema, db: Session = Depends(get_session)):
    db_shelter = get_shelter_by_email(db, email=shelter.contact_email)
    if not db_shelter or not verify_password(shelter.password, db_shelter.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generate JWT token
    access_token = dependencies.create_access_token(data={"sub": db_shelter.contact_email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/add-api-key")
def add_api_key(api_key_data: schemas.ApiKeySchema, current_shelter: models.Shelter = Depends(dependencies.get_current_shelter), db: Session = Depends(get_session)):
    current_shelter.api_key = api_key_data.api_key
    db.add(current_shelter)
    db.commit()
    db.refresh(current_shelter)
    return {"detail": "API key updated successfully"}

