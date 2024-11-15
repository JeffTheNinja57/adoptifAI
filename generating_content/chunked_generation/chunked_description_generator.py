import logging
import os

import google.generativeai as genai

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("../../gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = None


def generate_animal_descriptions_batch(animal_batch):
    """Generate descriptions for a batch of animals."""
    global gemini_model
    try:
        if gemini_model is None:
            gemini_model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=(
                    "You are a volunteer at an animal shelter. "
                    "Write descriptions for animals in the shelter to help them get adopted. "
                    "Make each response in one paragraph."
                    "Make each paragraph maximum 250 tokens."
                    "Start each paragraph with the Animal number like /n/nAnimal 1: "
                )
            )

        prompts = []
        for animal in animal_batch:
            prompt = (
                f"Animal {animal['row_num']}: {animal['animal_type']} named {animal['name']}, "
                f"{animal['age']} years old, {animal['color']}, in shelter for {animal['months_in_shelter']} months. "
                f"Behavior: {animal['behavior']}, health: {animal['health']}, vaccinated: {animal['vaccinated']}. "
                f"Target audience: {animal['target_audience']}."
            )
            prompts.append(prompt)

        combined_prompt = "\n\n".join(
            prompts) + "\n\nWrite a separate engaging, informative description for each animal listed above. Label each response with the row number."
        print(combined_prompt)
        response = gemini_model.generate_content(
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=220 * len(animal_batch),
                temperature=0.9,
            ),
            contents=combined_prompt,
        )

        # Parse the batch response
        if not response.text:
            raise Exception("No response generated")

        return response.text

    except Exception as e:
        logging.error(f"Error generating batch descriptions: {str(e)}")
        raise


def generate_animal_description(animal_info):
    """Wrapper for single animal description generation"""
    try:
        descriptions = generate_animal_descriptions_batch([animal_info])
        return descriptions.get(int(animal_info['row_num']), "Description could not be generated.")
    except Exception as e:
        logging.error(f"Error in single description generation: {str(e)}")
        return "Description could not be generated."
