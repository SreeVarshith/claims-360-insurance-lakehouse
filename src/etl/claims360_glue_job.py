"""
Claims360-Job  -  AWS Glue 4.0 (PySpark, G.1X)

Extract  : customers + policies from RDS PostgreSQL (JDBC)
           claims from DynamoDB (Glue DynamicFrame)
Transform: normalize, handle schema evolution, fix types, derive keys,
           join, keep the latest record per claim
Load     : Delta Lake on S3 (initial write, then MERGE / upsert)

Sections marked [SCAFFOLDING] are standard Glue/Delta boilerplate that the
project report did not show; everything else follows the report's code.

Job parameters (Glue console -> Job details -> Job parameters):
    --DB_HOST  --DB_PORT  --DB_NAME  --DB_USER  --DB_PASSWORD
    --SILVER_PATH        e.g. s3://<bucket>/silver/delta/insurance_claims/
    --DYNAMODB_TABLE     e.g. ClaimStatusAudit
    --AWS_REGION         e.g. us-east-1
    --datalake-formats   delta        (enables Delta Lake in Glue 4.0)

Never hardcode credentials. For anything beyond a POC, read the password
from AWS Secrets Manager instead of a job parameter.
"""
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from delta.tables import DeltaTable
from pyspark.context import SparkContext
from pyspark.sql import Window
from pyspark.sql.functions import (
    col, concat, lit, regexp_extract, row_number, to_timestamp,
)

# ── [SCAFFOLDING] Glue / Spark initialisation ────────────────────────
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD",
     "SILVER_PATH", "DYNAMODB_TABLE", "AWS_REGION"],
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

JDBC_URL = f"jdbc:postgresql://{args['DB_HOST']}:{args['DB_PORT']}/{args['DB_NAME']}"
SILVER_PATH = args["SILVER_PATH"]
JDBC_OPTIONS = {
    "url": JDBC_URL,
    "user": args["DB_USER"],
    "password": args["DB_PASSWORD"],
    "driver": "org.postgresql.Driver",
}

# ── EXTRACT ──────────────────────────────────────────────────────────
# 1. Customers
df_customers_raw = spark.read.format("jdbc").options(
    dbtable="customers", **JDBC_OPTIONS
).load()

df_customers = df_customers_raw \
    .withColumnRenamed("cust_id", "c_cust_id") \
    .withColumnRenamed("name", "c_name") \
    .withColumnRenamed("email", "c_email") \
    .withColumnRenamed("risk_segment", "risk_segment")

# 2. Policies
df_policies_raw = spark.read.format("jdbc").options(
    dbtable="policies", **JDBC_OPTIONS
).load()

df_policies = df_policies_raw \
    .withColumnRenamed("policy_id", "p_policy_id") \
    .withColumnRenamed("cust_id", "p_cust_id") \
    .withColumnRenamed("type", "policy_type") \
    .withColumnRenamed("premium", "premium_amount")

# 3. Claims from DynamoDB
df_claims_raw = glueContext.create_dynamic_frame.from_options(
    connection_type="dynamodb",
    connection_options={
        "dynamodb.input.tableName": args["DYNAMODB_TABLE"],
        "dynamodb.throughput.read.percent": "1.0",
        "dynamodb.region": args["AWS_REGION"],
    },
).toDF()

# ── TRANSFORM ────────────────────────────────────────────────────────
# Normalize column names
df_claims_raw = df_claims_raw.toDF(*[c.lower() for c in df_claims_raw.columns])

# -----------------------------
# SCHEMA EVOLUTION HANDLING
# -----------------------------
if "adjuster_note" not in df_claims_raw.columns:
    df_claims_raw = df_claims_raw.withColumn("adjuster_note", lit(None))

# Handle schema differences
if "amount" in df_claims_raw.columns:
    df_claims_raw = df_claims_raw.withColumnRenamed("amount", "amount_claimed")

# Fix types
df_claims_raw = df_claims_raw.withColumn(
    "updated_at", to_timestamp(col("updated_at"))
).withColumn(
    "amount_claimed", col("amount_claimed").cast("double")
)

# Add derived keys
# POC-ONLY: the synthetic dataset has no real claim->policy link, so the
# customer/policy IDs are derived from the numeric part of claim_id.
# This is a demo mechanism, not a real-world modeling practice.
df_claims = df_claims_raw \
    .withColumn(
        "derived_cust_id",
        (regexp_extract(col("claim_id"), r"(\d+)", 1).cast("int") % 50 + 1)
    ) \
    .withColumn(
        "derived_policy_id",
        concat(
            lit("POL_"),
            (
                (regexp_extract(col("claim_id"), r"(\d+)", 1).cast("int") % 50 + 1) + 100
            ).cast("string")
        )
    )

df_step1 = df_claims.join(
    df_policies,
    df_claims["derived_policy_id"] == df_policies["p_policy_id"],
    "left"
)

df_step2 = df_step1.join(
    df_customers,
    df_step1["derived_cust_id"] == df_customers["c_cust_id"],
    "left"
)

df_final_raw = df_step2.select(
    col("claim_id"),
    col("updated_at"),
    col("status"),
    col("amount_claimed").alias("amount"),
    col("derived_cust_id").alias("cust_id"),
    col("derived_policy_id").alias("policy_id"),
    col("policy_type"),
    col("premium_amount"),
    col("c_name").alias("customer_name"),
    col("risk_segment"),
    col("adjuster_note"),  # column added to demonstrate schema evolution
)

# Latest record per claim
window_spec = Window.partitionBy("claim_id").orderBy(col("updated_at").desc())

df_final = df_final_raw \
    .withColumn("row_num", row_number().over(window_spec)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")

print(f"Total records to write: {df_final.count()}")
df_final.printSchema()

# Allow Delta to evolve the table schema on write/merge (see docs/pipeline.md)
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# ── LOAD (DELTA MERGE) ───────────────────────────────────────────────
if DeltaTable.isDeltaTable(spark, SILVER_PATH):
    delta_table = DeltaTable.forPath(spark, SILVER_PATH)
    delta_table.alias("existing").merge(
        df_final.alias("incoming"),
        "existing.claim_id = incoming.claim_id"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()
    print("Merge complete.")
else:
    df_final.write.format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .save(SILVER_PATH)
    print("Initial write complete.")

# NOTE: The report states that all historical records are appended to
# silver/delta/insurance_claims_history/, but the code for that step is not
# shown in the report, so it is intentionally NOT reproduced here.

# ── DONE ─────────────────────────────────────────────────────────────
job.commit()
print("✓ ETL job finished successfully.")
