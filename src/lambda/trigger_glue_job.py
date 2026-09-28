"""
Lambda function: triggers-glue-job-1

Triggered by an S3 ObjectCreated:Put notification
    prefix : bronze/rds/
    suffix : policies.csv
Uploading policies.csv is treated as the signal that a data batch is ready,
and the function starts the Glue ETL job.

Configuration (Lambda environment variable):
    GLUE_JOB_NAME   name of the Glue job to start (default: Claims360-Job)
"""
import os

import boto3

glue = boto3.client("glue")

GLUE_JOB_NAME = os.environ.get("GLUE_JOB_NAME", "Claims360-Job")


def lambda_handler(event, context):
    print("Event received:", event)

    # SAFE CHECK
    if "Records" not in event:
        print("No S3 event found")
        return {"statusCode": 200}

    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        print("File uploaded:", key)

        if "policies.csv" in key:
            try:
                response = glue.start_job_run(JobName=GLUE_JOB_NAME)
                print("Glue Job Started:", response["JobRunId"])
            except Exception as e:
                print("Glue start failed:", str(e))

    return {"statusCode": 200}
