import os
import uuid
from datetime import datetime, timezone, timedelta

import boto3
import requests


_s3_client = None


def _get_s3():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    return _s3_client


def upload_from_url(image_url: str) -> str:
    """
    Download an image from a URL and upload it to S3.
    Returns a pre-signed URL valid for 14 days.
    Filename is a UUID to prevent guessing.
    """
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "image/png")
    extension = "jpg" if "jpeg" in content_type else "png"
    key = f"images/{uuid.uuid4()}.{extension}"

    bucket = os.environ["AWS_BUCKET_NAME"]
    expires_at = datetime.now(timezone.utc) + timedelta(days=14)

    _get_s3().put_object(
        Bucket=bucket,
        Key=key,
        Body=response.content,
        ContentType=content_type,
        Expires=expires_at,
    )

    presigned_url = _get_s3().generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=14 * 24 * 60 * 60,  # 14 days in seconds
    )
    return presigned_url
