import csv
import os

import google.generativeai as genai

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("/Users/mihnea/_workspace_/_uni/se_project/adoptifAI/gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)


def generate_descriptions(input_csv, output_csv):
    model = genai.GenerativeModel("gemini-1.5-flash")
    with open(input_csv, 'r', encoding='utf-8') as infile, \
            open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['description']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for animal_info in reader:
            say = f"Write an engaging, informative description for a {animal_info['animal_type']} named {animal_info['name']}. It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months. Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}. Target audience: {animal_info['target_audience']}."
            response = model.generate_content(
                "Tell me a story about a magic backpack.",
                generation_config=genai.types.GenerationConfig(
                    say,
                    max_output_tokens=400,
                    temperature=1.0,
                ),
            )

            animal_info['description'] = response
            writer.writerow(animal_info)

    print(f"Descriptions generated and saved to '{output_csv}'.")


# Example usage:
input_csv_file = "/Users/mihnea/_workspace_/_uni/se_project/adoptifAI/data/test_animal_data.csv"

output_csv_file = "animals_with_descriptions.csv"

if not os.path.exists(output_csv_file):
    with open(output_csv_file, 'w') as f:
        pass

generate_descriptions(input_csv_file, output_csv_file)
