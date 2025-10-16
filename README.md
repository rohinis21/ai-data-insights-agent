# AI Data Insights Agent

Ask business questions in plain English → get safe SQL, a summary, and a chart.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # add your API key
python scripts/seed_db.py
streamlit run app/main.py
```

## Notes
- The agent only allows **SELECT** queries (guardrails in `utils.py`).
- Sample data is under `data/` and is seeded into `data/retail.db`.
- Extend with Snowflake by swapping `DB_URL` and installing `snowflake-sqlalchemy`.
