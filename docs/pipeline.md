# Pipeline

## Sequence

1. `customers.csv` and `policies.csv` are uploaded to `s3://claims360-lakehouse/bronze/rds/`.
2. `claims_audit.json` is uploaded to `bronze/dynamodb/`.
3. The S3 `ObjectCreated:Put` event fires for `policies.csv`.
4. Lambda `triggers-glue-job-1` is invoked.
5. Lambda calls `glue.start_job_run()` for the Glue job.
6. Glue reads RDS (JDBC) and DynamoDB (DynamicFrame).
7. Glue transforms and joins the data.
8. Delta tables are written or merged in Silver.
9. Parquet files and `_delta_log/` transaction logs appear in S3.
10. Athena queries the Delta table through the Glue Data Catalog.

## Transformations (in order)

| # | Step | Code idea |
|---|---|---|
| 1 | Normalize column names | lowercase all claim columns |
| 2 | Schema evolution | add `adjuster_note` as null if missing |
| 3 | Rename | `amount` → `amount_claimed` |
| 4 | Type fixes | `updated_at` → timestamp, `amount_claimed` → double |
| 5–6 | Derived keys | `derived_cust_id`, `derived_policy_id` from `claim_id` |
| 7–8 | Joins | claims ⟕ policies ⟕ customers (left joins) |
| 9 | Select business columns | rename to `amount`, `cust_id`, `policy_id`, `customer_name` |
| 10–11 | Deduplicate | `row_number()` over `Window.partitionBy("claim_id").orderBy(updated_at desc)`, keep 1 |

## Delta write

```python
if DeltaTable.isDeltaTable(spark, SILVER_PATH):
    # MERGE: update matching claims, insert new ones
    existing.claim_id = incoming.claim_id  ->  whenMatchedUpdateAll / whenNotMatchedInsertAll
else:
    # first run: overwrite with mergeSchema=true
```

## Current state vs. historical state

| | Current state | Historical state |
|---|---|---|
| Table | `insurance_claims` | `insurance_claims_history` |
| Content | Latest record per claim, upserted by MERGE | All audit records appended |
| Use | "What is the status now?" | "How did this claim change over time?" |

The report documents the history table and says records are appended to it, but it does not show the code. The repository does not invent that code.

## Schema evolution

**What it means:** the source schema changes over time (here, a new `adjuster_note` attribute).

**Why it breaks pipelines:** code that selects a column which is missing, or a target table with a fixed schema, fails when the source shape changes.

**How the POC handles it**

- The Glue script checks whether `adjuster_note` exists; if not, it adds it as `null`, so the `select` always works.
- The initial Delta write uses `mergeSchema=true`.
- `spark.databricks.delta.schema.autoMerge.enabled=true` lets the MERGE add new columns to the table.
- In Athena the new column appears in `claims_table_v2` and can be queried.

This demonstrates one column-addition scenario. It is not a full schema governance solution (no type-change handling, contracts, or validation).

## Delta transaction log and ACID

Each commit writes a numbered JSON file in `_delta_log/` (with a `.crc` checksum). Readers see only committed versions, which is how Delta provides ACID and versioned (time-travel) reads.

| Property | How it is achieved (per the report) |
|---|---|
| Atomicity | A commit is all-or-nothing; if the Glue job fails midway, the table stays at its last consistent version |
| Consistency | Schema constraints and types stay valid after each write |
| Isolation | Optimistic concurrency control manages concurrent reads/writes |
| Durability | Committed data lives in S3, referenced by immutable log entries |

No benchmarking or production validation was performed.

## Time travel

The report shows the `_delta_log/` folder with versions 0 and 1 (created on separate days), which is the basis for time travel. It does not show a time-travel query; see [`sql/athena/time_travel_queries.sql`](../sql/athena/time_travel_queries.sql).
