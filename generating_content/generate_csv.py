import random
import os
import pandas as pd

# Define the categories for the new examples
animal_types = ['dog', 'cat']
cat_names = [
    # Traditional Cat Names
    "Whiskers", "Mittens", "Luna", "Oliver", "Bella", "Simba", "Chloe", "Sasha", "Shadow", "Nala",
    "Coco", "Leo", "Ginger", "Oscar", "Penny", "Dusty", "Tiger", "Loki", "Misty",
    "Chester", "Jasper", "Snowball", "Felix", "Ruby",
    # Food-Inspired Names
    "Oreo", "Cookie", "Pepper", "Pickle", "Biscuit", "Mochi", "Sushi", "Waffle", "Taco",
    # Color-Inspired Names
    "Smokey", "Patches", "Marble", "Auburn", "Midnight", "Storm", "Amber", "Ash",
    # Cute/Quirky Names
    "Milo", "Ziggy", "Binx", "Kitty", "Scout", "Pixie", "Willow", "Salem", "Sage",
    # Royal/Elegant Names
    "Princess", "Duke", "Duchess", "Queen", "King", "Prince", "Baron", "Lady",
    # Nature-Inspired
    "River", "Forest", "Sky", "Rain", "Moss", "Maple", "Pine", "Cloud"
]

dog_names = [
    # Classic Dog Names
    "Max", "Bella", "Charlie", "Rocky", "Daisy", "Buddy", "Rex", "Harley", "Cooper", "Finn",
    "Zara", "Buster", "Duke", "Oscar", "Zeus", "Rover", "Molly", "Bruno", "Jax",
    "Tank", "Coco", "Riley", "Maddie", "Murphy", "Nala",
    # Tough/Strong Names
    "Thor", "Atlas", "Titan", "Diesel", "Blade", "Storm", "Wolf", "Bear", "Axel",
    # Human Names
    "Bailey", "Sam", "Jack", "Lucy", "Sophie", "Ruby", "Oliver", "Archie", "Winston",
    # Food Names
    "Pepper", "Cookie", "Pickles", "Taco", "Nacho", "Nugget", "Pretzel", "Oreo",
    # Cute/Playful Names
    "Ziggy", "Teddy", "Scout", "Roxy", "Pixie", "Banjo", "Pip", "Sunny", "Waffles",
    # Nature Names
    "River", "Forest", "Brook", "Sky", "Storm", "Dawn", "Winter", "Summer"
]
colors = ['white', 'black', 'brown', 'gray']
behavior_options = [
    # Friendly Behaviors
    "friendly", "sociable", "outgoing", "people-oriented", "affectionate", "loving",
    # Active Behaviors
    "playful", "energetic", "active", "athletic", "adventurous", "enthusiastic",
    # Calm Behaviors
    "calm", "gentle", "relaxed", "mellow", "laid-back", "quiet",
    # Training-Related
    "intelligent", "trainable", "obedient", "quick learner", "responsive", "focused",
    # Personality Traits
    "independent", "confident", "shy", "cautious", "curious", "alert",
    # Social Behaviors
    "good with kids", "good with other pets", "protective", "loyal", "devoted",
    # Specific Traits
    "lap cat/dog", "cuddly", "talkative", "food-motivated", "dignified", "patient"
]
health_status = ['excellent', 'good', 'bad']
target_audience = ['families', 'elderly', 'singles', 'active individuals', 'couples']


# Create a function to generate random examples
def generate_random_examples(num_examples):
    examples = []
    for i in range(num_examples):
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

        health = random.choices(health_status, weights=[0.5, 0.35, 0.15])[0]

        vaccinated = True if health == 'excellent' else random.choices([True, False], weights=[0.9, 0.1])[0]

        audience = random.choice(target_audience)

        examples.append({
            'animal_type': animal_type,
            'name': name,
            'age': age,
            'color': color,
            'months_in_shelter': months_in_shelter,
            'behavior': behavior,
            'health': health,
            'vaccinated': vaccinated,
            'target_audience': audience
        })

    return pd.DataFrame(examples)


def append_to_csv(new_data, csv_path):
    try:
        # Check if file exists
        if os.path.exists(csv_path):
            existing_data = pd.read_csv(csv_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # Save to CSV
        updated_data.to_csv(csv_path, index=False)
        print(f"Successfully added {len(new_data)} new animals to {csv_path}")
        print(f"Total number of animals in database: {len(updated_data)}")

    except Exception as e:
        print(f"Error occurred while updating CSV: {str(e)}")


if __name__ == "__main__":
    # Configuration
    NUM_EXAMPLES = 94 # Change this to generate more or fewer animals
    CSV_PATH = "../data/animals.csv"  # Change this to your desired path

    # Generate new examples
    new_animals = generate_random_examples(NUM_EXAMPLES)

    # Print preview of new animals
    print("\nPreview of new animals being added:")
    print(new_animals)

    # Append to CSV
    append_to_csv(new_animals, CSV_PATH)
