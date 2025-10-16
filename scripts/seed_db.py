import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DB_URL", "sqlite:///./data/retail.db")
engine = create_engine(DB_URL)

customers = pd.read_csv("data/customers.csv")
products  = pd.read_csv("data/products.csv")
orders    = pd.read_csv("data/orders.csv")
items     = pd.read_csv("data/order_items.csv")

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS order_items"))
    conn.execute(text("DROP TABLE IF EXISTS orders"))
    conn.execute(text("DROP TABLE IF EXISTS products"))
    conn.execute(text("DROP TABLE IF EXISTS customers"))

    conn.execute(text("""    CREATE TABLE customers (
      customer_id INTEGER PRIMARY KEY,
      customer_name TEXT,
      segment TEXT,
      country TEXT
    )
    """))

    conn.execute(text("""    CREATE TABLE products (
      product_id INTEGER PRIMARY KEY,
      product_name TEXT,
      category TEXT,
      unit_price REAL
    )
    """))

    conn.execute(text("""    CREATE TABLE orders (
      order_id INTEGER PRIMARY KEY,
      customer_id INTEGER,
      order_date DATE,
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """))

    conn.execute(text("""    CREATE TABLE order_items (
      order_item_id INTEGER PRIMARY KEY,
      order_id INTEGER,
      product_id INTEGER,
      quantity INTEGER,
      discount REAL,
      FOREIGN KEY (order_id) REFERENCES orders(order_id),
      FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """))

customers.to_sql("customers", engine, if_exists="append", index=False)
products.to_sql("products", engine, if_exists="append", index=False)
orders.to_sql("orders", engine, if_exists="append", index=False)
items.to_sql("order_items", engine, if_exists="append", index=False)

print("Seeded DB at:", DB_URL)
