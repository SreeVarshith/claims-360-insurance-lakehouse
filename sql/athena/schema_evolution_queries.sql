-- Schema evolution check (from the report):
-- adjuster_note was added to the source and now appears in the Delta table.

SELECT
    claim_id,
    adjuster_note
FROM "claims-insurance-db"."claims_table_v2";

-- Optional: inspect the registered schema
DESCRIBE claims_table_v2;
