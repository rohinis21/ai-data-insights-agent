import os
from sqlalchemy import create_engine, text

# Build SQLAlchemy URL for Snowflake
# Example account: xy12345.us-east-1
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
role = os.getenv("SNOWFLAKE_ROLE", "READ_ONLY_ROLE")

url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"
engine = create_engine(url)

def run_sql(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
    class _C: pass
    c = _C()
    c.description = [(col,) for col in cols]
    return rows, c
