#!/bin/bash

if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found"
    exit 1
fi

if [ -z "$API_KEY" ]; then
    echo "API_KEY is not set in .env"
    exit 1
fi

API_KEY_BASE64=$(echo -n "$API_KEY" | base64)

if [ -z "$API_KEY_BASE64" ]; then
    echo "Base64 encoding failed"
    exit 1
fi

if [ -z "$KAFKA_NAMESPACE" ]; then
    echo "KAFKA_NAMESPACE is not set in .env"
    exit 1
fi

envsubst < openaq-secret.yml | kubectl apply -f - -n $KAFKA_NAMESPACE
