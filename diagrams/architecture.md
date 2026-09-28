# Architecture Diagram

Only services demonstrated in the POC appear here. Future enhancements are intentionally excluded.

```mermaid
flowchart LR
    subgraph SRC["Source systems"]
        RDS[("Amazon RDS PostgreSQL<br/>customers, policies")]
        DDB[("Amazon DynamoDB<br/>ClaimStatusAudit")]
    end

    subgraph S3["Amazon S3 - claims360-lakehouse"]
        BR["Bronze<br/>bronze/rds/<br/>bronze/dynamodb/"]
        SI["Silver - Delta Lake<br/>silver/delta/insurance_claims<br/>silver/delta/insurance_claims_history"]
        ATH_RES["silver/Claims-360-athena<br/>query results"]
    end

    LAM["AWS Lambda<br/>triggers-glue-job-1"]
    GLUE["AWS Glue - PySpark<br/>Claims360-Job"]
    CAT["Glue Data Catalog"]
    ATH["Amazon Athena"]
    CW["Amazon CloudWatch<br/>logs and monitoring"]
    IAM["AWS IAM roles"]

    BR -- "ObjectCreated:Put<br/>bronze/rds/policies.csv" --> LAM
    LAM -- "glue.start_job_run" --> GLUE
    RDS -- "JDBC read" --> GLUE
    DDB -- "DynamicFrame read" --> GLUE
    GLUE -- "Delta MERGE" --> SI
    SI --> CAT --> ATH
    ATH --> ATH_RES
    LAM -.-> CW
    GLUE -.-> CW
    IAM -.-> LAM
    IAM -.-> GLUE
```

The Bronze files are the raw copies of the source data (uploaded to S3) and act as the batch-ready signal. The ETL code itself reads from RDS and DynamoDB directly.
