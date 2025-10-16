import os
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DB_URL", "sqlite:///./data/retail.db")
engine = create_engine(DB_URL, future=True)

def run_sql(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        # SQLAlchemy 2.0 doesn't expose raw cursor by default; emulate description
        cols = result.keys()
    # Build a pseudo-cursor-like object
    class _C: pass
    c = _C()
    c.description = [(col,) for col in cols]
    return rows, c

def get_tables(engine_only=False):
    if engine_only:
        return engine
    with engine.connect() as conn:
        res = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        return [r[0] for r in res]
