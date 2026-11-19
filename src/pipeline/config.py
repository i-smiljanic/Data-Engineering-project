import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = PROJECT_ROOT / "data" / "raw" / "sales.csv"

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5433")),
    "dbname": os.getenv("POSTGRES_DB", "retail_warehouse"),
    "user": os.getenv("POSTGRES_USER", "pipeline_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "local_demo_password"),
}
