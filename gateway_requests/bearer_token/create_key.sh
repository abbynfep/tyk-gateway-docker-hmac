#!/bin/bash

echo "Creates token for authorization"
echo

curl -X POST http://localhost:8080/tyk/keys/create  \
    -H 'X-Tyk-Authorization: foo' \
    -d "{
        \"access_rights\": {
            \"Token-Webhook\": {
                \"allowed_urls\": [
                    {
                    \"methods\": [
                        \"POST\"
                    ],
                    \"url\": \"/tokenWebhook\"
                    }
                ],
                \"api_id\": \"Token-Webhook\",
                \"api_name\": \"Token-Webhook\",
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
        \"hmac_enabled\": false
    }" | jq
