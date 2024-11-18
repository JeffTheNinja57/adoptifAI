import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

import google.generativeai as genai


class AnimalDescriptionGenerator:
    def __init__(self, api_key_path: Optional[str] = None):
        """Initialize the generator with API key."""
        self.model = None
        self._setup_api(api_key_path)

    def _setup_api(self, api_key_path: Optional[str] = None):
        """Setup Gemini API with key from environment or file."""
        try:
            if "GEMINI_API_KEY" in os.environ:
                api_key = os.environ["GEMINI_API_KEY"]
            elif api_key_path:
                with open(os.path.abspath(api_key_path), "r") as file:
                    api_key = file.read().strip()
            else:
                raise ValueError("No API key provided")

            genai.configure(api_key=api_key)
        except Exception as e:
            logging.error(f"Failed to setup API: {str(e)}")
            raise

    def _initialize_model(self):
        """Initialize the Gemini model if not already initialized."""
        if self.model is None:
            self.model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=(
                    "You are a volunteer at an animal shelter. "
                    "Write descriptions for animals in the shelter to help them get adopted. "
                    "Make each response in one paragraph."
                    "Make each paragraph maximum 250 tokens."
                )
            )

    def _create_animal_prompt(self, animal_data: Dict[str, str]) -> str:
        """Create a prompt for a single animal."""
        return (
            f"Animal details: {animal_data['animal_type']} named {animal_data['name']}, "
            f"{animal_data['age']} years old, {animal_data['color']}, "
            f"in shelter for {animal_data['months_in_shelter']} months. "
            f"Behavior: {animal_data['behavior']}, health: {animal_data['health']}, "
            f"vaccinated: {animal_data['vaccinated']}. "
            f"Target audience: {animal_data['target_audience']}."
        )

    async def generate_single_description(self, animal_data: Dict[str, str]) -> str:
        """Generate a single description for web interface."""
        try:
            self._initialize_model()
            prompt = self._create_animal_prompt(animal_data)

            response = await self.model.generate_content_async(
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=220,
                    temperature=0.9,
                    candidate_count=1,  # Set to 3 if you want multiple options
                ),
                contents=prompt
            )

            if not response.text:
                raise Exception("No description generated")

            return response.text

        except Exception as e:
            logging.error(f"Error generating description: {str(e)}")
            raise

    async def generate_multiple_descriptions(self, animal_data: Dict[str, str], num_variations: int = 3) -> List[str]:
        """Generate multiple description variations for the same animal."""
        try:
            self._initialize_model()
            prompt = self._create_animal_prompt(animal_data)
            prompt += f"\n\nPlease provide {num_variations} different description variations."

            response = await self.model.generate_content_async(
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=220 * num_variations,
                    temperature=0.9,
                    candidate_count=num_variations,
                ),
                contents=prompt
            )

            if not response.text:
                raise Exception("No descriptions generated")

            return [candidate.text for candidate in response.candidates]

        except Exception as e:
            logging.error(f"Error generating descriptions: {str(e)}")
            raise

    def save_description(self, description: str, animal_data: Dict[str, str],
                         output_dir: str = "../full_data/descriptions") -> str:
        """Save a single description to a file."""
        try:
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{animal_data['name']}_{timestamp}.txt"
            file_path = os.path.join(output_dir, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Description for {animal_data['name']} - Generated at {timestamp}\n")
                f.write("=" * 80 + "\n\n")
                f.write("Animal Details:\n")
                for key, value in animal_data.items():
                    f.write(f"{key}: {value}\n")
                f.write("\nGenerated Description:\n")
                f.write("=" * 80 + "\n")
                f.write(description)

            return file_path

        except Exception as e:
            logging.error(f"Error saving description: {str(e)}")
            raise
