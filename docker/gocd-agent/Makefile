.PHONY: all build clean
all: push

build:
	docker build --tag "danielsomerfield/gocd-agent-java" .

push: build
	docker push danielsomerfield/gocd-agent-java

clean:
	docker rmi -f danielsomerfield/gocd-agent-java