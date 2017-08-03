FROM mfanderson/gocd_agent

RUN apk add openjdk8 make docker curl

RUN curl -O https://storage.googleapis.com/kubernetes-release/release/v1.6.1/bin/linux/amd64/kubectl
RUN chmod +x kubectl
RUN mv kubectl /usr/local/bin/kubectl

RUN curl -O https://releases.hashicorp.com/vault/0.7.3/vault_0.7.3_linux_amd64.zip
RUN unzip vault_0.7.3_linux_amd64.zip
RUN mv vault /usr/local/bin/vault

#TODO: need to set config and map to the certs