import csv
import os

import google.generativeai as genai

# # Set Gemini API key
# with open(os.path.abspath("gemini_key.txt"), "r") as file:
#     GEMINI_API_KEY = file.read().strip()
#
# genai.configure(api_key=os.environ["gemini_key.txt"])

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    with open(os.path.abspath("gemini_key.txt"), "r") as file:
        GEMINI_API_KEY = file.read().strip()

genai.configure(api_key=GEMINI_API_KEY)


# Import the Python SDK


# import pandas as pd
# import requests
#
# with open(os.path.abspath("gemini_key.txt"), "r") as file:
#     GEMINI_API_KEY = file.read().strip()
#
#
# def generate_description(animal_info):
#
#     prompt = (
#         f"Write an engaging, informative description for a {animal_info['animal_type']} named "
#         f"{animal_info['name']}. It is {animal_info['age']} years old, {animal_info['color']}, and "
#         f"has been in the shelter for {animal_info['months_in_shelter']} months. Its behavior is "
#         f"{animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: "
#         f"{animal_info['vaccinated']}. Target audience: {animal_info['target_audience']}."
#     )
#
#     headers = {
#         "Authorization": f"Bearer {os.environ.get('GEMINI_API_KEY')}",
#         "Content-Type": "application/json",
#     }
#
#     data = {
#         "prompt": prompt,
#         "temperature": 0.7,  # Adjust temperature for creativity vs. informativeness
#         "max_tokens": 200,  # Adjust max_tokens for desired description length
#     }
#
#     response = requests.post("https://api.palm.google.com/v1/generateText", headers=headers, json=data)
#     return response.json()["text"]
#
#
# df = pd.read_csv("animals.csv")
#
# # Create a new column to store the descriptions
# df['description'] = ""
#
# # Iterate through each row of the DataFrame and generate a description
# for index, row in df.iterrows():
#     description = generate_description(row)
#     df.at[index, 'description'] = description
#
# # Save the modified DataFrame back to the CSV file
# df.to_csv("animals_with_descriptions.csv", index=False)
#


def generate_descriptions(input_csv, output_csv):
    model = genai.GenerativeModel("gemini-pro"),  # Or a suitable Gemini model
    temperature = 0.5  # Adjust temperature as needed
    with open(input_csv, 'r', encoding='utf-8') as infile, \
            open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['description']  # Add 'description' column
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for animal_info in reader:
            prompt = f"Write an engaging, informative description for a {animal_info['animal_type']} named {animal_info['name']}. It is {animal_info['age']} years old, {animal_info['color']}, and has been in the shelter for {animal_info['months_in_shelter']} months. Its behavior is {animal_info['behavior']}, its health is {animal_info['health']}, and it is vaccinated: {animal_info['vaccinated']}. Target audience: {animal_info['target_audience']}."

            response = model.generate_content(prompt)

            animal_info['description'] = response
            writer.writerow(animal_info)

    print(f"Descriptions generated and saved to '{output_csv}'.")


# Example usage:
input_csv_file = "test_animal_data.csv"  # Replace with your input CSV filename
output_csv_file = "animals_with_descriptions.csv"  # Output filename
generate_descriptions(input_csv_file, output_csv_file)
