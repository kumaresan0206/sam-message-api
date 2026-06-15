import json
import os

import boto3

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
        claims = event["requestContext"]["authorizer"]["claims"]

        current_user_id = claims["sub"]

        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="messages/")

        messages = []

        for obj in response.get("Contents", []):
            file_response = s3.get_object(Bucket=BUCKET_NAME, Key=obj["Key"])

            message = json.loads(file_response["Body"].read().decode("utf-8"))

            if message["user_id"] == current_user_id:
                messages.append(
                    {
                        "id": message["id"],
                        "message": message["message"],
                        "created_at": message["created_at"],
                    }
                )

        messages.sort(key=lambda x: x["created_at"], reverse=True)

        return success_response(messages)

    except Exception as e:
        print(str(e))

        return error_response("Internal server error", 500)
