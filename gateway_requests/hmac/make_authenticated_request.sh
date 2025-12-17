#!/bin/bash

echo "Makes an authenticated request to the hmac endpoint"

function urlencode() {
echo -n "$1" | perl -MURI::Escape -ne 'print uri_escape($_)' | sed "s/%20/+/g"
}

KEYID=default157f35a6b79b459c9b80a57f78bf02d3
HMAC_SECRET="YmEyYzlhYjg5ODRmNGU0ODhkMmY5NzgwMzU3MGYwOTg="
formatted_date="$(LC_ALL=C date -u +'%a, %d %b %Y %X %Z')"

signature=$(echo -n "date: ${formatted_date}" | openssl sha256 -binary -hmac $HMAC_SECRET|base64)
url_encoded_signature=$(urlencode "${signature}")

echo "date: $formatted_date"
echo "signature: $signature"
echo "url_encoded_signature: $url_encoded_signature"
echo "Authorization: Signature keyId=\"${KEYID}\",algorithm=\"hmac-sha256\",signature=\"${url_encoded_signature}\""

curl -X POST -H "Date: ${formatted_date}" -H "Authorization: Signature keyId=\"${KEYID}\",algorithm=\"hmac-sha256\",signature=\"${url_encoded_signature}\"" -H "Content-Type: application/json" 'http://localhost:8080/public/carrier/webhookTracking/' -vvv -d '{}'