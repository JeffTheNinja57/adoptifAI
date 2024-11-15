import os

def save_batch_descriptions(descriptions, batch_number, output_file="../full_data/all_descriptions.txt"):
    """Save batch descriptions to a single text file, appending new batches."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Append the batch to the file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"Batch {batch_number}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(descriptions)
            f.write("\n\n")

        return output_file
    except Exception as e:
        print(f"Error saving descriptions: {str(e)}")
        raise