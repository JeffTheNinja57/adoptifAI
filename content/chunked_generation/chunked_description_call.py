import csv
import time
import logging

from chunked_description_generator import generate_animal_descriptions_batch, initialize_gemini
from description_text import save_batch_descriptions

def load_animals_from_csv(input_csv_file, start_row=None, end_row=None):
    try:
        animals = []
        with open(input_csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader, 1):
                if (start_row is None or i >= start_row) and (end_row is None or i <= end_row):
                    row['row_num'] = i
                    animals.append(row)
        return animals
    except Exception as e:
        logging.error(f"Error loading animals from CSV: {str(e)}")
        raise


def process_animals_in_batches(input_csv_file, batch_size=5, start_row=None, end_row=None):
    """Main function to process animals in batches."""
    try:
        # Load animals from CSV
        print("Loading animals from CSV...")
        animals = load_animals_from_csv(input_csv_file, start_row, end_row)
        print(f"Loaded {len(animals)} animals")

        # Initialize Gemini model once
        model = initialize_gemini()

        # Process in batches
        current_batch = []
        batch_number = 1

        for i, animal in enumerate(animals):
            current_batch.append(animal)

            if len(current_batch) >= batch_size or i == len(animals) - 1:
                print(f"\nProcessing batch {batch_number} ({len(current_batch)} animals)...")
                try:
                    # Generate descriptions
                    descriptions = generate_animal_descriptions_batch(current_batch, model)

                    # Save to file
                    file_path = save_batch_descriptions(descriptions, batch_number)
                    print(f"Saved descriptions to: {file_path}")

                    current_batch = []
                    batch_number += 1

                    # Add cooldown between batches (except for last batch)
                    if i < len(animals) - 1:
                        print("Cooling down for 5 seconds...")
                        time.sleep(5)

                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
                    current_batch = []

    except Exception as e:
        print(f"Critical error: {str(e)}")


if __name__ == "__main__":
    input_csv_file = "../../data/test_animal_data.csv"
    batch_size = 5

    process_animals_in_batches(
        input_csv_file=input_csv_file,
        batch_size=batch_size
    )