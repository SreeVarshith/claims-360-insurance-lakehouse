# Amazon DynamoDB `[IMPLEMENTED in POC]`

| Parameter | Value |
|---|---|
| Table name | `ClaimStatusAudit` |
| Partition key | `claim_id` (String) |
| Sort key | `updated_at` (String) |
| Settings | Default |
| Status | Active |

Every status change of a claim is a separate item, so one `claim_id` has several audit entries (the sample data has 100 entries across `CLM_1000`–`CLM_1020`).

Attributes: `status` (`Open` / `Under_Review` / `Paid`), `amount`, and later `adjuster_note` (added to demonstrate schema evolution).

`claims_audit.json` was loaded into the table with AWS CloudShell commands (the report does not include them). Item counts were checked in the DynamoDB console.

> **DynamoDB Streams are not used.** They appear only under [Future Enhancements](../../docs/future-enhancements.md).
