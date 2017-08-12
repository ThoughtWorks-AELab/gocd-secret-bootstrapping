#!/bin/bash

set -e

kubectl create -f ./kubernetes/go-cd-server.yml
key=`./bin/set-register-key.py`
if [[ $? != 0 ]]; then
    echo "Failed to get key: $key"
    exit 1
fi

kubectl create -f ./kubernetes/go-cd-agent.yml
kubectl create -f ./kubernetes/vault.yml
minikube service list