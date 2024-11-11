import csv
import os
import json
import google.generativeai as genai

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("../gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)

# Cache the Gemini model instance
gemini_model = None

def generate_animal_description(animal_info):
    global gemini_model

    if gemini_model is None:
        gemini_model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=(
                "You are a volunteer at an animal shelter. "
                "Write a description for an animal in the shelter to help it get adopted. "
                "Make your response in one paragraph."
            ),
            safety_settings=[
                genai.types.SafetySetting(
                    category=genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                ),
                genai.types.SafetySetting(
                    category=genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                ),
                genai.types.SafetySetting(
                    category=genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                ),
                genai.types.SafetySetting(
                    category=genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                )
            ]
        )

    prompt = _build_prompt(animal_info)

    try:
        response = gemini_model.generate_content(
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=250,
                temperature=0.7,  # Reduced temperature
            ),
            contents=prompt,
        )

        # Check if the response contains content
        if response.candidates and response.candidates[0].content.parts:
            description = response.candidates[0].text
        else:
            description = "Description could not be generated due to safety concerns."
    except Exception as e:
        print(f"An error occurred while generating description for row {animal_info['row_num']}: {e}")
        description = "Description could not be generated."

    return description

def _build_prompt(animal_info):
    return (
        f"Write an engaging, informative description for a {animal_info['animal_type']} in row {animal_info['row_num']}."
        f" It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months."
        f" Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}."
        f" Target audience: {animal_info['target_audience']}."
    )

def load_animal_info(data_source, start_row=None, end_row=None):
    if isinstance(data_source, str):
        # Assume the data_source is a CSV file path
        animal_info = {}
        with open(data_source, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row_num, row in enumerate(reader, start=1):
                if start_row is not None and row_num < start_row:
                    continue
                if end_row is not None and row_num > end_row:
                    break
                row['row_num'] = row_num
                animal_info[row_num] = row
        return animal_info
    elif isinstance(data_source, dict):
        # Assume the data_source is a JSON-like dictionary
        for row_num, row in enumerate(data_source.values(), start=1):
            row['row_num'] = row_num
        return data_source
    else:
        raise ValueError("Invalid data source format. Please provide a CSV file path or a dictionary.")