# 📊 AI Data Insights Agent  

**Developer:** Rohini Sondole  
**Type:** GenAI + SQL + Business Analytics  
**Environment:** Python 3.13 | Streamlit | LangChain | SQLite  

---

## 🧠 Overview  

The **AI Data Insights Agent** is a Streamlit-based web application that allows users to ask business questions in plain English and automatically receive:  
1️⃣ An interpreted **SQL query**  
2️⃣ A concise **natural-language summary**  
3️⃣ A **data visualization or table** of results  

This project merges **Natural Language Processing (NLP)**, **SQL generation**, and **data visualization** into a single interface — ideal for non-technical business users who need quick insights without writing SQL manually.  

---

## 🎯 Key Objectives  

✅ Translate natural-language questions into SQL queries  
✅ Execute queries safely on a structured database  
✅ Visualize outputs (bar / line charts) dynamically  
✅ Provide fallback operation if LLM API fails (mock mode)  
✅ Demonstrate GenAI integration with analytics stacks  

---

## 🧩 System Architecture  

| Layer | Modules | Description |
|:------|:---------|:------------|
| **Frontend** | `app/main.py` | Streamlit UI – handles input / output / visualization |
| **LLM Agent** | `app/agent.py` | Uses LangChain + OpenAI to generate SQL plans |
| **Database** | `app/db.py`, `data/retail.db` | SQLite database with sample retail data |
| **Utilities** | `app/utils.py` | Safety checks, dataframe conversion, plot helper |
| **Environment** | `.env` | Holds `OPENAI_API_KEY` and `DB_URL` |

📌 **Architecture Diagram:**  

📌 **Architecture Diagram:**

![Architecture](architecture.png)

---

## 🔁 Data Flow  

1️⃣ User types a question in Streamlit  
2️⃣ App calls `plan_sql()` → LLM (or mock) generates SQL  
3️⃣ `run_sql()` executes the query on `retail.db`  
4️⃣ Results are converted to a DataFrame and visualized  

---

## 🗄️ Dataset – `retail.db`  

**Source:** Generated from CSV files in `data/` via `scripts/seed_db.py`  

| Table | Description | Columns |
|:------|:-------------|:---------|
| **customers** | Customer profiles | `customer_id`, `customer_name`, `segment`, `country` |
| **products** | Product catalog | `product_id`, `product_name`, `category`, `unit_price` |
| **orders** | Order records | `order_id`, `customer_id`, `order_date` |
| **order_items** | Items per order | `order_item_id`, `order_id`, `product_id`, `quantity`, `discount` |

**Example schema:**
```sql
SELECT name FROM sqlite_master WHERE type='table';
```

## 🚀 Application Flow

**User Question → LLM/Mock Planner → SQL → Database → Visualization**

### 🧭 UI Features
- 📝 **Textbox:** “Your question”  
- 🔘 **Button:** Run  
- 🗂️ **Tabs:** Schema Explorer / Saved Queries  

### 🧾 Outputs Shown
- 🔎 **Generated SQL query**  
- 🧠 **AI-generated summary of insight**  
- 📈 **Bar / Line chart + DataFrame**

---

## 💡 Example Queries & Outputs

| User Question | Generated SQL | Result Type |
|----------------|---------------|--------------|
| **Top 5 products by revenue** | `SELECT p.product_name, SUM(oi.quantity * p.unit_price * (1 - oi.discount)) AS revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_name ORDER BY revenue DESC LIMIT 5;` | 📊 Bar chart |
| **Show monthly sales in 2024** | `SELECT strftime('%m', o.order_date) AS month, SUM(oi.quantity * p.unit_price) AS sales FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE strftime('%Y', o.order_date)= '2024' GROUP BY month;` | 📈 Line chart |
| **Revenue by category** | `SELECT p.category, SUM(oi.quantity * p.unit_price) AS revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.category;` | 📊 Bar chart |

---

## 🧱 Error Handling & Fallback

- If `OPENAI_API_KEY` is **invalid** or **quota exhausted (401 / 429)** → `plan_sql()` automatically falls back to a **mock plan** so the demo still runs.  
- Only **SELECT** queries are allowed (validated using `is_safe_sql()` guard).  
- Invalid or unsafe queries show:
  ```python
  st.error("Blocked: only SELECT queries allowed.")

## ⚙️ Installation & Execution

```bash
# Clone the repository
git clone https://github.com/rohinis21/ai-data-insights-agent.git
cd ai-data-insights-agent

# Setup environment
python3 -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate
pip install -r requirements.txt

# Seed sample database
python scripts/seed_db.py

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY inside the .env file

# Run the Streamlit app
python -m streamlit run app/main.py
```

➡️ Then open: http://localhost:8501

## 🧰 Tech Stack

| Layer | Technology |
|--------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.13 |
| **Database** | SQLite |
| **AI Agent** | LangChain + OpenAI GPT |
| **Visualization** | Plotly Express |
| **Environment Mgmt** | python-dotenv / venv |

---

## 🌟 Future Enhancements

- 🔗 Integrate **Snowflake** or **PostgreSQL** connections  
- 👤 Add **user authentication** and saved dashboards  
- 🎤 Support **speech-to-text** queries  
- 📊 Enable **multi-chart comparisons**  
- ☁️ Deploy on **Streamlit Cloud**, **AWS**, or **Azure**

---

## 🎓 Learning Outcomes

- 🤖 Hands-on **LLM integration** for structured query generation  
- 🧮 Practical **SQL + DataFrame** interaction with visual analytics  
- 🔒 Understanding **safe execution** and error handling in GenAI apps  
- 💡 Bridging **AI and business decision support**

---

## 🏁 Conclusion

This project demonstrates how **Generative AI models** can act as natural-language data analysts —  
translating plain business questions into actionable SQL insights.

Even when offline or quota-limited, the **mock mode** ensures full demo capability —  
making it ideal for **learning, presentations, and portfolio showcases.**



