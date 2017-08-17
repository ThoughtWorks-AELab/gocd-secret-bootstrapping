FROM alpine:3.6

EXPOSE 5000

RUN apk update
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

ADD service/dist/pipelineservice*.whl /

RUN pip install /pipelineservice*.whl
# Need to run this not in dev mode or it will only bind to localhost

ENTRYPOINT ["/docker-entrypoint.sh"]

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh