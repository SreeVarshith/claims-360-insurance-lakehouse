# Data Lineage

| Hop | From → To | How | Notes |
|---|---|---|---|
| 1 | Generator → RDS | `\copy` in psql via CloudShell | `customers`, `policies` |
| 2 | Generator → DynamoDB | CloudShell commands (not shown in report) | `ClaimStatusAudit` |
| 3 | Generator → S3 Bronze | file upload | `bronze/rds/`, `bronze/dynamodb/` |
| 4 | Bronze → Lambda | S3 `ObjectCreated:Put` on `bronze/rds/*policies.csv` | Signal only; Lambda does not read the file |
| 5 | Lambda → Glue | `glue.start_job_run()` | Starts `Claims360-Job` |
| 6 | RDS → Glue | JDBC | customers, policies |
| 7 | DynamoDB → Glue | Glue DynamicFrame | claim audit entries |
| 8 | Glue → Delta (Silver) | `MERGE` / initial write | `silver/delta/insurance_claims/` |
| 9 | Delta → Glue Data Catalog | external table with `table_type = DELTA` | `claims_table_v2` |
| 10 | Catalog → Athena | SQL | results stored in `silver/Claims-360-athena/` |

## Column lineage (key fields)

| Silver column | Source |
|---|---|
| `claim_id`, `updated_at`, `status` | DynamoDB `ClaimStatusAudit` |
| `amount` | DynamoDB `amount` (→ `amount_claimed` → `amount`) |
| `cust_id`, `policy_id` | derived from `claim_id` |
| `policy_type`, `premium_amount` | RDS `policies` (`type`, `premium` in the CSV) |
| `customer_name`, `risk_segment` | RDS `customers` |
| `adjuster_note` | DynamoDB (null when absent) |
