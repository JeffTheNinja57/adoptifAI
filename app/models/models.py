from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


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
    __tablename__ = "shelters"

    id: Optional[int] = Field(default=None, primary_key=True)
    api_key: str = Field(index=True)

    # Relationships
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
    shelter_id: Optional[int] = Field(default=None, foreign_key="shelters.id")


class Animal(AnimalBase, table=True):
    __tablename__ = "animals"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship
    shelter: Optional[Shelter] = Relationship(back_populates="animals")


class AnimalCreate(SQLModel):
    name: str
    animal_type: AnimalType
    age: float
    color: str
    behavior: str
    health: HealthStatus
    vaccinated: bool
    target_audience: str


class AnimalUpdate(SQLModel):
    name: Optional[str] = None
    animal_type: Optional[AnimalType] = None
    age: Optional[float] = None
    color: Optional[str] = None
    months_in_shelter: Optional[int] = None
    behavior: Optional[str] = None
    health: Optional[HealthStatus] = None
    vaccinated: Optional[bool] = None
    target_audience: Optional[str] = None


class ShelterResponse(ShelterBase):
    id: int
    animal_count: Optional[int] = None


class AnimalResponse(AnimalBase):
    id: int
    description_en: Optional[str] = None
    description_nl: Optional[str] = None
    shelter: ShelterResponse
