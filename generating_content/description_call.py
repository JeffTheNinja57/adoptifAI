import csv

from descrpition_generator import generate_animal_description


def process_animals(input_csv_file, output_csv_file, start_row=None, end_row=None):
    try:
        # First, load any existing descriptions from output file
        existing_descriptions = {}
        try:
            with open(output_csv_file, 'r', encoding='utf-8') as existing_file:
                reader = csv.DictReader(existing_file)
                for row in reader:
                    if (row.get('description') and
                        row.get('description') != "No description generated" and
                        row.get('description') != "Description could not be generated." and
                        row.get('description') != "Description could not be generated due to safety concerns."):
                        existing_descriptions[int(row['row_num'])] = row['description']
        except FileNotFoundError:
            pass  # Output file doesn't exist yet, that's OK

        # Read input CSV
        animals = []
        with open(input_csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader, 1):
                if (start_row is None or i >= start_row) and (end_row is None or i <= end_row):
                    row['row_num'] = i
                    # If we have an existing valid description, use it
                    if i in existing_descriptions:
                        row['description'] = existing_descriptions[i]
                    animals.append(row)

        # Process each animal and write to output
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = list(animals[0].keys()) + ([] if 'description' in animals[0] else ['description'])
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for animal in animals:
                try:
                    # Skip if we already have a valid description
                    if ('description' in animal and
                        animal['description'] and
                        animal['description'] != "No description generated" and
                        animal['description'] != "Description could not be generated." and
                        animal['description'] != "Description could not be generated due to safety concerns."):
                        print(f"Skipping row {animal['row_num']} - description exists")
                        writer.writerow(animal)
                        continue

                    description = generate_animal_description(animal)
                    animal['description'] = description
                    writer.writerow(animal)
                    print(f"Processed row {animal['row_num']}")
                except Exception as e:
                    print(f"Error processing row {animal['row_num']}: {str(e)}")
                    continue

    except Exception as e:
        print(f"Critical error: {str(e)}")


if __name__ == "__main__":
    input_csv_file = "../data/animals.csv"
    output_csv_file = "../data/animals_with_descriptions.csv"

    start_row = None
    end_row = None

    process_animals(input_csv_file, output_csv_file, start_row, end_row)
