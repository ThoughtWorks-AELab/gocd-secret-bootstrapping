storage "inmem" {}

listener "tcp" {
  address     = "0.0.0.0:8200"
  #TODO distribute TLS certificates and change this setting
  tls_disable = 1
}

#TODO enable this by setting linux permissions to allow mlock for process
disable_mlock = 1

