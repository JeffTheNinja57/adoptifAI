import random
import pandas as pd

# Define the categories for the new examples
animal_types = ['dog', 'cat']
cat_names = [
    "Whiskers", "Mittens", "Luna", "Oliver", "Bella", "Simba", "Chloe", "Sasha", "Shadow", "Nala",
    "Milo", "Coco", "Leo", "Ginger", "Oscar", "Penny", "Dusty", "Tiger", "Loki", "Misty",
    "Chester", "Jasper", "Snowball", "Felix", "Ruby"
]

dog_names = [
    "Max", "Bella", "Charlie", "Rocky", "Daisy", "Buddy", "Rex", "Harley", "Cooper", "Finn",
    "Zara", "Buster", "Duke", "Oscar", "Zeus", "Rover", "Molly", "Bruno", "Duke", "Jax",
    "Tank", "Coco", "Riley", "Maddie", "Murphy", "Nala"
]
colors = ['white', 'black', 'brown', 'gray']
behavior_options = ["friendly", "shy", "playful", "curious", "energetic",
                    "calm", "protective", "loyal", "obedient", "independent", "affectionate"]
health_status = ['excellent', 'good', 'bad']
target_audience = ['families', 'elderly', 'singles', 'active individuals', 'couples']

# Create a function to generate random examples
def generate_random_examples(num_examples):
    examples = []
    for _ in range(num_examples):
        animal_type = random.choice(animal_types)
        name = random.choice(cat_names if animal_type == 'cat' else dog_names)
        age = random.randint(1, 15)
        color = random.choice(colors)
        if age < 10:
            max_months = age * 12
            months_in_shelter = random.randint(1, min(max_months, 60))
        else:
            months_in_shelter = random.randint(16, 60)
        behavior = ", ".join(random.sample(behavior_options, random.randint(1, 3)))
        health = random.choice(health_status)

        vaccinated = True if health == 'excellent' else random.choice([True, False])

        audience = random.choice(target_audience)

        examples.append([animal_type, name, age, color, months_in_shelter,
                         behavior, health, vaccinated, audience])

    # Convert to DataFrame for easy appending
    return pd.DataFrame(examples, columns=['animal_type', 'name', 'age', 'color', 'months_in_shelter',
                                           'behavior', 'health', 'vaccinated', 'target_audience'])


# Generate 40 random examples
random_examples = generate_random_examples(120)

# Load the existing CSV file
existing_data = pd.read_csv("animals.csv")

# Append the new examples to the existing data
updated_data = pd.concat([existing_data, random_examples], ignore_index=True)

# Save the updated data back to the CSV file
updated_data.to_csv("animals.csv", index=False)
