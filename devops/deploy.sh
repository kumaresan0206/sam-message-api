#!/bin/bash
set -e

# ── Config ──────────────────────────
STACK_NAME="message-api-stack"
REGION="ap-south-1"
ENVIRONMENT="dev"
PROJECT_NAME="message-api"

# ── Colors ──────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# ── Build ───────────────────────────

rm -rf .aws-sam
echo -e "${BLUE}Building SAM project...${NC}"
sam build
echo -e "${GREEN}Build successful!${NC}"

# ── Deploy ──────────────────────────
echo -e "${BLUE}Deploying stack: $STACK_NAME...${NC}"
sam deploy \
    --stack-name "$STACK_NAME" \
    --parameter-overrides "Environment=$ENVIRONMENT" "ProjectName=$PROJECT_NAME" \
    --capabilities CAPABILITY_IAM \
    --region "$REGION" \
    --resolve-s3

echo -e "${GREEN}Deploy successful!${NC}"

# ── Outputs ──────────────────────────
echo -e "${BLUE}Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query "Stacks[0].Outputs" \
    --output table