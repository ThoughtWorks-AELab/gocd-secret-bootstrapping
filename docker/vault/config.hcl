storage "inmem" {}

listener "tcp" {
  address     = "0.0.0.0:8200"
  #These two lines need to be fixed once mlock is enabled on container and TLS certs are distributed
  tls_disable = 1
}

disable_mlock = 1

