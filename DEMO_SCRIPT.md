# 60‑Second Demo Script (AI Data Insights Agent)

**Hook (0‑10s):**
"Hi, I built a Gen‑AI powered analytics agent. You ask a question in plain English, it writes safe SQL, executes it, and visualizes the answer."

**Show the UI (10‑25s):**
- Type: *Top 5 products by revenue*
- Point to the generated SQL block (SELECT‑only, explicit joins).
- Show the bar chart and the table.

**Second Query (25‑40s):**
- Type: *Monthly revenue trend in 2024*
- Show that the model groups by month and returns a line/bar chart.

**Safety & Stack (40‑55s):**
- "Guardrails block non‑SELECT operations; server‑side we use a read‑only Snowflake role (or local SQLite)."
- Stack: Streamlit (UI), LangChain (LLM), SQLAlchemy (DB), Plotly (viz).

**Close (55‑60s):**
- "This showcases NL→SQL, analytics storytelling, and safe Gen‑AI integration. Repo link in the README."
