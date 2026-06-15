import json
import os

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

BUCKET_NAME = os.environ["BUCKET_NAME"]


def success_response(data=None, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps({"success": True, "data": data}),
    }


def error_response(message, status_code):
    return {
        "statusCode": status_code,
        "body": json.dumps({"success": False, "message": message}),
    }


def lambda_handler(event, context):

    try:
        message_id = event["pathParameters"]["id"]

        claims = event["requestContext"]["authorizer"]["claims"]

        current_user_id = claims["sub"]

        key = f"messages/{message_id}.json"

        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=key)

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return error_response("Message not found", 404)

            raise

        message = json.loads(response["Body"].read().decode("utf-8"))

        if message["user_id"] != current_user_id:
            return error_response("Forbidden", 403)

        s3.delete_object(Bucket=BUCKET_NAME, Key=key)

        return success_response({"message": "Message deleted successfully"})

    except Exception as e:
        print(str(e))

        return error_response("Internal server error", 500)
