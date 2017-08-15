#!/bin/sh

/gencert.sh
/usr/local/bin/vault server -config /etc/vault/config.hcl