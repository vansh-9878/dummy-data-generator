import os
import random
import pandas as pd
import psycopg2
from datetime import datetime, UTC
from psycopg2.extras import execute_values

conn = psycopg2.connect(
    host=os.environ["SUPABASE_HOST"],
    port=os.environ["SUPABASE_PORT"],
    dbname=os.environ["SUPABASE_DB"],
    user=os.environ["SUPABASE_USER"],
    password=os.environ["SUPABASE_PASSWORD"],
    sslmode="require"
)

# Fetch customers
customers = pd.read_sql(
    """
    SELECT customer_id
    FROM customers
    """,
    conn
)

# Fetch restaurants
restaurants = pd.read_sql(
    """
    SELECT restaurant_id
    FROM restaurants
    """,
    conn
)

# Get next order id
cur = conn.cursor()

cur.execute(
    """
    SELECT COALESCE(MAX(order_id), 0)
    FROM orders
    """
)

next_id = cur.fetchone()[0] + 1

statuses = [
    "PLACED",
    "PREPARING"
]

new_orders = random.randint(50, 150)

rows = []

for i in range(new_orders):

    current_ts = datetime.now(UTC)

    rows.append(
        (
            next_id + i,
            random.choice(
                customers["customer_id"].tolist()
            ),
            random.choice(
                restaurants["restaurant_id"].tolist()
            ),
            round(
                random.uniform(100, 2000),
                2
            ),
            random.choice(statuses),
            current_ts,
            current_ts
        )
    )

execute_values(
    cur,
    """
    INSERT INTO orders
    (
        order_id,
        customer_id,
        restaurant_id,
        order_amount,
        status,
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

print(f"Created {new_orders} orders")