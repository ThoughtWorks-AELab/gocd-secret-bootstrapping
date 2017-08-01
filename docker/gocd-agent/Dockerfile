FROM mfanderson/gocd_agent

RUN apk add openjdk8 make docker curl

RUN curl -O https://storage.googleapis.com/kubernetes-release/release/v1.6.1/bin/linux/amd64/kubectl

RUN chmod +x kubectl

RUN mv kubectl /usr/local/bin/kubectl

#TODO: need to set config and map to the certs