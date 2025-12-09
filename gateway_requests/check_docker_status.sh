#!/bin/bash

echo "Checks the status of the tyk gateway and redis instance in the docker container"
echo
curl http://localhost:8080/hello -i
