from faker import Faker
import pandas as pd
import random
from datetime import datetime, UTC

fake = Faker("en_IN")

cities = [
    "Delhi",
    "Noida",
    "Gurgaon",
    "Bangalore",
    "Mumbai",
    "Pune",
    "Hyderabad",
    "Chennai"
]

cuisines = [
    "North Indian",
    "South Indian",
    "Chinese",
    "Italian",
    "Fast Food",
    "Biryani",
    "Desserts",
    "Cafe"
]

restaurants = []

for i in range(1, 101):

    timestamp = datetime.now(UTC).isoformat()

    restaurants.append({
        "restaurant_id": i,
        "restaurant_name": fake.company(),
        "city": random.choice(cities),
        "cuisine": random.choice(cuisines),
        "rating": round(random.uniform(3.5, 5.0), 1),
        "created_at": timestamp,
        "updated_at": timestamp
    })

df = pd.DataFrame(restaurants)

df.to_csv("restaurants.csv", index=False)

print(f"Generated {len(df)} restaurants")

# print(df.head())