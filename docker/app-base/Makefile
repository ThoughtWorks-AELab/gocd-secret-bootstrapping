.PHONY: all build clean
all: push

build:
	docker build --tag "danielsomerfield/java-app-base" .

push: build
	docker push danielsomerfield/java-app-base

clean:
	docker rmi -f danielsomerfield/java-app-base