# Amazon S3 — Data Lake `[DOCUMENTATION]`

Bucket: `claims360-lakehouse` (use your own globally unique name when reproducing).

```text
s3://claims360-lakehouse/
├── bronze/
│   ├── dynamodb/
│   │   └── claims_audit.json
│   └── rds/
│       ├── customers.csv
│       └── policies.csv
└── silver/
    ├── Claims-360-athena/
    └── delta/
        ├── insurance_claims/
        └── insurance_claims_history/
```

| Path | Purpose |
|---|---|
| `bronze/` | Raw incoming files from the source systems |
| `bronze/rds/` | `customers.csv`, `policies.csv`. Uploading `policies.csv` here fires the Lambda trigger |
| `bronze/dynamodb/` | `claims_audit.json` |
| `silver/delta/insurance_claims/` | Current-state Delta table (one row per claim) |
| `silver/delta/insurance_claims_history/` | History table documented in the report |
| `silver/Claims-360-athena/` | Athena query result location |

There is no Gold layer in this POC.

## Event notification (`lambda-glue-trigger`)

| Setting | Value |
|---|---|
| Event type | `s3:ObjectCreated:Put` |
| Prefix | `bronze/rds/` |
| Suffix | `policies.csv` |
| Destination | Lambda `triggers-glue-job-1` |

## Delta table contents

Each Delta folder holds Parquet data files plus `_delta_log/` (one JSON commit per version, with `.crc` checksums).
