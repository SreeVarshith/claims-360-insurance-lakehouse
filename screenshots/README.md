# Screenshots

Place **sanitized** screenshots from the project report in the matching folder. Suggested names and the report page each comes from (page numbers follow the report's footer; double-check against your PDF):

| Folder | Suggested file | Report page |
|---|---|---|
| `s3/` | `01-bucket-overview.png`, `02-bucket-structure.png` | 5 |
| `aws/` | `iam-glue-etl-role.png`, `iam-lambda-trigger-role.png` | 6 |
| `rds/` | `01-instance-summary.png`, `02-security-group.png` | 7 |
| `dynamodb/` | `claimstatusaudit-items.png` | 9 |
| `glue/` | `claims360-job-list.png` | 10 |
| `lambda/` | `triggers-glue-job-1.png` | 14 |
| `athena/` | `01-select-query.png`, `02-paid-claims-per-risk.png`, `03-adjuster-note-schema.png`, `04-adjuster-note-query.png` | 15–17 |
| `s3/` | `delta-log.png` | 16 |

## Before you commit

The IAM, Lambda and RDS screenshots show a 12-digit AWS account ID, ARNs, security group IDs and the RDS identifier. Blur or crop those areas. Do not add screenshots you have not reviewed.
