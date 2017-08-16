.PHONY: all build clean
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build:
	docker build --tag "danielsomerfield/vault-init:latest" --tag "danielsomerfield/vault-init:${STAMP}" .

push: build
	docker push danielsomerfield/vault-init

clean:
	docker rmi -f danielsomerfield/vault-init