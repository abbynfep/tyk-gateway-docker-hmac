#!/bin/bash

echo "Creates an HMAC key"

HMAC_STRING="secret-key"
echo $HMAC_STRING
echo

curl -X POST http://localhost:8080/tyk/keys/create  \
    -H 'X-Tyk-Authorization: foo' \
    -d "{
        \"access_rights\": {
            \"carrier-webhook\": {
                \"allowed_urls\": [
                    {
                    \"methods\": [
                        \"POST\"
                    ],
                    \"url\": \"/public/carrier/webhookTracking\"
                    }
                ],
                \"api_id\": \"carrier-webhook\",
                \"api_name\": \"carrier-webhook\",
                \"versions\": [
                    \"Default\"
                ]
            }
        },
        \"allowance\": 999,
        \"rate\": 1000,
        \"per\": 1,
        \"expires\": 0,
        \"quota_max\": -1,
        \"quota_renews\": 1406121006,
        \"quota_remaining\": 0,
        \"quota_renewal_rate\": 60,
        \"org_id\": \"default\",
        \"hmac_enabled\": true,
        \"hmac_string\": \"${HMAC_STRING}\"
    }" | jq
