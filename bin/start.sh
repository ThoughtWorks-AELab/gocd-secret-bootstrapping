#!/bin/bash

set -e

kubectl create -f ./kubernetes/go-cd-server.yml

./bin/set-register-key.py

kubectl create -f ./kubernetes/go-cd-agent.yml
kubectl create -f ./kubernetes/vault.yml
kubectl create -f ./kubernetes/vault-setup.yml
# ./bin/set-vault-cert.py

minikube service list