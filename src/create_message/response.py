import json


def success_response(data, status_code=200, message=None):
    return {
        "statusCode": status_code,
        "body": json.dumps({
            "success": True,
            "data": data,
            "message": message
        })
    }

def error_response(message, status_code):
    return {
        "statusCode": status_code,
        "body": json.dumps({
            "success": False,
            "message": message
        })
    }