from typing import Optional
from pydantic import BaseModel, EmailStr
from .models import AnimalType, HealthStatus


# Shelter Schemas

class ShelterBase(BaseModel):
    name: str
    location: str
    contact_email: EmailStr


class ShelterCreate(ShelterBase):
    password: str
    api_key: Optional[str] = None


class ShelterRead(ShelterBase):
    id: int
    api_key: Optional[str] = None

    class Config:
        orm_mode = True


class ApiKeySchema(BaseModel):
    api_key: str


class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    api_key: Optional[str] = None


# Animal Schemas

class AnimalBase(BaseModel):
    name: str
    animal_type: AnimalType
    age: float
    color: str
    months_in_shelter: int = 0
    behavior: str
    health: HealthStatus
    vaccinated: bool = False
    target_audience: str


class AnimalCreate(AnimalBase):
    pass


class AnimalRead(AnimalBase):
    id: int
    shelter_id: int
    description_en: Optional[str] = None
    description_nl: Optional[str] = None

    class Config:
        orm_mode = True


class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    animal_type: Optional[AnimalType] = None
    age: Optional[float] = None
    color: Optional[str] = None
    months_in_shelter: Optional[int] = None
    behavior: Optional[str] = None
    health: Optional[HealthStatus] = None
    vaccinated: Optional[bool] = None
    target_audience: Optional[str] = None
    description_en: Optional[str] = None
    description_nl: Optional[str] = None


# Auth Schemas

class LoginSchema(BaseModel):
    contact_email: EmailStr
    password: str
