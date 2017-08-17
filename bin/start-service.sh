#!/bin/bash
set -e

. ./.env
. ./.pythonenv/bin/activate

mkdir -p /tmp/gocd-secret-bootstrapping
# Substitute the username from env variable
sed -- 's/${REGISTRY_USERNAME}/'"${REGISTRY_USERNAME}"'/g' ./kubernetes/pipeline-service.yml > /tmp/gocd-secret-bootstrapping/pipeline-service.yml

kubectl create -f /tmp/gocd-secret-bootstrapping/pipeline-service.yml

minikube service list