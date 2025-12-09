#!/bin/bash

curl http://localhost:8080/tyk/apis -H "X-Tyk-Authorization: foo" | jq
