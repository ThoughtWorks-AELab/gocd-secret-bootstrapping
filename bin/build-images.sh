#!/bin/sh

set -e

. .env
. ./.pythonenv/bin/activate

make -C docker/gocd-agent
make -C docker/java-app-base
make -C docker/vault
make -C docker/vault-setup
make -C docker/pipeline-service