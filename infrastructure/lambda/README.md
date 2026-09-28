# AWS Lambda `[IMPLEMENTED in POC]`

| Parameter | Value |
|---|---|
| Function | `triggers-glue-job-1` |
| Code | [`src/lambda/trigger_glue_job.py`](../../src/lambda/trigger_glue_job.py) |
| Role | `LambdaGlueTriggerRole` |
| Trigger | S3 `ObjectCreated:Put`, prefix `bronze/rds/`, suffix `policies.csv` (notification `lambda-glue-trigger`) |
| Environment variable | `GLUE_JOB_NAME` (defaults to `Claims360-Job`) |

## Event flow

1. `policies.csv` lands in `bronze/rds/`.
2. S3 invokes the function.
3. The function loops over `event["Records"]`, checks that the key contains `policies.csv`, and calls `glue.start_job_run()`.
4. Any failure is printed to CloudWatch Logs.

`policies.csv` is treated as the "batch is ready" signal, so upload `customers.csv` (and `claims_audit.json`) first.

> **Name mismatch in the report:** the Glue job is called `Claims360-Job` in the text, but the Lambda code and Glue console screenshot use `Claims360_Job`. Set `GLUE_JOB_NAME` to the exact name in your account.
