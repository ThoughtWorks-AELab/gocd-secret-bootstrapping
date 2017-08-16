#!/bin/sh

set -e

. .env

make -C docker/gocd-agent
make -C docker/java-app-base
make -C docker/vault
make -C docker/vault-setup