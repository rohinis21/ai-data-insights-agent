import streamlit as st
from sqlalchemy import text
from app.db import engine

st.title("🗂️ Schema Explorer")
with engine.connect() as conn:
    tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")).fetchall()

for (t,) in tables:
    st.subheader(t)
    with engine.connect() as conn:
        cols = conn.execute(text(f"PRAGMA table_info({t})")).fetchall()
    st.table({"cid": [c[0] for c in cols], "name": [c[1] for c in cols], "type": [c[2] for c in cols]})
