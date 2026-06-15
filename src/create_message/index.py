import json 
from layers.common_layers.python.utils.response import error_response
from services import create_message

def lambda_handler(event, context):

    try:

        response = create_message(event)
        return response
    
    except json.JSONDecodeError:

        return error_response(
            "Invalid JSON payload",
            400
        )

    except Exception as e:
        print(str(e))
        return error_response(
            "Internal server error",
            500
        )