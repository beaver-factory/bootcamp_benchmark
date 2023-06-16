#!/bin/bash

SECRET_NAME="AZURE_FUNCTIONAPP_PUBLISH_PROFILE"

source ../.env

if [[ -z $ADZUNA_APP_KEY || -z $ADZUNA_APP_ID ]]; then
    echo "Error: .env must contain ADZUNA_APP_KEY and ADZUNA_APP_ID"
    exit 1
fi

GH_USER="northcoders-dev"

GH_REPO="bootcamp_benchmark"

# Create or update GitHub secrets
echo "$ADZUNA_APP_KEY" | gh secret set ADZUNA_APP_KEY -R$GH_USER/$GH_REPO
echo "$ADZUNA_APP_ID" | gh secret set ADZUNA_APP_ID -R$GH_USER/$GH_REPO

echo "ADZUNA_APP_ID and ADZUNA_APP_KEY set in GitHub secrets"