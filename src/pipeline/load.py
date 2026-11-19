from pathlib import Path
import pandas as pd
from .db import get_connection

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_FILE = PROJECT_ROOT / "sql" / "create_tables.sql"

def create_tables() -> None:
    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

def load_sales(df: pd.DataFrame) -> int:
    """Upsert records by transaction_id; safe to re-run for same IDs."""
    insert_sql = '''
        INSERT INTO sales (
            transaction_id, transaction_date, customer_id, product,
            quantity, unit_price, total_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO UPDATE SET
            transaction_date = EXCLUDED.transaction_date,
            customer_id = EXCLUDED.customer_id,
            product = EXCLUDED.product,
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price,
            total_amount = EXCLUDED.total_amount,
            loaded_at = CURRENT_TIMESTAMP
    '''
    records = [
        (
            row.transaction_id, row.transaction_date, row.customer_id,
            row.product, int(row.quantity), float(row.unit_price),
            float(row.total_amount)
        )
        for row in df.itertuples(index=False)
    ]
    if not records:
        return 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(insert_sql, records)
    return len(records)
