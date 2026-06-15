# message-api

This folder contains an AWS SAM-based Python Lambda API for creating, listing, reading, and deleting user messages. It uses Amazon Cognito for request authorization and stores message payloads in an S3 bucket.

## What this project does

- Protects the API with a Cognito User Pool authorizer.
- Stores each message as a JSON object in S3 under `messages/<id>.json`.
- Uses the signed-in Cognito user ID (`sub`) to scope message access.
- Exposes API Gateway routes for profile and message operations.

## Folder layout

- `devops/` - SAM template and deployment script.
- `src/create_message/` - Lambda code for creating a message.
- `src/delete_message/` - Lambda code for deleting a message.
- `src/get_message/` - Lambda code for fetching a single message.
- `src/list_messages/` - Lambda code for listing the current user's messages.
- `src/profile/` - Lambda code for returning the authenticated user's profile data.

## API endpoints

- `GET /profile` - Returns the authenticated user's Cognito `sub` and email.
- `POST /message` - Creates a new message.
- `GET /messages` - Lists messages owned by the authenticated user.
- `GET /messages/{id}` - Returns one message if it belongs to the authenticated user.
- `DELETE /messages/{id}` - Deletes one message if it belongs to the authenticated user.

## Deployment

The folder includes a simple deploy script at `devops/deploy.sh`.

### Script flow

1. Removes the local `.aws-sam` build directory.
2. Runs `sam build`.
3. Runs `sam deploy` with the stack name `message-api-stack`.
4. Prints CloudFormation outputs after deployment.

### Notes

- The SAM template targets Python 3.13.
- The default region in the deploy script is `ap-south-1`.
- The template creates a Cognito User Pool, a Cognito App Client, an API Gateway API, and an S3 bucket.

## Runtime behavior

- Create message requests validate that the body exists, parse JSON, and reject empty or overly long messages.
- Read and delete operations verify ownership by comparing the stored `user_id` with the current Cognito `sub` claim.
- List operations filter S3 objects to only return messages that belong to the current user.

## Response format

Most handlers return JSON in the shape:

```json
{
  "success": true,
  "data": {}
}
```

Error responses follow the same pattern with `success: false` and a `message` field.
