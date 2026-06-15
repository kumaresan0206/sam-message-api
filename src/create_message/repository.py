


import json
import os

import boto3

s3_client = boto3.client("s3")

BUCKET_NAME = os.environ["BUCKET_NAME"]
def create_message_repository(message_data):

    # ----------------------------
    # Save To S3
    # ----------------------------

    object_key = f"messages/{message_data['id']}.json"

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(message_data),
        ContentType="application/json"
    )

    return {
        "message_id": message_data["id"],
        "message": message_data["message"],
        "created_at": message_data["created_at"]
    }