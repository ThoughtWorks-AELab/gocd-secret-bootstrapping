.PHONY: all build clean build-wheel
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build-wheel:
	cd service && python setup.py bdist_wheel

build: build-wheel
	docker build --tag "${REGISTRY_USERNAME}/pipeline-service:latest" --tag "${REGISTRY_USERNAME}/pipeline-service:${STAMP}" .

push: build
	docker push ${REGISTRY_USERNAME}/pipeline-service

clean:
	cd service && rm -rf .cache .eggs build dist pipelineservice.egg-info
	docker rmi -f ${REGISTRY_USERNAME}/pipeline-service
