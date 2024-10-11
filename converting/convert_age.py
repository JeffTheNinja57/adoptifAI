import csv


def transform_age(csv_input_path, csv_output_path):
    with open(csv_input_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Open the output CSV file
        with open(csv_output_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Transform the 'age' field to an integer by removing 'years' or 'year' and converting
                age_str = row['age']
                age_str = age_str.replace(' years', '').replace(' year', '').strip()
                row['age'] = int(age_str)

                # Transform the 'years_in_shelter' field to an integer (in months)
                shelter_str = row['years_in_shelter']
                if 'years' in shelter_str:
                    shelter_str = shelter_str.replace(' years', '').strip()
                    row['years_in_shelter'] = int(shelter_str) * 12
                elif 'year' in shelter_str:
                    shelter_str = shelter_str.replace(' year', '').strip()
                    row['years_in_shelter'] = int(shelter_str) * 12
                elif 'months' in shelter_str:
                    shelter_str = shelter_str.replace(' months', '').strip()
                    row['years_in_shelter'] = int(shelter_str)
                elif 'month' in shelter_str:
                    shelter_str = shelter_str.replace(' month', '').strip()
                    row['years_in_shelter'] = int(shelter_str)

                writer.writerow(row)


# Usage
transform_age('../animals.csv', 'animals.csv')