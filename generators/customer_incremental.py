import os
import random
import psycopg2
from faker import Faker
from datetime import datetime, UTC
from psycopg2.extras import execute_values

fake = Faker("en_IN")

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

conn = psycopg2.connect(
    host=os.environ["SUPABASE_HOST"],
    port=os.environ["SUPABASE_PORT"],
    dbname=os.environ["SUPABASE_DB"],
    user=os.environ["SUPABASE_USER"],
    password=os.environ["SUPABASE_PASSWORD"],
    sslmode="require"
)

cur = conn.cursor()

cur.execute(
    """
    SELECT COALESCE(MAX(customer_id), 0)
    FROM customers
    """
)

next_id = cur.fetchone()[0] + 1

new_customers = random.randint(20, 50)

rows = []

for i in range(new_customers):

    current_ts = datetime.now(UTC)

    rows.append(
        (
            next_id + i,
            fake.name(),
            random.choice(cities),
            random.choice(tiers),
            True,
            current_ts,
            current_ts
        )
    )

execute_values(
    cur,
    """
    INSERT INTO customers
    (
        customer_id,
        customer_name,
        city,
        customer_tier,
        is_active,
        created_at,
        updated_at
    )
    VALUES %s
    """,
    rows
)

conn.commit()

cur.close()
conn.close()

print(f"Added {new_customers} customers")