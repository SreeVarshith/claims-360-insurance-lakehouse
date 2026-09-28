"""
Claims 360 - synthetic dataset generator.

Generates the three sample files used in the POC:
    customers.csv      (50 records)   -> loaded into RDS PostgreSQL
    policies.csv       (50 records)   -> loaded into RDS PostgreSQL
    claims_audit.json  (100 records)  -> loaded into DynamoDB (ClaimStatusAudit)

Usage:
    python src/data_generation/generate_dataset.py
    python src/data_generation/generate_dataset.py --output data/sample
    python src/data_generation/generate_dataset.py --seed 42   # optional, reproducible
"""
import argparse
import os
import random
from datetime import datetime, timedelta

import pandas as pd

DEFAULT_OUTPUT = os.path.join("data", "sample")


def generate_insurance_data(output_path):
    os.makedirs(output_path, exist_ok=True)

    # RDS - Customers & Policies
    custs = [
        {
            "cust_id": i,
            "name": f"Insured_{i}",
            "email": f"insured_{i}@example.com",
            "risk": random.choice(["Low", "Med", "High"]),
        }
        for i in range(1, 51)
    ]

    policies = [
        {
            "policy_id": f"POL_{100 + i}",
            "cust_id": i,
            "type": "Auto",
            "premium": random.randint(500, 2000),
        }
        for i in range(1, 51)
    ]

    # DynamoDB - Claims Audit (multiple states per claim)
    claims = []
    for _ in range(100):
        c_id = f"CLM_{random.randint(1000, 1020)}"
        claims.append(
            {
                "claim_id": c_id,
                "updated_at": (
                    datetime.now() - timedelta(hours=random.randint(1, 100))
                ).isoformat(),
                "status": random.choice(["Open", "Under_Review", "Paid"]),
                "amount": round(random.uniform(1000, 5000), 2),
            }
        )

    pd.DataFrame(custs).to_csv(os.path.join(output_path, "customers.csv"), index=False)
    pd.DataFrame(policies).to_csv(os.path.join(output_path, "policies.csv"), index=False)
    pd.DataFrame(claims).to_json(
        os.path.join(output_path, "claims_audit.json"), orient="records"
    )

    print(f"Files generated at: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Claims 360 sample data.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output directory")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    generate_insurance_data(args.output)
