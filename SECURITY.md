# Security Policy

This is a learning / capstone POC published for portfolio purposes. It is **not** a production deployment.

## Rules for this repository

1. **Never commit credentials.** No passwords, access keys, tokens, `.pem`/`.key` files or `.env` files. `.gitignore` blocks the common patterns, but it is not a substitute for checking.
2. **Use configuration, not constants.** Local scripts read `.env` (see `.env.example`). In AWS, values come from Glue job parameters, Lambda environment variables and IAM roles.
3. **Use IAM roles for service access.** Glue and Lambda authenticate through their execution roles, never through embedded keys.
4. **Use AWS Secrets Manager beyond the POC.** Database passwords should be fetched at runtime instead of being passed as plain job parameters.
5. **Sanitize screenshots and reports before publishing.** Redact AWS account IDs, RDS endpoints, ARNs, security group IDs, and anything that resembles a secret.
6. **Rotate anything that was ever exposed.** If a password appeared in a document, notebook or commit, treat it as compromised and change it, even if the resource was temporary.

## Known POC-level shortcuts (documented, not recommended for production)

| Area | POC configuration | Production direction |
|---|---|---|
| RDS network access | Security group allowed PostgreSQL 5432 from `0.0.0.0/0` | Restrict to VPC / known CIDRs; keep the DB private |
| Glue role | `AmazonS3FullAccess` plus read-only DynamoDB/RDS managed policies | Resource-level least privilege (specific bucket/prefix/table) |
| DB password | Passed to the Glue job | Secrets Manager |

## Reporting

If you notice an exposed secret in this repository, please open an issue that does **not** include the secret itself, or contact the repository owner directly.
