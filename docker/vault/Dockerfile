FROM alpine:3.5

EXPOSE 8200
RUN mkdir /etc/vault

RUN apk update
RUN apk add curl
RUN apk add openssl
RUN curl -O https://releases.hashicorp.com/vault/0.7.3/vault_0.7.3_linux_amd64.zip
RUN unzip vault_0.7.3_linux_amd64.zip
RUN mv vault /usr/local/bin/vault

# Need to run this not in dev mode or it will only bind to localhost

ENTRYPOINT ["/docker-entrypoint.sh"]

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


ADD gencert.sh /gencert.sh
RUN chmod +x /gencert.sh

ADD config.hcl /etc/vault/config.hcl
