# app/agent.py
import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .prompts import SYSTEM_PROMPT, FEW_SHOTS

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Pass the key explicitly (removes ambiguity)
llm = ChatOpenAI(model=MODEL, temperature=0, openai_api_key=OPENAI_KEY)

def build_prompt(user_question: str) -> str:
    parts = ["System:\n" + SYSTEM_PROMPT]
    for ex in FEW_SHOTS:
        parts.append("User:\n" + ex["user"])
        parts.append("Assistant:\n" + json.dumps(ex["assistant"]))
    parts.append("User:\n" + user_question)
    parts.append("Assistant:")
    return "\n\n".join(parts)

def mock_plan(user_question: str) -> dict:
    # Simple heuristic mock so the UI keeps working without LLM calls
    if "revenue" in user_question.lower() and "product" in user_question.lower():
        sql = """
        SELECT p.product_name,
               SUM(oi.quantity * p.unit_price * (1 - oi.discount)) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 5;
        """
        return {"sql": sql, "summary": "Mocked: top products by revenue.", "viz": "bar"}
    # default mock
    return {"sql": "SELECT * FROM customers LIMIT 5;", "summary": "Mocked: showing sample customers.", "viz": "table"}

def plan_sql(user_question: str) -> dict:
    prompt = build_prompt(user_question)
    try:
        resp = llm.invoke(prompt)   # real call
        text = resp.content
        try:
            return json.loads(text)
        except Exception:
            start, end = text.find("{"), text.rfind("}")
            return json.loads(text[start:end+1])
    except Exception as e:
        # Fallback for 401/429 or any connectivity/quota error
        return mock_plan(user_question)
