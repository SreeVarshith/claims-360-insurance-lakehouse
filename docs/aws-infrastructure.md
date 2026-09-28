# AWS Infrastructure

Resources created manually in the AWS console / CloudShell. No infrastructure-as-code was used in this POC.

| Resource | Name | Details |
|---|---|---|
| S3 bucket | `claims360-lakehouse` | Bronze / Silver layout, see [S3 README](../infrastructure/s3/README.md) |
| RDS | `insurance-db` | PostgreSQL, `db.t4g.micro`, `us-east-1c` |
| DynamoDB | `ClaimStatusAudit` | PK `claim_id`, SK `updated_at` |
| Glue job | `Claims360-Job` | PySpark, G.1X, role `Claims_GlueETLRole` |
| Lambda | `triggers-glue-job-1` | role `LambdaGlueTriggerRole` |
| S3 notification | `lambda-glue-trigger` | `ObjectCreated:Put`, `bronze/rds/`, `policies.csv` |
| Glue Data Catalog | database `claims-insurance-db` | table `claims_table_v2` (Delta) |
| Athena | workgroup `primary` | results in `silver/Claims-360-athena/` |
| CloudWatch | — | Lambda and Glue logs |
| IAM roles | `Claims_GlueETLRole`, `LambdaGlueTriggerRole` | see [IAM README](../infrastructure/iam/README.md) |

Per-service details: [`infrastructure/`](../infrastructure).
