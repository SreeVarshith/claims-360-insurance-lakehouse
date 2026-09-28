-- Amazon RDS PostgreSQL  |  run via AWS CloudShell using psql
-- Connect (use placeholders / env vars, never commit real values):
--   psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
--
-- NOTE: the report names the database "insurance_db" in the configuration
-- table but connects to "insurancedb" in the psql / JDBC examples.
-- Use whichever name your instance actually has and keep it consistent
-- with the Glue job parameter --DB_NAME.

-- Customers table
CREATE TABLE customers (
    cust_id      INT PRIMARY KEY,
    name         VARCHAR(100),
    email        VARCHAR(100),
    risk_segment VARCHAR(20)
);

-- Policies table
CREATE TABLE policies (
    policy_id      VARCHAR(20) PRIMARY KEY,
    cust_id        INT,
    policy_type    VARCHAR(50),
    premium_amount INT,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);
