FROM alpine:3.5

RUN mkdir -p /etc/vault/certificates

RUN apk update
RUN apk add python3
RUN apk add curl
RUN curl -O https://releases.hashicorp.com/vault/0.7.3/vault_0.7.3_linux_amd64.zip
RUN unzip vault_0.7.3_linux_amd64.zip
RUN mv vault /usr/local/bin/vault

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

ENTRYPOINT ["/docker-entrypoint.py"]

ADD docker-entrypoint.py /docker-entrypoint.py
RUN chmod +x /docker-entrypoint.py