from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class AnimalData(BaseModel):
    animal_type: str
    name: str
    age: int
    color: str
    months_in_shelter: int
    behavior: str
    health: str
    vaccinated: bool
    target_audience: str

app = FastAPI()
generator = AnimalDescriptionGenerator()

@app.post("/generate-description")
async def generate_description(animal_data: AnimalData, variations: int = 1):
    try:
        if variations > 1:
            descriptions = await generator.generate_multiple_descriptions(
                animal_data.dict(),
                num_variations=variations
            )
            return {"descriptions": descriptions}
        else:
            description = await generator.generate_single_description(animal_data.dict())
            file_path = generator.save_description(description, animal_data.dict())
            return {
                "description": description,
                "saved_to": file_path
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
