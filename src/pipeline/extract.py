from pathlib import Path
import pandas as pd

def extract_sales(file_path: str | Path) -> pd.DataFrame:
    """Read the raw sales CSV into a DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    return pd.read_csv(path)
