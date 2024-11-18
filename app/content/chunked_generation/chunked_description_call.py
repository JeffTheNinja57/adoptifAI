import csv
import time
import logging

from chunked_description_generator import generate_animal_descriptions_batch, initialize_gemini
from description_text import save_batch_descriptions


def load_animals_from_csv(input_csv_file, parse_start=None, parse_end=None):
    """
    Load animals from CSV file within specified range.

    Args:
        input_csv_file (str): Path to CSV file
        parse_start (int): Starting row number (1-based indexing)
        parse_end (int): Ending row number (inclusive)
    """
    try:
        animals = []
        with open(input_csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader, 1):  # 1-based indexing
                # Skip rows before parse_start
                if parse_start and i < parse_start:
                    continue
                # Stop after parse_end
                if parse_end and i > parse_end:
                    break

                row['row_num'] = i
                animals.append(row)

        return animals
    except Exception as e:
        logging.error(f"Error loading animals from CSV: {str(e)}")
        raise


def process_animals_in_batches(input_csv_file, batch_size=5, parse_start=None, parse_end=None):
    """
    Main function to process animals in batches within specified range.

    Args:
        input_csv_file (str): Path to CSV file
        batch_size (int): Number of animals to process in each batch
        parse_start (int): Starting row number (1-based indexing)
        parse_end (int): Ending row number (inclusive)
    """
    try:
        # Load animals from CSV within range
        print(f"Loading animals from CSV (Range: {parse_start or 'start'} to {parse_end or 'end'})...")
        animals = load_animals_from_csv(input_csv_file, parse_start, parse_end)
        print(f"Loaded {len(animals)} animals")

        if not animals:
            print("No animals to process in specified range")
            return

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
                    file_path = save_batch_descriptions(descriptions, batch_number, "content/full_data/all_descriptions.txt")
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
    input_csv_file = "../../../data/animals.csv"
    batch_size = 25

    # Define processing range
    parse_start = 51  # Start from first animal (optional, default is start of file)
    # parse_end = 50  # Stop after 50th animal (optional, default is end of file)

    process_animals_in_batches(
        input_csv_file=input_csv_file,
        batch_size=batch_size,
        parse_start=parse_start,
        # parse_end=parse_end
    )