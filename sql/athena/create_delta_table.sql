-- Register the Delta table in the AWS Glue Data Catalog (from the report).
-- Run in the Athena query editor, in the Glue database used in the POC
-- ("claims-insurance-db" in the report's screenshots).
--
-- Athena needs no column list for Delta tables: the schema is read from
-- the Delta transaction log.

CREATE EXTERNAL TABLE claims_table_v2
LOCATION 's3://claims360-lakehouse/silver/delta/'
TBLPROPERTIES ('table_type' = 'DELTA');

-- NOTE: the LOCATION must point at the folder that directly contains
-- _delta_log/ for the current-state table. The Glue job writes to
-- silver/delta/insurance_claims/, so if the query returns no data, point
-- LOCATION there. Replace the bucket name with your own.
