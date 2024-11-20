from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class AnimalType(str, Enum):
    DOG = "dog"
    CAT = "cat"

class HealthStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    BAD = "bad"

class ShelterBase(SQLModel):
    name: str = Field(index=True)
    location: str
    contact_email: str = Field(index=True)
    api_key: Optional[str] = None

class Shelter(ShelterBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str  # Hashed password
    animals: List["Animal"] = Relationship(back_populates="shelter")

class AnimalBase(SQLModel):
    name: str = Field(index=True)
    animal_type: AnimalType = Field(index=True)
    age: float
    color: str
    months_in_shelter: int = Field(default=0)
    behavior: str
    health: HealthStatus
    vaccinated: bool = Field(default=False)
    target_audience: str = Field(index=True)
    description_en: Optional[str] = None
    description_nl: Optional[str] = None

class Animal(AnimalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shelter_id: Optional[int] = Field(default=None, foreign_key="shelter.id")
    shelter: Optional[Shelter] = Relationship(back_populates="animals")
