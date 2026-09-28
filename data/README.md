# Sample Data

The POC uses synthetic data produced by [`src/data_generation/generate_dataset.py`](../src/data_generation/generate_dataset.py).

| File | Format | Records | Loaded into |
|---|---|---|---|
| `customers.csv` | CSV | 50 | RDS `customers` |
| `policies.csv` | CSV | 50 | RDS `policies` |
| `claims_audit.json` | JSON (records) | 100 | DynamoDB `ClaimStatusAudit` |

| File | Columns |
|---|---|
| `customers.csv` | `cust_id, name, email, risk` (Low / Med / High) |
| `policies.csv` | `policy_id, cust_id, type, premium` |
| `claims_audit.json` | `claim_id, updated_at, status, amount` |

## Generate

```bash
pip install pandas
python src/data_generation/generate_dataset.py                 # writes to data/sample/
python src/data_generation/generate_dataset.py --output data/sample --seed 42
```

Claim IDs range from `CLM_1000` to `CLM_1020`, so the 100 entries cover at most 21 distinct claims, each with several status updates.

The generated files are random and git-ignored. Regenerate them rather than committing them.
`adjuster_note` is not produced by the generator; it was added to the DynamoDB data to demonstrate schema evolution.
