import pandas as pd
import random
from datetime import datetime
from pathlib import Path

customers = pd.read_csv("customers.csv")
restaurants = pd.read_csv("restaurants.csv")

FILE = "orders.csv"

statuses = [
    "PLACED",
    "PREPARING"
]

if Path(FILE).exists():

    orders = pd.read_csv(FILE)
    next_id = orders["order_id"].max() + 1

else:

    orders = pd.DataFrame()
    next_id = 1

rows = []

new_orders = random.randint(50, 150)

for i in range(new_orders):

    now = datetime.utcnow()

    rows.append({
        "order_id": next_id + i,
        "customer_id": random.choice(
            customers["customer_id"].tolist()
        ),
        "restaurant_id": random.choice(
            restaurants["restaurant_id"].tolist()
        ),
        "order_amount": round(
            random.uniform(100, 2000),
            2
        ),
        "status": random.choice(statuses),
        "created_at": now,
        "updated_at": now
    })

new_df = pd.DataFrame(rows)

orders = pd.concat(
    [orders, new_df],
    ignore_index=True
)

orders.to_csv(FILE, index=False)

print(f"Created {new_orders} orders")