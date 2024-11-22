from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas, dependencies
from ..database import get_session
from ..crud import get_shelter_by_email, create_shelter

router = APIRouter()

# Initialize the password context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

@router.post("/register", response_model=schemas.ShelterRead)
def register_shelter(
    shelter: schemas.ShelterCreate,
    db: Session = Depends(get_session)
):
    """Register a new shelter."""
    existing_shelter = get_shelter_by_email(db, email=shelter.contact_email)
    if existing_shelter:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(shelter.password)
    shelter.password = hashed_password
    new_shelter = create_shelter(db, shelter)
    return new_shelter

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """Authenticate a shelter and return a JWT token."""
    db_shelter = get_shelter_by_email(db, email=form_data.username)
    if not db_shelter or not verify_password(form_data.password, db_shelter.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = dependencies.create_access_token(data={"sub": db_shelter.contact_email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/add-api-key")
def add_api_key(
    api_key_data: schemas.ApiKeySchema,
    current_shelter: models.Shelter = Depends(dependencies.get_current_shelter),
    db: Session = Depends(get_session)
):
    """Add or update the API key for the current shelter."""
    current_shelter.api_key = api_key_data.api_key
    db.add(current_shelter)
    db.commit()
    db.refresh(current_shelter)
    return {"detail": "API key updated successfully"}
