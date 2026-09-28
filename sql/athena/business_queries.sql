-- Business query from the report: total paid claims per risk segment.
-- Gives analysts a quick view of financial exposure across risk categories.
-- (The report's snippet queries "claims_table"; the schema screenshot shows
--  claims_table_v2, which is used here.)

SELECT
    risk_segment,
    SUM(amount)      AS total_paid_claims,
    COUNT(claim_id)  AS claim_count
FROM claims_table_v2
WHERE status = 'Paid'
GROUP BY risk_segment;
