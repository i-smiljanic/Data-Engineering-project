from datetime import datetime, timedelta
from pathlib import Path
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path("/opt/airflow/project")
sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.extract import extract_sales
from src.pipeline.transform import transform_sales
from src.pipeline.load import create_tables, load_sales

SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "sales.csv"

def extract_task(**context):
    df = extract_sales(SOURCE_FILE)
    # Keep XCom small: pass a JSON-compatible list of records between tasks.
    records = df.to_dict(orient="records")
    context["ti"].xcom_push(key="raw_records", value=records)
    return f"Extracted {len(records)} records"

def transform_task(**context):
    records = context["ti"].xcom_pull(
        task_ids="extract_sales", key="raw_records"
    )
    import pandas as pd
    transformed = transform_sales(pd.DataFrame(records))
    context["ti"].xcom_push(
        key="transformed_records",
        value=transformed.astype(str).to_dict(orient="records")
    )
    return f"Validated and transformed {len(transformed)} records"

def load_task(**context):
    records = context["ti"].xcom_pull(
        task_ids="transform_sales", key="transformed_records"
    )
    import pandas as pd
    df = pd.DataFrame(records)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["total_amount"] = df["total_amount"].astype(float)
    create_tables()
    count = load_sales(df)
    return f"Loaded/upserted {count} records"

default_args = {
    "owner": "portfolio",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="retail_sales_pipeline",
    description="CSV to PostgreSQL batch ETL with validation",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "etl", "python", "postgres"],
) as dag:
    extract = PythonOperator(
        task_id="extract_sales",
        python_callable=extract_task,
    )
    transform = PythonOperator(
        task_id="transform_sales",
        python_callable=transform_task,
    )
    load = PythonOperator(
        task_id="load_sales",
        python_callable=load_task,
    )
    extract >> transform >> load
