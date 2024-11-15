import os


def save_batch_descriptions(descriptions, batch_number, output_dir="../full_data/descriptions"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save as formatted text file
    filename = f"batch_{batch_number}.txt"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"Batch {batch_number}")
        f.write("\n\n")
        f.write(descriptions)

    return file_path
