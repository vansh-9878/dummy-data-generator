import pandas as pd
import random
from datetime import datetime, UTC

orders = pd.read_csv("orders.csv")

transitions = {
    "PLACED": ["PREPARING", "CANCELLED"],
    "PREPARING": ["DELIVERED"]
}

eligible = orders[
    orders["status"].isin(transitions.keys())
]

sample_size = 0

if len(eligible) > 0:

    sample_size = min(
        len(eligible),
        random.randint(20, 100)
    )

    selected = eligible.sample(sample_size)

    current_ts = datetime.now(UTC).isoformat()

    for idx in selected.index:

        current_status = orders.loc[idx, "status"]

        orders.loc[idx, "status"] = random.choice(
            transitions[current_status]
        )

        orders.loc[idx, "updated_at"] = current_ts

orders.to_csv(
    "orders.csv",
    index=False
)

print(f"Updated {sample_size} orders")