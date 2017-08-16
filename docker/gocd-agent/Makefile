.PHONY: all build clean
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build:
	docker build --tag "${REGISTRY_USERNAME}/gocd-agent-java:latest" --tag "${REGISTRY_USERNAME}/gocd-agent-java:${STAMP}" .

push: build
	docker push ${REGISTRY_USERNAME}/gocd-agent-java

clean:
	docker rmi -f ${REGISTRY_USERNAME}/gocd-agent-java