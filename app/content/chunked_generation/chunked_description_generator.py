import logging
import os

import google.generativeai as genai


def initialize_gemini():
    """Initialize Gemini API and model."""
    try:
        GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    except KeyError:
        with open(os.path.abspath("../../../gemini_key.txt"), "r") as file:
            GEMINI_API_KEY = file.read().strip()

    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=(
            "You are a volunteer at an animal shelter. "
            "Write descriptions for animals in the shelter to help them get adopted. "
            "Make each response in one paragraph."
            "Make each paragraph maximum 250 tokens."
            "Start each paragraph with the Animal number like /n/nAnimal 1: "
        )
    )


def generate_animal_descriptions_batch(animal_batch, model=None):
    """Generate descriptions for a batch of animals."""
    try:
        # Initialize model if not provided
        if model is None:
            model = initialize_gemini()

        # Create prompts for each animal
        prompts = []
        for animal in animal_batch:
            # Convert boolean to Yes/No for vaccinated status
            vaccinated_status = "Yes" if str(animal['vaccinated']).lower() == 'true' else "No"
            prompt = (
                f"Animal {animal['row_num']}: {animal['animal_type']} named {animal['name']}, "
                f"{animal['age']} years old, {animal['color']}, in shelter for {animal['months_in_shelter']} months. "
                f"Behavior: {animal['behavior']}, health: {animal['health']}, vaccinated: {vaccinated_status}. "
                f"Target audience: {animal['target_audience']}."
            )
            prompts.append(prompt)

        combined_prompt = "\n\n".join(
            prompts) + "\n\nWrite a separate engaging, informative description for each animal listed above. Label each response with the row number."

        response = model.generate_content(
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=220 * len(animal_batch),
                temperature=0.9,
            ),
            contents=combined_prompt,
        )

        if not response.text:
            raise Exception("No response generated")

        return response.text

    except Exception as e:
        logging.error(f"Error generating batch descriptions: {str(e)}")
        raise
