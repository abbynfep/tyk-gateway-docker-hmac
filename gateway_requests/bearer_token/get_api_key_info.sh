#!/bin/bash

echo "Shows the info for the key. Fun but not necessary. You need to paste the key into this script."

KEYID=default62371065d6464721a9f0e98f8278cd82
curl -H 'X-Tyk-Authorization: foo' http://localhost:8080/tyk/keys/$KEYID | jq
