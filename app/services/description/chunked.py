import logging

from app.main import SessionDep
from generator import initialize_gemini


async def generate_descriptions_batch(session: SessionDep, animals, batch_size=5):
    """Generate descriptions for multiple animals in batches"""
    try:
        model = initialize_gemini()

        for i in range(0, len(animals), batch_size):
            batch = animals[i:i + batch_size]
            prompts = []

            for animal in batch:
                vaccinated_status = "Yes" if animal.vaccinated else "No"
                prompt = (
                    f"Animal {animal.id}: {animal.animal_type} named {animal.name}, "
                    f"{animal.age} years old, {animal.color}, "
                    f"in shelter for {animal.months_in_shelter} months. "
                    f"Behavior: {animal.behavior}, health: {animal.health}, "
                    f"vaccinated: {vaccinated_status}. "
                    f"Target audience: {animal.target_audience}."
                )
                prompts.append(prompt)

            combined_prompt = "\n\n".join(
                prompts) + "\n\nWrite a separate engaging description for each animal listed above. Label each response with the Animal ID."

            response = model.generate_content(
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=250 * len(batch),
                    temperature=0.9,
                ),
                contents=combined_prompt,
            )

            descriptions = response.text.split("\n\n")

            # Update descriptions in database
            for animal, description in zip(batch, descriptions):
                if description.strip():
                    animal.description_en = description.strip()
                    session.add(animal)

            session.commit()

    except Exception as e:
        logging.error(f"Error in batch generation: {str(e)}")
        raise
