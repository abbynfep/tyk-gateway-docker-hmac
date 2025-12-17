#!/bin/bash

echo "Get the hmac secret string for the key"

KEYID=defaultcb80d7f9074d43059507fd6311d994ca
curl -H 'X-Tyk-Authorization: foo' http://localhost:8080/tyk/keys/$KEYID | jq
