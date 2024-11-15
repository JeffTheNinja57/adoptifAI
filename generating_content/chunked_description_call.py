import csv
import time

from chunked_description_generator import generate_animal_descriptions_batch
from description_text import save_batch_descriptions


def process_animals_in_batches(input_csv_file, output_csv_file, batch_size=5, start_row=None, end_row=None):
    try:
        # Load existing descriptions (same as before)
        existing_descriptions = {}
        try:
            with open(output_csv_file, 'r', encoding='utf-8') as existing_file:
                reader = csv.DictReader(existing_file)
                for row in reader:
                    if (row.get('description') and
                            row.get('description') not in [
                                "No description generated",
                                "Description could not be generated.",
                                "Description could not be generated due to safety concerns."
                            ]):
                        existing_descriptions[int(row['row_num'])] = row['description']
        except FileNotFoundError:
            pass

        # Read and prepare animals for batch processing
        animals_to_process = []
        with open(input_csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader, 1):
                if (start_row is None or i >= start_row) and (end_row is None or i <= end_row):
                    row['row_num'] = i
                    # Only add animals that need new descriptions
                    if i not in existing_descriptions:
                        animals_to_process.append(row)
                    else:
                        row['description'] = existing_descriptions[i]

        print(f"Found {len(animals_to_process)} animals that need descriptions")

        # Process in batches
        current_batch = []
        all_processed_animals = []

        for animal in animals_to_process:
            current_batch.append(animal)

            if len(current_batch) >= batch_size:
                print(f"\nProcessing batch of {len(current_batch)} animals...")
                try:
                    # Here's where we use our batch generation!
                    descriptions = generate_animal_descriptions_batch(current_batch)

                    for batch_animal in current_batch:
                        row_num = int(batch_animal['row_num'])
                        batch_animal['description'] = descriptions.get(
                            row_num, "Description could not be generated."
                        )
                        all_processed_animals.append(batch_animal)
                        print(f"Generated description for animal {row_num}")

                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
                    for batch_animal in current_batch:
                        batch_animal['description'] = "Description could not be generated."
                        all_processed_animals.append(batch_animal)

                current_batch = []  # Clear the batch
                time.sleep(5)  # Cooldown between batches

        if current_batch:
            print(f"\nProcessing final batch of {len(current_batch)} animals...")
            try:
                descriptions = generate_animal_descriptions_batch(current_batch)

                for batch_animal in current_batch:
                    row_num = int(batch_animal['row_num'])
                    batch_animal['description'] = descriptions.get(
                        row_num, "Description could not be generated."
                    )
                    all_processed_animals.append(batch_animal)
                    print(f"Generated description for animal {row_num}")

            except Exception as e:
                print(f"Error processing final batch: {str(e)}")
                for batch_animal in current_batch:
                    batch_animal['description'] = "Description could not be generated."
                    all_processed_animals.append(batch_animal)
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = list(animals_to_process[0].keys())
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            all_animals = sorted(all_processed_animals, key=lambda x: x['row_num'])
            for animal in all_animals:
                writer.writerow(animal)

    except Exception as e:
        print(f"Critical error: {str(e)}")


if __name__ == "__main__":
    input_csv_file = "../data/test_animal_data.csv"
    output_csv_file = "../data/test_animal_data_with_descriptions.csv"

    batch_size = 5  # Process 5 animals at a time

    process_animals_in_batches(
        input_csv_file=input_csv_file,
        output_csv_file=output_csv_file,
        batch_size=batch_size
    )
