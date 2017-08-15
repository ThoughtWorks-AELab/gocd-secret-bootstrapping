#!/bin/sh

mkdir -p /etc/vault/certs
mkdir -p /etc/vault/private

cat > csr_details.txt <<-EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
CN = $VAULT_SERVICE_HOST

[ req_ext ]
basicConstraints = CA:FALSE  

# This next line is critical so that you can connect to the IP address
subjectAltName = @alt_names

[alt_names]
IP.1 = $VAULT_SERVICE_HOST
DNS.1 = vault

EOF

openssl genrsa -out /etc/vault/private/vault.pem 3072
openssl req -extensions req_ext -new -x509 -days 365 -nodes \
    -out /etc/vault/certs/vault.pem \
    -key /etc/vault/private/vault.pem \
    -config csr_details.txt

rm csr_details.txt