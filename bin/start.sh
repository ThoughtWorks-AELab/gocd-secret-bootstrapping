#!/bin/bash
set -e

. ./.env
. ./.pythonenv/bin/activate

mkdir -p /tmp/gocd-secret-bootstrapping
# Substitute the username from env variable
sed -- 's/${REGISTRY_USERNAME}/'"${REGISTRY_USERNAME}"'/g' ./kubernetes/go-cd-agent.yml > /tmp/gocd-secret-bootstrapping/go-cd-agent.yml
sed -- 's/${REGISTRY_USERNAME}/'"${REGISTRY_USERNAME}"'/g' ./kubernetes/vault.yml > /tmp/gocd-secret-bootstrapping/vault.yml
sed -- 's/${REGISTRY_USERNAME}/'"${REGISTRY_USERNAME}"'/g' ./kubernetes/vault-setup.yml > /tmp/gocd-secret-bootstrapping/vault-setup.yml


kubectl create -f ./kubernetes/go-cd-server.yml

./bin/set-register-key.py

kubectl create -f /tmp/gocd-secret-bootstrapping/go-cd-agent.yml
kubectl create -f /tmp/gocd-secret-bootstrapping/vault.yml
kubectl create -f /tmp/gocd-secret-bootstrapping/vault-setup.yml

minikube service list