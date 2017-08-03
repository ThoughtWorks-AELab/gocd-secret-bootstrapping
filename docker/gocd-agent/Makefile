.PHONY: all build clean
all: push

STAMP=`date +'%Y-%m-%d_%H%M%S'`

build:
	docker build --tag "danielsomerfield/gocd-agent-java:latest" --tag "danielsomerfield/gocd-agent-java:${STAMP}" .

push: build
	docker push danielsomerfield/gocd-agent-java

clean:
	docker rmi -f danielsomerfield/gocd-agent-java