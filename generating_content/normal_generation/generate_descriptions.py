import csv
import os

import google.generativeai as genai

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("../../gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)


def generate_descriptions(input_csv, output_csv):
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are a volunteer at an animal shelter. Write a description for an animal in the shelter to help it get adopted. Make your response in one paragraph.",
    )
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', newline='',encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['description']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for animal_info in reader:
            # model = genai.GenerativeModel(
            #     "gemini-1.5-flash",
            #     system_instruction="You are a volunteer at an animal shelter. Write a description for an animal in the shelter to help it get adopted.",
            # )
            response = model.generate_content(
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=250,
                    temperature=1.25,
                ),
                contents=f"Write an engaging, informative description for a {animal_info['animal_type']} named {animal_info['name']}. It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months. Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}. Target audience: {animal_info['target_audience']}.",
            )
            # response = response.text
            animal_info['description'] = response
            writer.writerow(animal_info)
            print(f"Generated description for {animal_info['name']}.")
    print(f"Descriptions generated and saved to '{output_csv}'.")


input_csv_file = "../../data/test_animal_data.csv"

output_csv_file = "animals_with_descriptions.csv"

if not os.path.exists(output_csv_file):
    with open(output_csv_file, 'w') as f:
        pass

generate_descriptions(input_csv_file, output_csv_file)
