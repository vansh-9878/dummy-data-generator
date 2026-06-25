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

transitions = {
    "PLACED": ["PREPARING", "CANCELLED"],
    "PREPARING": ["DELIVERED"]
}

# Fetch eligible orders
query = """
SELECT
    order_id,
    status
FROM orders
WHERE status IN ('PLACED', 'PREPARING')
"""

orders = pd.read_sql(query, conn)

if len(orders) == 0:
    print("No eligible orders found")
    conn.close()
    exit()

sample_size = min(
    len(orders),
    random.randint(20, 100)
)

selected = orders.sample(sample_size)

current_ts = datetime.now(UTC)

updates = []

for _, row in selected.iterrows():

    new_status = random.choice(
        transitions[row["status"]]
    )

    updates.append(
        (
            row["order_id"],
            new_status,
            current_ts
        )
    )

cur = conn.cursor()

execute_values(
    cur,
    """
    UPDATE orders AS o
    SET
        status = v.status,
        updated_at = v.updated_at
    FROM (
        VALUES %s
    ) AS v(order_id, status, updated_at)
    WHERE o.order_id = v.order_id
    """,
    updates
)

conn.commit()

cur.close()
conn.close()

print(f"Updated {sample_size} orders")