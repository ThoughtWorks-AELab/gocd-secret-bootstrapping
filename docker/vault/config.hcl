storage "inmem" {}

listener "tcp" {
  address     = "0.0.0.0:8200"
  #TODO distribute TLS certificates and change this setting
  tls_disable = 0
  tls_cert_file = "/etc/vault/certs/vault.pem"
  tls_key_file = "/etc/vault/private/vault.pem"
}

#TODO enable this by setting linux permissions to allow mlock for process
disable_mlock = 1

