import json
import datetime
from time import timezone
import uuid

from response import error_response, success_response
from repository import create_message_repository


def create_message(event):

    try:
        # ----------------------------
        # Cognito User Claims
        # ----------------------------

        claims = event["requestContext"]["authorizer"]["claims"]

        user_id = claims["sub"]
        email = claims["email"]

        # ----------------------------
        # Request Body
        # ----------------------------

        if not event.get("body"):
            return error_response("Request body is required", 400)

        body = json.loads(event["body"])

        message = body.get("message")

        if not message:
            return error_response("Message is required", 400)

        message = message.strip()

        if len(message) == 0:
            return error_response("Message cannot be empty", 400)

        if len(message) > 1000:
            return error_response("Message exceeds maximum length", 400)

        # ----------------------------
        # Create Message Object
        # ----------------------------

        message_id = str(uuid.uuid4())

        message_data = {
            "id": message_id,
            "user_id": user_id,
            "email": email,
            "message": message,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        response = create_message_repository(message_data)

        return success_response(
            {"data": response, "message": "Message created successfully"}, 201
        )

    except json.JSONDecodeError:
        return error_response("Invalid JSON payload", 400)
    except Exception as e:
        print(str(e))
        return error_response("Internal server error", 500)
