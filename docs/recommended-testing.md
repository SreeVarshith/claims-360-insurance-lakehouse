# Recommended Testing

> **[RECOMMENDED] — no automated tests were implemented or run in this POC.** This lists what would be worth adding (for example under a `tests/` folder with pytest and a local Spark session).

| Area | Example check |
|---|---|
| Generated dataset schema | 50 customers, 50 policies, 100 claims; expected columns; risk in {Low, Med, High}; status in {Open, Under_Review, Paid} |
| Duplicate claims | Input has repeated `claim_id`; output has exactly one row per `claim_id` |
| Latest record selection | For a claim with several `updated_at` values, the output row has the maximum timestamp |
| Schema evolution | Input without `adjuster_note` still produces the column (all null); input with it keeps values |
| Null handling | Unmatched joins produce nulls rather than dropped claims (left joins) |
| Derived keys | `CLM_1005` → `derived_cust_id` 6, `derived_policy_id` `POL_106` |
| Transformed schema | Output columns and types match [data-model.md](data-model.md) |
| MERGE | A second run updates existing claims and inserts new ones without duplicating rows |
