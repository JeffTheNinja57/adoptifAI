import pandas as pd

# Load the CSV file
csv_file = "../test_animal_data.csv"
df = pd.read_csv(csv_file)

# Convert the DataFrame to JSON format
json_data = df.to_json(orient='records')

# Save the JSON data to a file
json_file = "../test_animal_data.json"
with open(json_file, "w") as file:
    file.write(json_data)

print("JSON data saved to:", json_file)

