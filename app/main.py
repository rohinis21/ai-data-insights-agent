# app/main.py

import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# --- Robust imports: try absolute first, then relative fallback ---
try:
    from app.agent import plan_sql
    from app.db import run_sql
    from app.utils import is_safe_sql, to_dataframe, infer_can_plot
except ImportError:
    # Fallback if "app" isn't recognized as a package
    from agent import plan_sql
    from db import run_sql
    from utils import is_safe_sql, to_dataframe, infer_can_plot

# --- App setup ---
load_dotenv()
st.set_page_config(page_title="AI Data Insights Agent", page_icon="📊", layout="wide")

st.title("📊 AI Data Insights Agent")
st.caption("Ask business questions in plain English. The agent will convert to SQL, execute, and summarize.")

# --- UI ---
q = st.text_input("Your question", placeholder="e.g., Show monthly revenue by category in 2024")
run = st.button("Run")

# --- Main action ---
if run and q:
    with st.spinner("Thinking..."):
        plan = plan_sql(q) if q else {}
        sql = plan.get("sql", "")
        summary = plan.get("summary", "")
        viz = plan.get("viz", "table")

        st.subheader("🔎 Planned SQL")
        st.code(sql or "-- no sql produced --", language="sql")

        if not sql:
            st.error("No SQL was produced by the model. Try rephrasing your question.")
        elif not is_safe_sql(sql):
            st.error("Blocked: only SELECT queries are allowed.")
        else:
            rows, cursor = run_sql(sql)
            df = to_dataframe(rows, cursor) if rows else pd.DataFrame()

            st.subheader("🧠 Answer")
            st.write(summary or "The model didn't include a summary.")

            st.subheader("📈 Results")
            if df.empty:
                st.info("No rows returned.")
            else:
                st.dataframe(df, use_container_width=True)

                # Simple viz heuristic
                if infer_can_plot(df):
                    x = df.columns[0]
                    num_cols = df.select_dtypes(include=["number"]).columns
                    y = num_cols[-1] if len(num_cols) else None
                    if y and y != x:
                        fig = px.line(df, x=x, y=y) if viz == "line" else px.bar(df, x=x, y=y)
                        st.plotly_chart(fig, use_container_width=True)
