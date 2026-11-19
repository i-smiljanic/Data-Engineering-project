import pandas as pd
from src.pipeline.transform import transform_sales

def test_transform_calculates_total_and_standardizes_product():
    source = pd.DataFrame([{
        "transaction_id": "T100",
        "transaction_date": "2025-01-02",
        "customer_id": " C01 ",
        "product": " coffee beans ",
        "quantity": 2,
        "unit_price": 4.50,
    }])
    result = transform_sales(source)
    assert result.loc[0, "total_amount"] == 9.00
    assert result.loc[0, "product"] == "Coffee Beans"
    assert result.loc[0, "customer_id"] == "C01"
    assert str(result.loc[0, "transaction_date"]) == "2025-01-02"

def test_transform_returns_expected_columns():
    source = pd.DataFrame([{
        "transaction_id": "T101",
        "transaction_date": "2025-01-02",
        "customer_id": "C02",
        "product": "Tea",
        "quantity": 1,
        "unit_price": 3.25,
    }])
    result = transform_sales(source)
    assert list(result.columns) == [
        "transaction_id", "transaction_date", "customer_id",
        "product", "quantity", "unit_price", "total_amount"
    ]
