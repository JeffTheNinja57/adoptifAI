import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv


def initialize_gemini(api_key):
    """Initialize Gemini API and model."""
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=(
                "You are a volunteer at an animal shelter. "
                "Write descriptions for animals in the shelter to help them get adopted. "
                "Make each response engaging and informative in one paragraph. "
                "Maximum 250 tokens per description."
            )
        )
    except Exception as e:
        logging.error(f"Error initializing Gemini: {str(e)}")
        raise


async def generate_description(animal, api_key):
    """Generate description for a single animal"""
    try:
        model = initialize_gemini(api_key)

        # Create prompt
        vaccinated_status = "Yes" if animal.vaccinated else "No"
        prompt = (
            f"{animal.animal_type} named {animal.name}, "
            f"{animal.age} years old, {animal.color}, "
            f"in shelter for {animal.months_in_shelter} months. "
            f"Behavior: {animal.behavior}, health: {animal.health}, "
            f"vaccinated: {vaccinated_status}. "
            f"Target audience: {animal.target_audience}. "
            f"Write an engaging, informative description to help this animal get adopted."
        )

        response = model.generate_content(
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=250,
                temperature=0.9,
            ),
            contents=prompt,
        )

        if not response.text:
            raise Exception("No description generated")

        return response.text.strip()

    except Exception as e:
        logging.error(f"Error generating description: {str(e)}")
        raise