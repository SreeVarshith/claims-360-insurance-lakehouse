# Amazon RDS PostgreSQL `[IMPLEMENTED in POC]`

| Parameter | Value |
|---|---|
| DB identifier | `insurance-db` |
| Engine | PostgreSQL |
| Instance class | `db.t4g.micro` |
| Region / AZ | `us-east-1c` |
| Database name | `insurance_db` (see note) |
| Tables | `customers`, `policies` |

> **Note:** the report lists the database as `insurance_db` but its `psql` and JDBC examples use `insurancedb`. Use the real name of your instance and pass it to the Glue job as `--DB_NAME`.

## Schema

| customers | type | | policies | type |
|---|---|---|---|---|
| `cust_id` | INT, PK | | `policy_id` | VARCHAR(20), PK |
| `name` | VARCHAR(100) | | `cust_id` | INT, FK → customers |
| `email` | VARCHAR(100) | | `policy_type` | VARCHAR(50) |
| `risk_segment` | VARCHAR(20) | | `premium_amount` | INT |

## How it was loaded

Via AWS CloudShell with `psql`: [`sql/rds/create_tables.sql`](../../sql/rds/create_tables.sql), then [`sql/rds/load_data.sql`](../../sql/rds/load_data.sql) (`\copy`), then [`sql/rds/verify_data.sql`](../../sql/rds/verify_data.sql).

## Security note

The POC security group allowed PostgreSQL (5432) from `0.0.0.0/0` so that Glue and CloudShell could connect. That is acceptable only for a short-lived learning environment. Do not repeat it in real environments; restrict access to the VPC or known CIDRs. Never commit the endpoint or credentials.
