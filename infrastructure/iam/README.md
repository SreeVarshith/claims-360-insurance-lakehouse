# IAM Roles `[IMPLEMENTED in POC]`

The POC uses two IAM roles to give Glue and Lambda their service permissions.

## `Claims_GlueETLRole` (attached to Glue job `Claims360-Job`)

| Policy | Type |
|---|---|
| `AmazonDynamoDBReadOnlyAccess` | AWS managed |
| `AmazonRDSReadOnlyAccess` | AWS managed |
| `AmazonS3FullAccess` | AWS managed |
| `AWSGlueServiceRole` | AWS managed |

## `LambdaGlueTriggerRole` (attached to Lambda `triggers-glue-job-1`)

| Policy | Type |
|---|---|
| `AWSLambdaBasicExecutionRole` | AWS managed (CloudWatch Logs) |
| `AWSGlueConsoleFullAccess` | AWS managed (allows starting Glue jobs) |

## Production note

The POC uses IAM roles to provide service permissions. For production deployment, these policies should be further restricted to resource-level least privilege (for example, S3 access limited to the lakehouse bucket and prefixes, and `glue:StartJobRun` limited to the one job).

Note that `AmazonS3FullAccess` and `AWSGlueConsoleFullAccess` are broad, so this configuration is **not** least-privilege.

No policy exports are committed here. If you add any, sanitize account IDs and ARNs first.
