# app/s3_utils.py
import boto3
from datetime import datetime
from flask import current_app


def upload_orders_to_s3(orders):
    bucket = current_app.config.get("S3_BUCKET")
    if not bucket:
        current_app.logger.info("S3_BUCKET_NAME not set, skipping S3 upload")
        return

    region = current_app.config.get("AWS_REGION", "eu-west-1")
    s3 = boto3.client("s3", region_name=region)

    # Construim conținut CSV simplu
    lines = ["id,customer_name,coffee_type,size,created_at"]
    for o in orders:
        lines.append(
            f"{o['id']},{o['customer_name']},{o['coffee_type']},{o['size']},{o['created_at']}"
        )
    body = "\n".join(lines).encode("utf-8")

    key = f"reports/orders_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

    s3.put_object(Bucket=bucket, Key=key, Body=body)
    current_app.logger.info("Uploaded orders report to S3: %s/%s", bucket, key)

