.PHONY: all build clean
all: push

build:
	docker build --tag "${REGISTRY_USERNAME}/java-app-base" .

push: build
	docker push ${REGISTRY_USERNAME}/java-app-base

clean:
	docker rmi -f ${REGISTRY_USERNAME}/java-app-base