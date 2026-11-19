import pandas as pd
import pytest
from src.pipeline.transform import (
    DataValidationError, transform_sales
)

def valid_row():
    return {
        "transaction_id": "T100",
        "transaction_date": "2025-01-02",
        "customer_id": "C01",
        "product": "Coffee",
        "quantity": 2,
        "unit_price": 4.50,
    }

def test_duplicate_transaction_ids_are_rejected():
    row = valid_row()
    with pytest.raises(DataValidationError, match="Duplicate"):
        transform_sales(pd.DataFrame([row, row]))

def test_zero_quantity_is_rejected():
    row = valid_row()
    row["quantity"] = 0
    with pytest.raises(DataValidationError, match="quantity"):
        transform_sales(pd.DataFrame([row]))

def test_invalid_date_is_rejected():
    row = valid_row()
    row["transaction_date"] = "not-a-date"
    with pytest.raises(DataValidationError, match="transaction_date"):
        transform_sales(pd.DataFrame([row]))

def test_missing_required_column_is_rejected():
    row = valid_row()
    del row["product"]
    with pytest.raises(DataValidationError, match="Missing required columns"):
        transform_sales(pd.DataFrame([row]))
