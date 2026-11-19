import psycopg2
from .config import DB_CONFIG

def get_connection():
    """Open a PostgreSQL connection using environment-based configuration."""
    return psycopg2.connect(**DB_CONFIG)
