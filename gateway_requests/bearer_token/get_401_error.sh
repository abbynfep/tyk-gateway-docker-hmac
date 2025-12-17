#!/bin/bash

echo "asserts that the endpoint rejects requests without authorization"
echo

echo "With no header:"
curl -X POST http://localhost:8080/tokenWebhook -v
echo
echo
echo "With incorrect header:"
curl -X POST -H 'Authorization: incorrect' -H 'Authorization: incorrect' http://localhost:8080/tokenWebhook -v
