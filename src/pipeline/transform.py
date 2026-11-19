import pandas as pd

REQUIRED_COLUMNS = {
    "transaction_id", "transaction_date", "customer_id",
    "product", "quantity", "unit_price"
}

class DataValidationError(ValueError):
    """Raised when source data fails business/data-quality rules."""

def validate_sales(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise DataValidationError(
            f"Missing required columns: {sorted(missing_columns)}"
        )
    if df.empty:
        raise DataValidationError("Input dataset is empty")
    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise DataValidationError("Required fields contain null values")
    if df["transaction_id"].duplicated().any():
        raise DataValidationError("Duplicate transaction_id values found")

    dates = pd.to_datetime(df["transaction_date"], errors="coerce")
    if dates.isnull().any():
        raise DataValidationError("Invalid transaction_date value found")

    quantity = pd.to_numeric(df["quantity"], errors="coerce")
    unit_price = pd.to_numeric(df["unit_price"], errors="coerce")
    if quantity.isnull().any() or unit_price.isnull().any():
        raise DataValidationError("quantity and unit_price must be numeric")
    if (quantity <= 0).any():
        raise DataValidationError("quantity must be greater than zero")
    if (unit_price < 0).any():
        raise DataValidationError("unit_price cannot be negative")

def transform_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Validate, standardize and derive the sales amount."""
    validate_sales(df)
    result = df.copy()
    result["transaction_date"] = pd.to_datetime(
        result["transaction_date"], errors="raise"
    ).dt.date
    result["customer_id"] = result["customer_id"].astype(str).str.strip()
    result["product"] = result["product"].astype(str).str.strip().str.title()
    result["quantity"] = pd.to_numeric(result["quantity"]).astype(int)
    result["unit_price"] = pd.to_numeric(result["unit_price"]).round(2)
    result["total_amount"] = (
        result["quantity"] * result["unit_price"]
    ).round(2)
    return result[
        ["transaction_id", "transaction_date", "customer_id",
         "product", "quantity", "unit_price", "total_amount"]
    ]
