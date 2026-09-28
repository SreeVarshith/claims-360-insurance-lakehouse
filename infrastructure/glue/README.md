# AWS Glue Job `[IMPLEMENTED in POC]`

| Parameter | Value |
|---|---|
| Job name | `Claims360-Job` |
| Glue version | 4.0 (per the report's table; the console screenshot shows 5.1, so confirm your own setting) |
| Worker type | G.1X |
| Language | Python (PySpark) |
| IAM role | `Claims_GlueETLRole` |
| Script | [`src/etl/claims360_glue_job.py`](../../src/etl/claims360_glue_job.py) |

## Job parameters

| Key | Example / purpose |
|---|---|
| `--DB_HOST`, `--DB_PORT`, `--DB_NAME`, `--DB_USER` | RDS connection details |
| `--DB_PASSWORD` | RDS password (Secrets Manager recommended beyond the POC) |
| `--SILVER_PATH` | `s3://<bucket>/silver/delta/insurance_claims/` |
| `--DYNAMODB_TABLE` | `ClaimStatusAudit` |
| `--AWS_REGION` | `us-east-1` |
| `--datalake-formats` | `delta` (turns on Delta Lake in Glue; not shown in the report but required to import `delta.tables`) |

The job connects to RDS over JDBC, so the Glue job needs network access to the database.

## Monitoring

Job runs write logs to Amazon CloudWatch.
