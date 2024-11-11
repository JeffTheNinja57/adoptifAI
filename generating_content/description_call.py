from generate_descriptions import generate_animal_description, load_animal_info

# Example usage with a CSV file
input_csv_file = "../data/test_animal_data.csv"
output_csv_file = "../data/animals_with_descriptions.csv"

# You can choose the interval of data to be processed
start_row = 2  # Process starting from the 2nd row
end_row = 5    # Process up to the 5th row

animal_info = load_animal_info(input_csv_file, start_row=start_row, end_row=end_row)

with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = list(next(iter(animal_info.values())).keys())
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row_num, animal_data in animal_info.items():
        description = generate_animal_description(animal_data)
        animal_data['description'] = description
        writer.writerow(animal_data)
        print(f"Processed row {row_num}, description: {description}")

print(f"Descriptions generated and saved to '{output_csv_file}'.")