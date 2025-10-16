# Snowflake Backend Setup

1) **Install deps** (already in `requirements.txt`):
```
pip install snowflake-connector-python snowflake-sqlalchemy
```

2) **Create a read‑only role** (as ACCOUNTADMIN/SECURITYADMIN):
```
# Edit names and run:
@ scripts/snowflake_readonly.sql
```

3) **Set environment variables** in `.env`:
```
DB_URL=  # leave blank to signal Snowflake usage (or ignore in code)
SNOWFLAKE_USER=YOUR_USER
SNOWFLAKE_PASSWORD=YOUR_PASSWORD
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_WAREHOUSE=YOUR_WAREHOUSE
SNOWFLAKE_DATABASE=YOUR_DATABASE
SNOWFLAKE_SCHEMA=YOUR_SCHEMA
SNOWFLAKE_ROLE=READ_ONLY_ROLE
LLM_MODEL=gpt-4o-mini
```

4) **Switch the app to Snowflake** by adapting imports in `app/main.py`:
```python
# Replace:
# from .db import run_sql
# With:
from .db_snowflake import run_sql
```

5) **Test queries** (same prompts as SQLite). Ensure your Snowflake schema has tables:
- `customers(customer_id, customer_name, segment, country)`
- `products(product_id, product_name, category, unit_price)`
- `orders(order_id, customer_id, order_date)`
- `order_items(order_item_id, product_id, quantity, discount)`
```sql
-- Optional: create views that match these names/columns
```

**Tip:** Keep the SQLite path for local dev and switch to Snowflake for production‑like demos.
