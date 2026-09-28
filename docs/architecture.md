# Architecture

Claims 360 is a batch lakehouse on AWS. Data from a relational source (RDS PostgreSQL) and a NoSQL source (DynamoDB) is combined by an AWS Glue PySpark job and stored as Delta Lake tables on S3, then queried with Athena. See the [diagram](../diagrams/architecture.md).

## Why each service is used

| Service | Role in this POC |
|---|---|
| Amazon RDS (PostgreSQL) | Relational source for `customers` and `policies` |
| Amazon DynamoDB | NoSQL source: `ClaimStatusAudit`, multiple status entries per claim |
| Amazon S3 | Data lake storage: Bronze (raw) and Silver (Delta) |
| AWS Lambda | Starts the Glue job when `policies.csv` lands in Bronze |
| AWS Glue (PySpark) | ETL engine: extract, transform, join, dedupe, Delta MERGE |
| Delta Lake | ACID table format, MERGE upserts, schema evolution, transaction log |
| AWS Glue Data Catalog | Registers the Delta table so Athena can find it |
| Amazon Athena | Serverless SQL over the Delta table |
| AWS IAM | Roles for Glue (`Claims_GlueETLRole`) and Lambda (`LambdaGlueTriggerRole`) |
| Amazon CloudWatch | Logs from Lambda and Glue runs |

## Layers

- **Bronze** — raw incoming files from the source systems.
- **Silver** — processed Delta Lake tables (`insurance_claims` current state, `insurance_claims_history` history).
- No Gold layer is documented in the report.

## Design notes

- **Bronze vs. extraction:** the Bronze files are uploaded to S3 and drive the trigger. The Glue script, however, reads customers and policies straight from RDS over JDBC and claims straight from DynamoDB. Bronze therefore works as the raw landing copy and event signal in this POC.
- **Batch, not streaming:** each run processes the full current source data. Streaming (Kinesis, DynamoDB Streams) is future work.
- **Scope:** this is a capstone POC. Security shortcuts are listed in [SECURITY.md](../SECURITY.md).
