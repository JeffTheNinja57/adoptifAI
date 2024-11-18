import csv
import os

import google.generativeai as genai


try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("../../../gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)


def generate_descriptions(input_csv, output_csv):
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=(
            "You are a volunteer at an animal shelter. "
            "Write a description for an animal in the shelter to help it get adopted. "
            "Make your response in one paragraph."
        ),
    )
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', newline='',
                                                                encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['description']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for animal_info in reader:
            prompt = (
                f"Write an engaging, informative description for a {animal_info['animal_type']} named {animal_info['name']}."
                f" It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months."
                f" Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}."
                f" Target audience: {animal_info['target_audience']}."
            )

            try:
                response = model.generate_content(
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=250,
                        temperature=0.7,  # Reduced temperature

                    ),
                    contents=prompt,
                )

                # Check if the response contains content
                if response.candidates and response.candidates[0].content.parts:
                    description = response.text.strip()
                else:
                    description = "Description could not be generated due to safety concerns."

            except Exception as e:
                print(f"An error occurred while generating description for {animal_info['name']}: {e}")
                description = "Description could not be generated."

            animal_info['description'] = description
            writer.writerow(animal_info)
            print(f"Processed {animal_info['name']}.")

    print(f"Descriptions generated and saved to '{output_csv}'.")


# Example usage
input_csv_file = "../../../data/test_animal_data.csv"
output_csv_file = "animals_with_descriptions.csv"

generate_descriptions(input_csv_file, output_csv_file)
