-- 1. Total revenue and transaction count
SELECT
    COUNT(*) AS transaction_count,
    SUM(total_amount) AS total_revenue
FROM sales;

-- 2. Revenue by product
SELECT
    product,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;

-- 3. Daily revenue
SELECT
    transaction_date,
    COUNT(*) AS transactions,
    SUM(total_amount) AS daily_revenue
FROM sales
GROUP BY transaction_date
ORDER BY transaction_date;

-- 4. Average transaction value
SELECT ROUND(AVG(total_amount), 2) AS average_transaction_value
FROM sales;

-- 5. Check for duplicate transaction IDs (should return zero rows)
SELECT transaction_id, COUNT(*)
FROM sales
GROUP BY transaction_id
HAVING COUNT(*) > 1;
