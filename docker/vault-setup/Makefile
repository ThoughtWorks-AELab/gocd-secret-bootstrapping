.PHONY: all build clean
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build:
	docker build --tag "${REGISTRY_USERNAME}/vault-init:latest" --tag "${REGISTRY_USERNAME}/vault-init:${STAMP}" .

push: build
	docker push ${REGISTRY_USERNAME}/vault-init

clean:
	docker rmi -f ${REGISTRY_USERNAME}/vault-init