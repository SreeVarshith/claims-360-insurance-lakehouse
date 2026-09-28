-- Verify tables (from the report)
SELECT * FROM customers LIMIT 5;
SELECT * FROM policies  LIMIT 5;

-- Expected after loading the generated sample data: 50 rows in each table
SELECT COUNT(*) AS customer_rows FROM customers;
SELECT COUNT(*) AS policy_rows   FROM policies;
