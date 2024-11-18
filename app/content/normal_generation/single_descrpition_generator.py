import logging
import os
from datetime import datetime

import google.generativeai as genai

# Set up logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = os.path.join(log_directory, f"generation_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("../../../gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)

# Cache the Gemini model instance
gemini_model = None


def generate_animal_description(animal_info):
    """Generate a description for a single animal."""
    global gemini_model
    try:
        if gemini_model is None:
            gemini_model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=(
                    "You are a volunteer at an animal shelter. "
                    "Write a description for an animal in the shelter to help it get adopted. "
                    "Make your response in one paragraph."
                )
            )

        prompt = (
            f"Write an engaging, informative description for a {animal_info['animal_type']} named {animal_info['name']}."
            f" It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months."
            f" Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}."
            f" Target audience: {animal_info['target_audience']}."
        )

        response = gemini_model.generate_content(
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=250,
                temperature=0.9,
            ),
            contents=prompt,
        )

        # Extract just the text content from the response
        if response.parts:
            description = response.text.strip()
            print(description)
            # logging.info(f"Successfully generated description for {animal_info.get('name', 'unknown animal')}")
            return description
        else:
            logging.warning(f"No valid response for {animal_info.get('name', 'unknown animal')}")
            description = "No description generated"
            return description

    except Exception as e:
        logging.error(f"Error generating description for {animal_info.get('name', 'unknown animal')}: {str(e)}")
        return "Description could not be generated."
