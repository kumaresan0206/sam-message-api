import json


def lambda_handler(event, context):

    claims = event["requestContext"]["authorizer"]["claims"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "user_id": claims["sub"],
            "email": claims["email"]
        })
    }