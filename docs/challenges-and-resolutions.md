# Challenges and Resolutions

| Challenge | Resolution |
|---|---|
| Joining relational and NoSQL data sources | Glue DynamicFrames for the DynamoDB read, combined with Spark joins |
| Repeated claim IDs across audit entries | Window function selecting the latest record per `claim_id` |
| Source schema changes | Runtime missing-column handling plus Delta `mergeSchema` |
| ACID-compliant writes | Delta transaction log and MERGE operations |
| Historical claim querying | History table plus Athena / Delta capabilities |
| Pipeline automation | S3 event → Lambda → Glue |
