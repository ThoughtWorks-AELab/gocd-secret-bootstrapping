.PHONY: all build clean
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build:
	docker build --tag "danielsomerfield/vault:latest" --tag "danielsomerfield/vault:${STAMP}" .

push: build
	docker push danielsomerfield/vault

clean:
	docker rmi -f danielsomerfield/vault