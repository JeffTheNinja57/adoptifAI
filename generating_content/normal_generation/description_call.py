import csv

from descrpition_generator import generate_animal_description


def process_animals(input_csv_file, output_csv_file, start_row=None, end_row=None):
    try:
        # Read input CSV
        animals = []
        with open(input_csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader, 1):
                if (start_row is None or i >= start_row) and (end_row is None or i <= end_row):
                    row['row_num'] = i
                    animals.append(row)

        # Process each animal and write to output
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = list(animals[0].keys()) + ['description']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for animal in animals:
                try:
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
    input_csv_file = "../../data/animals.csv"
    output_csv_file = "../../data/animals_with_descriptions.csv"

    start_row = None
    end_row = None

    process_animals(input_csv_file, output_csv_file, start_row, end_row)
