#!/bin/bash

docker build -t "urosss/keycloak" -f "Dockerfile.orthanc-keycloak" .
docker build -t "urosss/nginx" -f "Dockerfile.orthanc-nginx" .
docker build -t "urosss/ohif-v3" -f "ohif/Dockerfile.ohif-v3" ohif
