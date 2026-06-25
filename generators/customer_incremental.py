import pandas as pd
import random
from faker import Faker
from datetime import datetime
from pathlib import Path

fake = Faker("en_IN")

FILE = "customers.csv"

cities = [
    "Delhi",
    "Noida",
    "Gurgaon",
    "Bangalore",
    "Mumbai",
    "Pune"
]

tiers = [
    "BRONZE",
    "SILVER",
    "GOLD"
]

if Path(FILE).exists():

    customers = pd.read_csv(FILE)
    next_id = customers["customer_id"].max() + 1

else:

    customers = pd.DataFrame()
    next_id = 1

rows = []

new_customers = random.randint(20, 50)

for i in range(new_customers):

    now = datetime.utcnow()

    rows.append({
        "customer_id": next_id + i,
        "customer_name": fake.name(),
        "city": random.choice(cities),
        "customer_tier": random.choice(tiers),
        "is_active": True,
        "created_at": now,
        "updated_at": now
    })

new_df = pd.DataFrame(rows)

customers = pd.concat(
    [customers, new_df],
    ignore_index=True
)

customers.to_csv(FILE, index=False)

print(f"Added {new_customers} customers")