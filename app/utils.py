import re
import pandas as pd

READ_ONLY = re.compile(r"^\s*SELECT\b", re.IGNORECASE | re.DOTALL)

def is_safe_sql(sql: str) -> bool:
    return bool(READ_ONLY.match(sql or "")) and not any(
        bad in sql.upper() for bad in ["DROP ", "DELETE ", "UPDATE ", "INSERT ", "ALTER ", "TRUNCATE ", ";;"]
    )

def to_dataframe(rows, cursor) -> pd.DataFrame:
    if cursor is None or not rows:
        return pd.DataFrame()
    cols = [c[0] for c in cursor.description]
    return pd.DataFrame(rows, columns=cols)

def infer_can_plot(df: pd.DataFrame) -> bool:
    return df.shape[1] in (2, 3) and df.select_dtypes(include=["number"]).shape[1] >= 1
