CREATE TABLE IF NOT EXISTS sales (
    transaction_id VARCHAR(30) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    customer_id VARCHAR(30) NOT NULL,
    product VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount NUMERIC(14, 2) NOT NULL CHECK (total_amount >= 0),
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sales_transaction_date
    ON sales (transaction_date);

CREATE INDEX IF NOT EXISTS idx_sales_product
    ON sales (product);
