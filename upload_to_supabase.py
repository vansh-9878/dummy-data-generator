import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect(
    host=os.environ["SUPABASE_HOST"],
    port=os.environ["SUPABASE_PORT"],
    dbname=os.environ["SUPABASE_DB"],
    user=os.environ["SUPABASE_USER"],
    password=os.environ["SUPABASE_PASSWORD"]
)


cur = conn.cursor()


def upsert_restaurants():

    df = pd.read_csv("restaurants.csv")

    rows = [tuple(x) for x in df.to_numpy()]

    query = """
    INSERT INTO restaurants
    (
        restaurant_id,
        restaurant_name,
        city,
        cuisine,
        rating,
        created_at,
        updated_at
    )
    VALUES %s
    ON CONFLICT (restaurant_id)
    DO UPDATE SET
        restaurant_name = EXCLUDED.restaurant_name,
        city = EXCLUDED.city,
        cuisine = EXCLUDED.cuisine,
        rating = EXCLUDED.rating,
        updated_at = EXCLUDED.updated_at;
    """

    execute_values(cur, query, rows)


def upsert_customers():

    df = pd.read_csv("customers.csv")

    rows = [tuple(x) for x in df.to_numpy()]

    query = """
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
    ON CONFLICT (customer_id)
    DO UPDATE SET
        customer_name = EXCLUDED.customer_name,
        city = EXCLUDED.city,
        customer_tier = EXCLUDED.customer_tier,
        is_active = EXCLUDED.is_active,
        updated_at = EXCLUDED.updated_at;
    """

    execute_values(cur, query, rows)


def upsert_orders():

    df = pd.read_csv("orders.csv")

    rows = [tuple(x) for x in df.to_numpy()]

    query = """
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
    ON CONFLICT (order_id)
    DO UPDATE SET
        order_amount = EXCLUDED.order_amount,
        status = EXCLUDED.status,
        updated_at = EXCLUDED.updated_at;
    """

    execute_values(cur, query, rows)


upsert_restaurants()
upsert_customers()
upsert_orders()

conn.commit()

cur.close()
conn.close()

print("Upload completed")