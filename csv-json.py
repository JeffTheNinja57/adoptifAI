import csv
import json


def json_to_csv(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract the list of animals from the JSON
    animals = data.get("animals", [])

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = [
            "animal_type", "name", "age", "color",
            "months_in_shelter", "behavior", "health", "vaccinated", "target_audience"
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for animal in animals:
            # Flatten the lists into comma-separated strings
            animal_data = animal.copy()
            animal_data["behavior"] = ", ".join(animal.get("behavior", []))
            # Write the row to the CSV file
            writer.writerow(animal_data)


# Convert and save JSON to CSV
json_to_csv("/Users/mihnea/_workspace_/_uni/se_project/adoptifAI/animals.json", 'animals.csv')